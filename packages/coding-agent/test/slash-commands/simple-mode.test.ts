import { describe, expect, it } from "bun:test";
import { Settings } from "@oh-my-pi/pi-coding-agent/config/settings";
import {
	BUILTIN_SLASH_COMMAND_DEFS,
	lookupBuiltinSlashCommand,
} from "@oh-my-pi/pi-coding-agent/slash-commands/builtin-registry";
import { SIMPLE_MODE_COMMANDS } from "@oh-my-pi/pi-coding-agent/slash-commands/simple-mode";
import { cfgShortcutBar, cfgSimpleMode } from "@oh-my-pi/pi-coding-agent/slash-commands/simple-mode-settings";
import type { TuiSlashCommandRuntime } from "@oh-my-pi/pi-coding-agent/slash-commands/types";

describe("simple mode", () => {
	it("keeps only real builtin names in the simple list", () => {
		const builtinNames = new Set(BUILTIN_SLASH_COMMAND_DEFS.map(cmd => cmd.name));
		for (const name of SIMPLE_MODE_COMMANDS) expect(builtinNames.has(name)).toBe(true);
		expect(SIMPLE_MODE_COMMANDS.size).toBeLessThan(builtinNames.size / 3);
	});

	it("is on by default, with the shortcut bar", () => {
		const settings = Settings.isolated();
		expect(cfgSimpleMode.get(settings)).toBe(true);
		expect(cfgShortcutBar.get(settings)).toBe(true);
	});

	it("/gelismis toggles the setting and reports the new mode", async () => {
		const command = lookupBuiltinSlashCommand("gelismis");
		expect(lookupBuiltinSlashCommand("advanced")).toBe(command);

		const settings = Settings.isolated();
		const statuses: string[] = [];
		let editorText = "/gelismis";
		const runtime = {
			ctx: {
				settings,
				showStatus: (text: string) => statuses.push(text),
				editor: { setText: (text: string) => (editorText = text) },
			},
		} as unknown as TuiSlashCommandRuntime;
		const parsed = { name: "gelismis", args: "", text: "/gelismis" };

		await command?.handleTui?.(parsed as never, runtime);
		expect(cfgSimpleMode.get(settings)).toBe(false);
		expect(statuses.at(-1)).toContain("Gelişmiş mod");
		expect(editorText).toBe("");

		await command?.handleTui?.(parsed as never, runtime);
		expect(cfgSimpleMode.get(settings)).toBe(true);
		expect(statuses.at(-1)).toContain("Sade mod");
	});
});
