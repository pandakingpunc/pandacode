import { afterEach, describe, expect, it } from "bun:test";
import * as fs from "node:fs";
import * as path from "node:path";
import { PANDACODE_SCENES, selectSetupScenes } from "@oh-my-pi/pi-coding-agent/modes/setup";
import type { InteractiveModeContext } from "@oh-my-pi/pi-coding-agent/modes/types";
import { TempDir } from "@oh-my-pi/pi-utils";
import { launcherFiles, MARKER } from "../../../scripts/install-pandacode";

const REPO_ROOT = path.resolve(import.meta.dir, "..", "..", "..");
const INSTALLER = path.join(REPO_ROOT, "scripts", "install-pandacode.ts");

describe("PandaCode onboarding", () => {
	it("runs sign-in, model and theme only", async () => {
		expect(PANDACODE_SCENES.map(scene => scene.id)).toEqual(["providers", "model", "theme"]);
		const ctx = {
			session: { modelRegistry: { getAvailable: () => [{ provider: "configured", id: "model" }] } },
		} as unknown as InteractiveModeContext;
		const scenes = await selectSetupScenes(0, PANDACODE_SCENES, ctx, { isTTY: true });
		expect(scenes.map(scene => scene.id)).toEqual(["providers", "model", "theme"]);
	});
});

describe("pandacode launcher", () => {
	let tempDir: TempDir | undefined;

	afterEach(() => {
		tempDir?.removeSync();
		tempDir = undefined;
	});

	function install(binDir: string, ...extra: string[]) {
		return Bun.spawnSync(["bun", INSTALLER, "--bin-dir", binDir, ...extra], { stdout: "pipe", stderr: "pipe" });
	}

	it("points every launcher at this checkout", () => {
		const posix = launcherFiles(REPO_ROOT, "linux");
		expect([...posix.keys()]).toEqual(["pandacode"]);
		expect(posix.get("pandacode")).toContain(`${REPO_ROOT.replaceAll("\\", "/")}/packages/coding-agent/scripts/omp`);

		const windows = launcherFiles(REPO_ROOT, "win32");
		expect([...windows.keys()]).toEqual(["pandacode", "pandacode.cmd"]);
		const cmd = windows.get("pandacode.cmd")!;
		expect(cmd).toContain(MARKER);
		expect(cmd).toContain(path.join(REPO_ROOT, "packages", "coding-agent", "src", "cli.ts"));
		expect(cmd).toContain('set "OMP_LAUNCH_CWD=%CD%"');
	});

	it("installs, refuses to overwrite a foreign file and uninstalls its own", () => {
		tempDir = TempDir.createSync("@pandacode-launcher-");
		const binDir = tempDir.path();

		expect(install(binDir).exitCode).toBe(0);
		const names = [...launcherFiles(REPO_ROOT).keys()];
		for (const name of names) expect(fs.readFileSync(path.join(binDir, name), "utf8")).toContain(MARKER);

		// Reinstalling over its own launchers is fine.
		expect(install(binDir).exitCode).toBe(0);

		const foreign = path.join(binDir, "pandacode");
		fs.writeFileSync(foreign, "someone else's launcher\n");
		expect(install(binDir).exitCode).toBe(1);
		expect(fs.readFileSync(foreign, "utf8")).toBe("someone else's launcher\n");

		fs.rmSync(foreign);
		expect(install(binDir, "--uninstall").exitCode).toBe(0);
		for (const name of names) expect(fs.existsSync(path.join(binDir, name))).toBe(false);
	});
});
