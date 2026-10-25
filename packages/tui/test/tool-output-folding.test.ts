import { afterEach, beforeAll, describe, expect, it } from "bun:test";
import { ToolExecutionComponent } from "../src/chat/tool-execution";
import { setUiLanguage } from "../src/locale";
import { formatOutputPaneLines } from "../src/render/output-pane";
import { DEFAULT_TERMINAL_PREVIEW_LINES, getToolPreviewLines, setToolPreviewLines } from "../src/render/render-utils";
import { getThemeByName, setThemeInstance } from "../src/theme";
import type { Theme } from "../src/theme/theme";

const ui = { requestRender: () => {}, requestComponentRender: () => {}, resetDisplay: () => {} };
const OUTPUT = Array.from({ length: 30 }, (_, i) => `line-${i + 1}`).join("\n");

/** Render a settled `bash` card whose output is {@link OUTPUT}. */
function renderBashCard(expanded = false): string {
	const tool = new ToolExecutionComponent("bash", { command: "seq 30" }, {}, undefined, ui);
	try {
		tool.updateResult({ content: [{ type: "text", text: OUTPUT }], details: {} }, false);
		tool.setExpanded(expanded);
		return Bun.stripANSI(tool.render(100).join("\n"));
	} finally {
		tool.dispose();
	}
}

const shownLines = (card: string) => card.match(/line-\d+/g) ?? [];

describe("PandaCode tool output folding", () => {
	let theme: Theme;

	beforeAll(async () => {
		const dark = await getThemeByName("dark");
		if (!dark) throw new Error("dark theme missing");
		setThemeInstance(dark);
		theme = dark;
	});

	afterEach(() => {
		setToolPreviewLines(DEFAULT_TERMINAL_PREVIEW_LINES);
		setUiLanguage("en");
	});

	it("keeps upstream's preview size by default", () => {
		expect(getToolPreviewLines()).toBe(DEFAULT_TERMINAL_PREVIEW_LINES);
		expect(shownLines(renderBashCard())).toHaveLength(DEFAULT_TERMINAL_PREVIEW_LINES);
	});

	it("folds a bash card to the configured tail and expands it in full", () => {
		setToolPreviewLines(3);
		expect(shownLines(renderBashCard())).toEqual(["line-28", "line-29", "line-30"]);
		expect(shownLines(renderBashCard(true))).toHaveLength(30);
	});

	it("labels the folded card in Turkish", () => {
		setUiLanguage("tr");
		setToolPreviewLines(3);
		const card = renderBashCard();
		expect(card).toContain("Çıktı");
		expect(card).toContain("30 satırın son 3 satırı");
		expect(card).toContain(": Aç");
		expect(card).not.toContain("Expand");
	});

	it("keeps the English hidden-line label for upstream", () => {
		const lines = Array.from({ length: 5 }, (_, i) => `r${i}`);
		const tail = formatOutputPaneLines({ lines, expanded: false, collapsedMaxLines: 2, edge: "tail" }, theme);
		expect(Bun.stripANSI(tail.lines[0] ?? "")).toContain("3 earlier lines, showing 2 of 5");
		setUiLanguage("tr");
		const head = formatOutputPaneLines({ lines, expanded: false, collapsedMaxLines: 2 }, theme);
		expect(Bun.stripANSI(head.lines.at(-1) ?? "")).toContain("3 satır daha");
	});
});
