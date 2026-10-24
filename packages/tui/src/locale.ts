/**
 * PandaCode interface language. The coding agent's `pandacode.language` setting
 * drives it (Turkish by default); the TUI default stays English, so code and
 * tests that never bind settings render exactly as upstream omp does.
 */
export type UiLanguage = "tr" | "en";

let current: UiLanguage = "en";

export function setUiLanguage(language: UiLanguage): void {
	current = language;
}

export function getUiLanguage(): UiLanguage {
	return current;
}

/** `tr` while the interface is Turkish, `en` otherwise. */
export function localize(en: string, tr: string): string {
	return current === "tr" ? tr : en;
}
