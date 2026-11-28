/**
 * The VS Code extension of the spezi kit: it starts `spezi lsp`.
 *
 * The extension starts `spezi` from PATH. When PATH has no `spezi`, it starts the command in
 * `.vscode/spezi/server.json`, which `spezi setup-ide code` writes.
 */

import { accessSync, constants, readFileSync } from "node:fs";
import { delimiter, join } from "node:path";
import { type ExtensionContext, workspace } from "vscode";
import {
  type DocumentSelector,
  LanguageClient,
  type LanguageClientOptions,
  type ServerOptions,
} from "vscode-languageclient/node";

/** The content of `.vscode/spezi/server.json`. */
interface Server {
  readonly command: string;
  readonly suffixes: readonly string[];
}

let client: LanguageClient | undefined;

/**
 * Return True when a file can run.
 *
 * @param path - The file.
 * @returns True for a file that runs.
 */
const runs = (path: string): boolean => {
  try {
    accessSync(path, constants.X_OK);
    return true;
  } catch {
    return false;
  }
};

/**
 * Return the path of `spezi` on PATH.
 *
 * @returns The path, or undefined.
 */
const onPath = (): string | undefined =>
  (process.env.PATH ?? "")
    .split(delimiter)
    .filter((folder) => folder !== "")
    .map((folder) => join(folder, "spezi"))
    .find(runs);

/**
 * Return the content of `server.json`, or the defaults when it is missing.
 *
 * @param root - The root of the workspace.
 * @returns The command and the suffixes.
 */
const server = (root: string): Server => {
  try {
    return JSON.parse(readFileSync(join(root, ".vscode", "spezi", "server.json"), "utf8")) as Server;
  } catch {
    return { command: "spezi", suffixes: [] };
  }
};

/**
 * Return the files that the server serves: the specs and the files with the suffixes.
 *
 * @param suffixes - The suffixes of the code.
 * @returns The selector.
 */
const selector = (suffixes: readonly string[]): DocumentSelector => [
  { scheme: "file", pattern: "**/specs/**/*.md" },
  ...suffixes.map((suffix) => ({ scheme: "file", pattern: `**/*${suffix}` })),
];

/**
 * Start the language server for the first folder of the workspace.
 *
 * @param context - The context of the extension.
 */
export const activate = async (context: ExtensionContext): Promise<void> => {
  const root = workspace.workspaceFolders?.[0]?.uri.fsPath;
  if (root === undefined) {
    return;
  }
  const config = server(root);
  const serverOptions: ServerOptions = {
    command: onPath() ?? config.command,
    args: ["lsp"],
    options: { cwd: root },
  };
  const clientOptions: LanguageClientOptions = { documentSelector: selector(config.suffixes) };
  client = new LanguageClient("spezi", "spezi", serverOptions, clientOptions);
  context.subscriptions.push(client);
  await client.start();
};

/** Stop the language server. */
export const deactivate = async (): Promise<void> => {
  await client?.stop();
};
