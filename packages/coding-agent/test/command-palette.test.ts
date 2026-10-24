import { afterEach, beforeAll, beforeEach, describe, expect, it } from "bun:test";
import * as path from "node:path";
import { Agent } from "@oh-my-pi/pi-agent-core";
import { ModelRegistry } from "@oh-my-pi/pi-coding-agent/config/model-registry";
import { resetSettingsForTest, Settings } from "@oh-my-pi/pi-coding-agent/config/settings";
import {
	buildPaletteOptions,
	COMMAND_PALETTE_TITLE,
	findPaletteCommand,
	paletteAction,
} from "@oh-my-pi/pi-coding-agent/modes/command-palette";
import { InteractiveMode } from "@oh-my-pi/pi-coding-agent/modes/interactive-mode";
import { AgentSession } from "@oh-my-pi/pi-coding-agent/session/agent-session";
import { AuthStorage } from "@oh-my-pi/pi-coding-agent/session/auth-storage";
import { SessionManager } from "@oh-my-pi/pi-coding-agent/session/session-manager";
import { cfgSimpleMode } from "@oh-my-pi/pi-coding-agent/slash-commands/simple-mode-settings";
import type { SlashCommand } from "@oh-my-pi/pi-tui/autocomplete";
import { Composer } from "@oh-my-pi/pi-tui/prompt/composer";
import { initTheme } from "@oh-my-pi/pi-tui/theme";
import { TempDir } from "@oh-my-pi/pi-utils";
import { VirtualTerminal } from "../../tui/test/virtual-terminal";

const CTRL_K = "\x0b";

describe("command palette helpers", () => {
	const commands: SlashCommand[] = [
		{ name: "model", description: "Select model", getAutocompleteDescription: () => "Model: test" },
		{ name: "hotkeys", description: "Show all keyboard shortcuts" },
		{ name: "hotkeys", description: "Duplicate from a hook" },
		{ name: "mcp", description: "Manage MCP servers", subcommands: [{ name: "list" }] } as SlashCommand,
		{
			name: "fast",
			description: "Fast mode",
			subcommands: [{ name: "on" }],
			subcommandOptional: true,
		} as SlashCommand,
		{ name: "review", description: "Review a file", argumentHint: "<path>" },
	];

	it("lists each command once with its live description", () => {
		const options = buildPaletteOptions(commands);
		expect(options.map(option => option.label)).toEqual(["/model", "/hotkeys", "/mcp", "/fast", "/review"]);
		expect(options[0]?.description).toBe("Model: test");
		expect(options[1]?.description).toBe("Show all keyboard shortcuts");
		expect(findPaletteCommand(commands, "/hotkeys")?.description).toBe("Show all keyboard shortcuts");
	});

	it("runs bare commands and leaves argument-taking ones in the composer", () => {
		const action = (name: string) => paletteAction(commands.find(command => command.name === name)!);
		expect(action("model")).toEqual({ text: "/model", submit: true });
		expect(action("fast")).toEqual({ text: "/fast", submit: true });
		expect(action("mcp")).toEqual({ text: "/mcp ", submit: false });
		expect(action("review")).toEqual({ text: "/review ", submit: false });
	});
});

function screen(term: VirtualTerminal): string[] {
	return term.getViewport().map(row => Bun.stripANSI(row).trimEnd());
}

describe("command palette on a real terminal core", () => {
	let tempDir: TempDir;
	let authStorage: AuthStorage;
	let session: AgentSession;
	let mode: InteractiveMode;
	let term: VirtualTerminal;

	beforeAll(() => {
		initTheme();
	});

	beforeEach(async () => {
		resetSettingsForTest();
		tempDir = TempDir.createSync("@pi-command-palette-");
		await Settings.init({ inMemory: true, cwd: tempDir.path() });
		authStorage = await AuthStorage.create(path.join(tempDir.path(), "testauth.db"));
		const modelRegistry = new ModelRegistry(authStorage);
		const model = modelRegistry.find("anthropic", "claude-sonnet-4-5");
		if (!model) throw new Error("Expected claude-sonnet-4-5 to exist in registry");
		session = new AgentSession({
			agent: new Agent({ initialState: { model, systemPrompt: ["Test"], tools: [], messages: [] } }),
			sessionManager: SessionManager.create(tempDir.path(), tempDir.path()),
			settings: Settings.isolated(),
			modelRegistry,
		});
		term = new VirtualTerminal(120, 32);
		mode = new InteractiveMode(
			session,
			"test",
			undefined,
			() => {},
			undefined,
			undefined,
			undefined,
			new Composer({ terminal: term }),
		);
		await mode.init({ suppressWelcomeIntro: true });
		void mode.getUserInput();
		await term.waitForRender();
	});

	afterEach(async () => {
		mode?.stop();
		await session?.dispose();
		authStorage?.close();
		tempDir?.removeSync();
		resetSettingsForTest();
	});

	it("opens on an empty composer, filters by typing and runs the chosen command", async () => {
		term.sendInput(CTRL_K);
		await term.waitForRender(() => screen(term).some(row => row.includes(COMMAND_PALETTE_TITLE)));

		term.sendInput("gelismis");
		await term.waitForRender(() => screen(term).some(row => row.includes("/gelismis")));
		term.sendInput("\r");
		await term.waitForRender(() => screen(term).some(row => row.includes("Gelişmiş mod")));

		expect(cfgSimpleMode.get(mode.settings)).toBe(false);
		expect(screen(term).some(row => row.includes(COMMAND_PALETTE_TITLE))).toBe(false);
		expect(mode.editor.getText()).toBe("");
	});

	it("closes on Esc without touching the composer", async () => {
		term.sendInput(CTRL_K);
		await term.waitForRender(() => screen(term).some(row => row.includes(COMMAND_PALETTE_TITLE)));
		term.sendInput("\x1b");
		await term.waitForRender(() => !screen(term).some(row => row.includes(COMMAND_PALETTE_TITLE)));
		expect(mode.ui.getFocused()).toBe(mode.editor);
	});

	it("keeps ctrl+k as delete-to-line-end while a draft is typed", async () => {
		term.sendInput("merhaba dünya");
		await term.waitForRender(() => mode.editor.getText() === "merhaba dünya");
		term.sendInput("\x1b[D\x1b[D\x1b[D\x1b[D\x1b[D");
		term.sendInput(CTRL_K);
		await term.waitForRender(() => mode.editor.getText() === "merhaba ");
		expect(screen(term).some(row => row.includes(COMMAND_PALETTE_TITLE))).toBe(false);
	});
});
