/**
 * PandaCode command palette: Ctrl+K on an empty composer lists the picker's slash
 * commands in a type-to-search selector. Choosing one runs it, or leaves `/name `
 * in the composer when the command needs an argument first.
 */
import type { SlashCommand } from "@oh-my-pi/pi-tui/autocomplete";
import type { HookSelectorOption } from "@oh-my-pi/pi-tui/overlays/hook-selector";

export const COMMAND_PALETTE_TITLE = "Komut paleti";

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

/** Palette label for a command; also the key {@link findPaletteCommand} resolves. */
export function paletteLabel(command: SlashCommand): string {
	return `/${command.name}`;
}

/** Selector rows for `commands`, first occurrence of a name winning, with live status descriptions. */
export function buildPaletteOptions(commands: readonly SlashCommand[]): HookSelectorOption[] {
	const seen = new Set<string>();
	const options: HookSelectorOption[] = [];
	for (const command of commands) {
		if (seen.has(command.name)) continue;
		seen.add(command.name);
		options.push({
			label: paletteLabel(command),
			description: command.getAutocompleteDescription?.() ?? command.description,
		});
	}
	return options;
}

/** The command a palette label names, first occurrence winning like {@link buildPaletteOptions}. */
export function findPaletteCommand(commands: readonly SlashCommand[], label: string): SlashCommand | undefined {
	return commands.find(command => paletteLabel(command) === label);
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
	return needsArgument
		? { text: `${paletteLabel(command)} `, submit: false }
		: { text: paletteLabel(command), submit: true };
}
