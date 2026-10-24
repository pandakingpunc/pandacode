import { afterAll, beforeAll, describe, expect, it } from "bun:test";
import { stripVTControlCharacters } from "node:util";
import { KeybindingsManager } from "@oh-my-pi/pi-tui/app-keybindings";
import { ShortcutBar, type ShortcutBarHost } from "@oh-my-pi/pi-tui/prompt/shortcut-bar";
import { setUiLanguage } from "@oh-my-pi/pi-tui/locale";
import { initTheme } from "@oh-my-pi/pi-tui/theme";
import { visibleWidth } from "@oh-my-pi/pi-tui";

function host(overrides: Partial<ShortcutBarHost> = {}): ShortcutBarHost {
	return {
		keybindings: KeybindingsManager.inMemory(),
		enabled: () => true,
		busy: () => false,
		...overrides,
	};
}

function text(bar: ShortcutBar, width = 200): string {
	return bar
		.render(width)
		.map(row => stripVTControlCharacters(row))
		.join("\n");
}

describe("ShortcutBar", () => {
	beforeAll(async () => {
		await initTheme(false);
		setUiLanguage("tr");
	});

	afterAll(() => {
		setUiLanguage("en");
	});

	it("speaks English when the interface is English", () => {
		setUiLanguage("en");
		try {
			const rendered = text(new ShortcutBar(host()));
			expect(rendered).toContain("commands");
			expect(rendered).not.toContain("komutlar");
		} finally {
			setUiLanguage("tr");
		}
	});

	it("lists the everyday gestures while idle", () => {
		const rendered = text(new ShortcutBar(host()));
		for (const label of ["komutlar", "model", "düşünme", "geçmiş", "çıkış"]) expect(rendered).toContain(label);
		expect(rendered).not.toContain("durdur");
	});

	it("switches to the stop gesture while the agent works", () => {
		const rendered = text(new ShortcutBar(host({ busy: () => true })));
		expect(rendered).toContain("durdur");
		expect(rendered).not.toContain("komutlar");
	});

	it("renders nothing when disabled", () => {
		expect(new ShortcutBar(host({ enabled: () => false })).render(80)).toEqual([]);
	});

	it("skips actions the user unbound", () => {
		const rendered = text(
			new ShortcutBar(host({ keybindings: KeybindingsManager.inMemory({ "app.model.select": [] }) })),
		);
		expect(rendered).not.toContain("model");
		expect(rendered).toContain("komutlar");
	});

	it("fits one row in a narrow terminal", () => {
		const rows = new ShortcutBar(host()).render(30);
		expect(rows).toHaveLength(1);
		expect(visibleWidth(rows[0]!)).toBeLessThanOrEqual(30);
	});
});
