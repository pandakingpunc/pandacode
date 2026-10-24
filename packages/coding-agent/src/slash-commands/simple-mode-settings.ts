/**
 * Settings declared by this domain (see `config/registry.ts`). Declaration order is the
 * settings-panel order; `config/all-settings.ts` registers every domain.
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
