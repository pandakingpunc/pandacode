#!/usr/bin/env bun
/**
 * Install the `pandacode` launcher: runs this checkout's CLI from source, the
 * way `scripts/setup.ts` links the `omp` dev launcher, but under its own name so
 * an installed `omp` is never touched.
 *
 * Writes into Bun's global bin dir (`bun pm -g bin`, then
 * `${BUN_INSTALL:-$HOME/.bun}/bin`), which Bun puts on PATH:
 * - `pandacode`: POSIX sh wrapper around `packages/coding-agent/scripts/omp`
 *   (Git Bash on Windows, any shell elsewhere).
 * - `pandacode.cmd` (Windows only): the same launch for cmd and PowerShell —
 *   Bun starts from a bunfig-free dir and the `omp.ts` preload restores the cwd.
 *
 * A file at either path is replaced only when it carries {@link MARKER}, so a
 * launcher this script did not write is left alone.
 *
 * Usage: bun scripts/install-pandacode.ts [--bin-dir <dir>] [--uninstall]
 */
import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";

export const MARKER = "pandacode-launcher";

/** Bun's global bin directory, as `scripts/setup.ts` resolves it. */
function globalBinDir(): string {
	const out = Bun.spawnSync(["bun", "pm", "-g", "bin"], { stdout: "pipe", stderr: "ignore" });
	const resolved = out.exitCode === 0 ? out.stdout.toString().trim() : "";
	return resolved || path.join(process.env.BUN_INSTALL ?? path.join(os.homedir(), ".bun"), "bin");
}

/** Launcher files for `repoRoot`, keyed by file name. */
export function launcherFiles(repoRoot: string, platform: NodeJS.Platform = process.platform): Map<string, string> {
	const scriptsDir = path.join(repoRoot, "packages", "coding-agent", "scripts");
	const shPath = path.join(scriptsDir, "omp").replaceAll("\\", "/");
	const files = new Map<string, string>();
	files.set(
		"pandacode",
		`#!/bin/sh\n# ${MARKER}: written by scripts/install-pandacode.ts\nexec sh "${shPath}" "$@"\n`,
	);
	if (platform === "win32") {
		const cli = path.join(repoRoot, "packages", "coding-agent", "src", "cli.ts");
		const preload = path.join(scriptsDir, "omp.ts");
		files.set(
			"pandacode.cmd",
			[
				"@echo off",
				`rem ${MARKER}: written by scripts/install-pandacode.ts`,
				"rem Start Bun from a bunfig-free dir; the omp.ts preload restores the real cwd.",
				"setlocal",
				'set "OMP_LAUNCH_CWD=%CD%"',
				'set "PANDACODE_LAUNCH_DIR=%USERPROFILE%\\.omp\\.dev-cwd"',
				'if not exist "%PANDACODE_LAUNCH_DIR%" mkdir "%PANDACODE_LAUNCH_DIR%"',
				'cd /d "%PANDACODE_LAUNCH_DIR%"',
				`bun --preload "${preload}" "${cli}" %*`,
				"exit /b %ERRORLEVEL%",
				"",
			].join("\r\n"),
		);
	}
	return files;
}

/** Whether `file` is absent or a launcher this script wrote. */
function ownedOrMissing(file: string): boolean {
	if (!fs.existsSync(file)) return true;
	try {
		return fs.readFileSync(file, "utf8").includes(MARKER);
	} catch {
		return false;
	}
}

function main(): number {
	const args = process.argv.slice(2);
	const binFlag = args.indexOf("--bin-dir");
	const binDir = binFlag >= 0 && args[binFlag + 1] ? path.resolve(args[binFlag + 1]!) : globalBinDir();
	const uninstall = args.includes("--uninstall");
	const repoRoot = path.resolve(import.meta.dir, "..");

	let failed = false;
	for (const [name, content] of launcherFiles(repoRoot)) {
		const target = path.join(binDir, name);
		if (!ownedOrMissing(target)) {
			console.error(`install-pandacode: ${target} exists and was not written by this script; left untouched`);
			failed = true;
			continue;
		}
		if (uninstall) {
			fs.rmSync(target, { force: true });
			console.log(`install-pandacode: removed ${target}`);
			continue;
		}
		fs.mkdirSync(binDir, { recursive: true });
		fs.writeFileSync(target, content, { mode: 0o755 });
		console.log(`install-pandacode: wrote ${target}`);
	}
	return failed ? 1 : 0;
}

if (import.meta.main) process.exit(main());
