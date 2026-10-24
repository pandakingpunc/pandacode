import { afterEach, describe, expect, it } from "bun:test";
import { Settings } from "@oh-my-pi/pi-coding-agent/config/settings";
import {
	BUILTIN_SLASH_COMMAND_DEFS,
	lookupBuiltinSlashCommand,
} from "@oh-my-pi/pi-coding-agent/slash-commands/builtin-registry";
import {
	localizeSimpleCommandTr,
	SIMPLE_MODE_COMMANDS,
	translateStatusTr,
} from "@oh-my-pi/pi-coding-agent/slash-commands/simple-mode";
import {
	cfgShortcutBar,
	cfgSimpleMode,
	cfgUiLanguage,
} from "@oh-my-pi/pi-coding-agent/slash-commands/simple-mode-settings";
import type { TuiSlashCommandRuntime } from "@oh-my-pi/pi-coding-agent/slash-commands/types";
import { setUiLanguage } from "@oh-my-pi/pi-tui/locale";

afterEach(() => {
	setUiLanguage("en");
});

describe("simple mode", () => {
	it("keeps only real builtin names in the simple list", () => {
		const builtinNames = new Set(BUILTIN_SLASH_COMMAND_DEFS.map(cmd => cmd.name));
		for (const name of SIMPLE_MODE_COMMANDS) expect(builtinNames.has(name)).toBe(true);
		expect(SIMPLE_MODE_COMMANDS.size).toBeLessThan(builtinNames.size / 3);
	});

	it("is on by default, with the shortcut bar and a Turkish interface", () => {
		const settings = Settings.isolated();
		expect(cfgSimpleMode.get(settings)).toBe(true);
		expect(cfgShortcutBar.get(settings)).toBe(true);
		expect(cfgUiLanguage.get(settings)).toBe("tr");
	});

	it("/gelismis toggles the setting and reports the new mode", async () => {
		setUiLanguage("tr");
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

		setUiLanguage("en");
		await command?.handleTui?.(parsed as never, runtime);
		expect(statuses.at(-1)).toContain("Advanced mode");
		expect(command?.description).toBe("Show or hide advanced commands (simple mode)");
	});
});

describe("Turkish picker copy", () => {
	it("gives every simple-mode builtin a Turkish description", () => {
		for (const def of BUILTIN_SLASH_COMMAND_DEFS) {
			if (!SIMPLE_MODE_COMMANDS.has(def.name) || def.name === "gelismis") continue;
			const localized = localizeSimpleCommandTr({ name: def.name, description: def.description });
			expect(localized.description).not.toBe(def.description);
		}
	});

	it("translates live status descriptions and leaves the rest alone", () => {
		expect(translateStatusTr("Thinking: high")).toBe("Düşünme: yüksek");
		expect(translateStatusTr("Thinking: model default")).toBe("Düşünme: model varsayılanı");
		expect(translateStatusTr("Plan: off")).toBe("Plan: kapalı");
		expect(translateStatusTr("Plan: on (plan.md)")).toBe("Plan: açık (plan.md)");
		expect(translateStatusTr("Login: waiting for anthropic callback")).toBe("Giriş: anthropic yanıtı bekleniyor");
		expect(translateStatusTr("Model: deepseek/v4")).toBe("Model: deepseek/v4");
		expect(translateStatusTr("Fast: off")).toBe("Fast: off");
	});

	it("wraps live descriptions and skips commands outside simple mode", () => {
		const effort = localizeSimpleCommandTr({
			name: "effort",
			description: "Set thinking effort",
			getAutocompleteDescription: () => "Thinking: low",
		});
		expect(effort.description).toBe("Düşünme seviyesini ayarla");
		expect(effort.getAutocompleteDescription?.()).toBe("Düşünme: düşük");

		const fast = { name: "fast", description: "Fast mode" };
		expect(localizeSimpleCommandTr(fast)).toBe(fast);
	});
});
