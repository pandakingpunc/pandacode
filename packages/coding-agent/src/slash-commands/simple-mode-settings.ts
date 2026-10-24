/**
 * Settings declared by this domain (see `config/registry.ts`). Declaration order is the
 * settings-panel order; `config/all-settings.ts` registers every domain.
 * PandaCode's own settings live here, under the "PandaCode" group.
 */
import { register } from "../config/registry";

/** PandaCode simple mode: the slash-command picker lists only everyday builtins. */
export const cfgSimpleMode = register({
	id: "pandacode.simpleMode",
	type: "boolean",
	default: true,
	ui: {
		tab: "interaction",
		group: "PandaCode",
		label: "Sade Mod",
		description: "Komut listesinde yalnız günlük komutları göster; /gelismis tüm listeyi açıp kapatır",
	},
});

/** PandaCode shortcut bar: a dim row of everyday keys under the composer. */
export const cfgShortcutBar = register({
	id: "pandacode.shortcutBar",
	type: "boolean",
	default: true,
	ui: {
		tab: "interaction",
		group: "PandaCode",
		label: "Kısayol Çubuğu",
		description: "Yazı alanının altında günlük kısayolları göster",
	},
});
