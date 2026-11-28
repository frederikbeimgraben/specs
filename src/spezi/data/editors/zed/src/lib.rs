//! The Zed extension of the spezi kit: it starts `spezi lsp`.

use zed_extension_api::{self as zed, LanguageServerId, Result, Worktree};

const SERVER_JSON: &str = ".zed/spezi/server.json";

struct Specs;

/// Returns the command in `.zed/spezi/server.json`, written by `spezi setup-ide zed`.
fn configured(worktree: &Worktree) -> Option<String> {
    worktree
        .read_text_file(SERVER_JSON)
        .ok()
        .and_then(|text| serde_json::from_str::<serde_json::Value>(&text).ok())
        .and_then(|value| value.get("command")?.as_str().map(str::to_owned))
}

impl zed::Extension for Specs {
    fn new() -> Self {
        Specs
    }

    fn language_server_command(
        &mut self,
        _language_server_id: &LanguageServerId,
        worktree: &Worktree,
    ) -> Result<zed::Command> {
        worktree
            .which("spezi")
            .or_else(|| configured(worktree))
            .map(|command| zed::Command {
                command,
                args: vec!["lsp".to_owned()],
                env: worktree.shell_env(),
            })
            .ok_or_else(|| format!("spezi is not on PATH, and {SERVER_JSON} names no command"))
    }
}

zed::register_extension!(Specs);
