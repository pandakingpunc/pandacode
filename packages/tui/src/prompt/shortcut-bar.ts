/**
 * PandaCode shortcut bar: one dim row under the composer listing the keys that
 * matter right now, so the everyday gestures are visible without `/hotkeys`.
 * Idle shows the composer gestures; while the agent works it shows how to stop it.
 * Keys come from the live keybindings, so user rebinds show up here too. The bar
 * always takes exactly one row while enabled, so the layout never jumps under it.
 */
import { type AppKeybinding, formatKeyHint, type KeybindingsManager } from "../app-keybindings";
import { theme } from "../theme/theme";
import type { Component } from "../tui";
import { truncateToWidth } from "../utils";

/** Live state the bar reads on every render. */
export interface ShortcutBarHost {
	keybindings: KeybindingsManager;
	/** The bar is turned on in settings. */
	enabled(): boolean;
	/** The agent is streaming or otherwise busy. */
	busy(): boolean;
}

/** A shortcut entry: a bound action, or a literal key for gestures with no binding. */
type ShortcutEntry = { action: AppKeybinding; label: string } | { key: string; label: string };

const IDLE_SHORTCUTS: readonly ShortcutEntry[] = [
	{ key: "/", label: "komutlar" },
	{ action: "app.model.select", label: "model" },
	{ action: "app.thinking.cycle", label: "düşünme" },
	{ action: "app.history.search", label: "geçmiş" },
	{ action: "app.exit", label: "çıkış" },
];

const BUSY_SHORTCUTS: readonly ShortcutEntry[] = [
	{ action: "app.interrupt", label: "durdur" },
	{ action: "app.tools.expand", label: "ayrıntı" },
];

const SEPARATOR = "  ·  ";

export class ShortcutBar implements Component {
	#cacheKey: string | undefined;
	#cacheRows: readonly string[] = [];

	constructor(private readonly host: ShortcutBarHost) {}

	render(width: number): readonly string[] {
		if (!this.host.enabled()) return [];
		const entries = this.host.busy() ? BUSY_SHORTCUTS : IDLE_SHORTCUTS;
		const parts: string[] = [];
		for (const entry of entries) {
			let key: string;
			if ("key" in entry) {
				key = entry.key;
			} else {
				const bound = this.host.keybindings.getKeys(entry.action)[0];
				// An action the user unbound has nothing to teach.
				if (!bound) continue;
				key = formatKeyHint(bound);
			}
			parts.push(`${theme.fg("accent", key)} ${theme.fg("dim", entry.label)}`);
		}
		const line = ` ${parts.join(theme.fg("dim", SEPARATOR))}`;
		const cacheKey = `${width}\0${line}`;
		if (cacheKey !== this.#cacheKey) {
			this.#cacheKey = cacheKey;
			this.#cacheRows = parts.length === 0 ? [] : [truncateToWidth(line, width)];
		}
		return this.#cacheRows;
	}

	invalidate(): void {
		this.#cacheKey = undefined;
	}
}
