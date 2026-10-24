import { afterEach, beforeAll, describe, expect, it, vi } from "bun:test";
import { KeybindingsManager } from "@oh-my-pi/pi-tui/app-keybindings";
import { getUiLanguage, localize, setUiLanguage } from "@oh-my-pi/pi-tui/locale";
import { HookSelectorComponent } from "@oh-my-pi/pi-tui/overlays/hook-selector";
import { resolveComposerHint } from "@oh-my-pi/pi-tui/prompt/composer-hints";
import { renderWelcomeTip, WelcomeComponent } from "@oh-my-pi/pi-tui/prompt/welcome";
import { initTheme } from "@oh-my-pi/pi-tui/theme";
import tipsTrText from "../src/prompt/tips-tr.txt" with { type: "text" };

const plain = (rows: readonly string[]) => rows.map(row => Bun.stripANSI(row)).join("\n");

describe("PandaCode interface language", () => {
	beforeAll(async () => {
		await initTheme(false);
	});

	afterEach(() => {
		setUiLanguage("en");
		vi.restoreAllMocks();
	});

	it("defaults to English so upstream surfaces are unchanged", () => {
		expect(getUiLanguage()).toBe("en");
		expect(localize("Search", "Ara")).toBe("Search");
		setUiLanguage("tr");
		expect(localize("Search", "Ara")).toBe("Ara");
	});

	it("translates the empty-composer hint", () => {
		const hint = (language: "en" | "tr") => {
			setUiLanguage(language);
			return Bun.stripANSI(
				resolveComposerHint({
					runningAgents: 0,
					focusedOnAgent: false,
					conversationStarted: false,
					keybindings: KeybindingsManager.inMemory(),
					uses: () => 0,
				}) ?? "",
			);
		};
		expect(hint("en")).toContain("to change thinking effort");
		expect(hint("tr")).toContain("düşünme seviyesini değiştir");
	});

	it("translates the selector chrome", () => {
		setUiLanguage("tr");
		const selector = new HookSelectorComponent(
			"Seç",
			["bir", "iki"],
			() => {},
			() => {},
		);
		const rendered = plain(selector.render(80));
		expect(rendered).toContain("gez");
		expect(rendered).toContain("vazgeç");
		expect(rendered).not.toContain("navigate");
	});

	it("picks Turkish tips with every key placeholder resolved", () => {
		setUiLanguage("tr");
		vi.spyOn(Math, "random").mockReturnValue(0.5);
		const tip = new WelcomeComponent("1.0.0").tip ?? "";
		const tips = tipsTrText
			.split("\n")
			.map(line => line.trim())
			.filter(line => line.length > 0);
		expect(tips).toContain(tip);
		for (const line of tips) {
			const rendered = plain(renderWelcomeTip(line, 200));
			expect(rendered.startsWith("İpucu: ")).toBe(true);
			expect(rendered).not.toContain("{key:");
		}
	});
});
