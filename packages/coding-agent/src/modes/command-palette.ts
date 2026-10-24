/**
 * PandaCode command palette: Ctrl+K on an empty composer lists the picker's slash
 * commands in a type-to-search selector. Choosing one runs it, or leaves `/name `
 * in the composer when the command needs an argument first.
 */
import type { SlashCommand } from "@oh-my-pi/pi-tui/autocomplete";
import { localize } from "@oh-my-pi/pi-tui/locale";
import type { HookSelectorOption } from "@oh-my-pi/pi-tui/overlays/hook-selector";

export function commandPaletteTitle(): string {
	return localize("Command palette", "Komut paleti");
}

/** Builtin metadata the picker entries carry beyond {@link SlashCommand}. */
interface PaletteCommand extends SlashCommand {
	subcommands?: readonly unknown[];
	subcommandOptional?: boolean;
}

/** What choosing a command does: the composer text, and whether to submit it. */
export interface PaletteAction {
	text: string;
	submit: boolean;
}

/** Selector rows plus the command each row label stands for. */
export interface Palette {
	options: HookSelectorOption[];
	commandFor(label: string): SlashCommand | undefined;
}

/** Columns between the widest command name and its description. */
const DESCRIPTION_GAP = 2;

/**
 * One row per command, first occurrence of a name winning: `/name` padded to the
 * widest name, then its live description. Rows carry the description inline (not
 * as a selector description) because a long list collapses descriptions away.
 */
export function buildPalette(commands: readonly SlashCommand[]): Palette {
	const unique: SlashCommand[] = [];
	const seen = new Set<string>();
	for (const command of commands) {
		if (seen.has(command.name)) continue;
		seen.add(command.name);
		unique.push(command);
	}
	const nameWidth = Math.max(0, ...unique.map(command => command.name.length + 1));
	const byLabel = new Map<string, SlashCommand>();
	const options = unique.map(command => {
		const name = `/${command.name}`;
		const description = (command.getAutocompleteDescription?.() ?? command.description ?? "").trim();
		const label = description ? `${name.padEnd(nameWidth + DESCRIPTION_GAP)}${description}` : name;
		byLabel.set(label, command);
		return { label };
	});
	return { options, commandFor: label => byLabel.get(label) };
}

/**
 * Run the command as is, unless it cannot run bare: required subcommands, or an
 * argument hint in `<required>` form. Those land in the composer for the argument.
 */
export function paletteAction(command: SlashCommand): PaletteAction {
	const { subcommands, subcommandOptional, argumentHint } = command as PaletteCommand;
	const needsArgument =
		(subcommands !== undefined && subcommands.length > 0 && subcommandOptional !== true) ||
		argumentHint?.trimStart().startsWith("<") === true;
	const name = `/${command.name}`;
	return needsArgument ? { text: `${name} `, submit: false } : { text: name, submit: true };
}
