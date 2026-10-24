/**
 * PandaCode simple mode. The slash-command picker shows only everyday builtins;
 * hidden builtins stay registered, so typing one still runs it. `/gelismis`
 * toggles the full list; the setting lives in `./simple-mode-settings`.
 */
import { localize } from "@oh-my-pi/pi-tui/locale";
import { clearSubmittedText } from "./helpers/draft";
import { cfgSimpleMode } from "./simple-mode-settings";
import type { SlashCommand } from "@oh-my-pi/pi-tui/autocomplete";
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

/** Turkish picker copy for the simple-mode builtins (`/gelismis` is Turkish already). */
const SIMPLE_MODE_DESCRIPTIONS_TR: Readonly<Record<string, string>> = {
	new: "Yeni oturum başlat",
	resume: "Önceki bir oturuma dön",
	model: "Model seç",
	effort: "Düşünme seviyesini ayarla",
	plan: "Plan modunu aç/kapat (ajan önce plan yapar)",
	compact: "Konuşmayı özetleyip bağlamı küçült",
	retry: "Son başarısız adımı yeniden dene",
	copy: "Konuşmadan metin ya da kod kopyala",
	settings: "Ayarlar menüsünü aç",
	setup: "Sağlayıcı kurulumunu aç",
	login: "Bir sağlayıcıya giriş yap",
	logout: "Bir sağlayıcıdan çıkış yap",
	hotkeys: "Tüm klavye kısayollarını göster",
	usage: "Sağlayıcı kullanımını ve limitlerini göster",
	exit: "PandaCode'dan çık",
};

const THINKING_LEVELS_TR: Readonly<Record<string, string>> = {
	inherit: "devral",
	off: "kapalı",
	minimal: "minimum",
	low: "düşük",
	medium: "orta",
	high: "yüksek",
	xhigh: "çok yüksek",
	max: "en yüksek",
	"model default": "model varsayılanı",
};

/** Turkish for the live status descriptions of the simple-mode builtins, first match wins. */
const STATUS_TR: ReadonlyArray<readonly [RegExp, (...groups: string[]) => string]> = [
	[/^Model: none selected$/, () => "Model: seçili değil"],
	[/^Thinking: (.+)$/, level => `Düşünme: ${THINKING_LEVELS_TR[level] ?? level}`],
	[/^Plan: disabled in settings$/, () => "Plan: ayarlarda kapalı"],
	[/^Plan: blocked by goal mode$/, () => "Plan: hedef modu engelliyor"],
	[/^Plan: on(.*)$/, rest => `Plan: açık${rest}`],
	[/^Plan: off$/, () => "Plan: kapalı"],
	[/^Login: choose provider$/, () => "Giriş: sağlayıcı seç"],
	[/^Login: waiting for (.+) callback$/, provider => `Giriş: ${provider} yanıtı bekleniyor`],
];

/** Turkish for one live status description; unknown text passes through. */
export function translateStatusTr(text: string): string {
	for (const [pattern, render] of STATUS_TR) {
		const match = pattern.exec(text);
		if (match) return render(...match.slice(1));
	}
	return text;
}

/** `command` with Turkish picker copy when it is a simple-mode builtin; other commands are returned as is. */
export function localizeSimpleCommandTr<T extends SlashCommand>(command: T): T {
	const description = SIMPLE_MODE_DESCRIPTIONS_TR[command.name];
	if (description === undefined) return command;
	const live = command.getAutocompleteDescription;
	return {
		...command,
		description,
		getAutocompleteDescription: live
			? () => {
					const text = live();
					return text === undefined ? undefined : translateStatusTr(text);
				}
			: undefined,
	};
}

export const SIMPLE_MODE_SLASH_COMMANDS: ReadonlyArray<SlashCommandSpec> = [
	{
		name: "gelismis",
		aliases: ["advanced"],
		icon: "settings",
		get description() {
			return localize("Show or hide advanced commands (simple mode)", "Gelişmiş komutları göster/gizle (sade mod)");
		},
		handleTui: (_command, runtime) => {
			const simple = !cfgSimpleMode.get(runtime.ctx.settings);
			cfgSimpleMode.set(runtime.ctx.settings, simple);
			runtime.ctx.showStatus(
				simple
					? localize(
							"Simple mode on: listing everyday commands only",
							"Sade mod açık: yalnız günlük komutlar listeleniyor",
						)
					: localize("Advanced mode: listing every command", "Gelişmiş mod: tüm komutlar listeleniyor"),
			);
			clearSubmittedText(runtime);
		},
	},
];
