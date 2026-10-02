# Product Sense packages

Root `SKILL.md` and `references/` are the shared canonical source. Codex continues to use that source with `agents/openai.yaml`. The Claude package contains identical instructions and references, with its own manifest in `packaging/claude/plugin.json`.

## Build and check

Requires Python 3 and, for native validation, Claude Code.

```sh
python3 -m unittest discover -s tests -v
python3 scripts/build_claude.py
claude plugin validate --json --strict dist/claude/product-sense
```

Outputs are `dist/claude/product-sense/` and `dist/claude/product-sense.zip`. Rebuilds replace these generated outputs. The ZIP has fixed timestamps and permissions, and contains only the manifest, entrypoint and Markdown references. Qualification evidence and Codex metadata stay outside it. Generated outputs are ignored by Git; the source and builder are tracked.

## Try in Claude Code

Load the generated folder for one session:

```sh
claude --plugin-dir ./dist/claude/product-sense
```

The explicit command is `/product-sense:product-sense`. Claude can also select it for ordinary product assessment requests. This uses Claude's [documented session-only plugin loading](https://code.claude.com/docs/en/plugins); it does not require marketplace installation.

Version `0.1.1` adds Radical Candor's supporting-source attribution; runtime critique instructions remain unchanged. The baseline behaviour check and decision to avoid additional rules are recorded in `qualification/run-5/`. Native test results for version `0.1.0` and their limitations remain in `qualification/run-4/`; they do not qualify this archive. Packaging and local tests do not establish acceptance on claude.ai, Cowork or an OpenAI plugin surface. Marketplace submission and MCP/UI extensions remain separate work.
