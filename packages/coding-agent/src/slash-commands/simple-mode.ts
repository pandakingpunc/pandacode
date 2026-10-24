/**
 * PandaCode simple mode. The slash-command picker shows only everyday builtins;
 * hidden builtins stay registered, so typing one still runs it. `/gelismis`
 * toggles the full list; the setting lives in `./simple-mode-settings`.
 */
import { clearSubmittedText } from "./helpers/draft";
import { cfgSimpleMode } from "./simple-mode-settings";
import type { SlashCommandSpec } from "./types";

/** Builtins the picker keeps in simple mode, in no particular order. */
export const SIMPLE_MODE_COMMANDS: ReadonlySet<string> = new Set([
	"new",
	"resume",
	"model",
	"effort",
	"plan",
	"compact",
	"retry",
	"copy",
	"settings",
	"setup",
	"login",
	"logout",
	"hotkeys",
	"usage",
	"exit",
	"gelismis",
]);

export const SIMPLE_MODE_SLASH_COMMANDS: ReadonlyArray<SlashCommandSpec> = [
	{
		name: "gelismis",
		aliases: ["advanced"],
		icon: "settings",
		description: "Gelişmiş komutları göster/gizle (sade mod)",
		handleTui: (_command, runtime) => {
			const simple = !cfgSimpleMode.get(runtime.ctx.settings);
			cfgSimpleMode.set(runtime.ctx.settings, simple);
			runtime.ctx.showStatus(
				simple ? "Sade mod açık: yalnız günlük komutlar listeleniyor" : "Gelişmiş mod: tüm komutlar listeleniyor",
			);
			clearSubmittedText(runtime);
		},
	},
];
