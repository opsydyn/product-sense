# Product Sense packages

`SKILL.md` and `references/` are the canonical source for both hosts. Claude uses `packaging/claude/plugin.json`; Codex uses `agents/openai.yaml` and the icon. Version `0.1.2` is an unpublished beta candidate.

## Build and check

Requires Python 3.9 or newer, and Claude Code for native validation.

```sh
python3 -m unittest discover -s tests -v
python3 scripts/build_claude.py --format claude
python3 scripts/build_claude.py --format codex
```

Each build prints its ZIP path. Defaults are in the system temporary directory under `product-sense-release/claude/` or `product-sense-release/codex/`. Each destination contains a generated `product-sense/` folder and `product-sense.zip`.

Use `--output-dir /absolute/path/outside-this-checkout` for persistent staging. The builder rejects output inside the installed source tree and destinations that could replace source. Keep the two formats in separate destinations. Rebuilds replace the generated folder and ZIP. Temporary output may be cleared by the operating system; copy verified assets to your release destination before publishing.

Both ZIPs have fixed timestamps, permissions and ordered members. They exclude Git state, qualification evidence and authoring documents. Claude contains the manifest and shared skill/references; Codex has a top-level `product-sense/` folder containing the shared payload, UI metadata and icon. Both include the exact root `LICENSE` text when the owner supplies it. Tests check exact canonical bytes, reproducibility, missing inputs, symlink rejection and output isolation.

Validate the generated Claude folder (the printed ZIP's sibling folder):

```sh
claude plugin validate --json --strict /path/to/output/claude/product-sense
```

## Installation checks

Install a single Codex skill folder as described in [README.md](README.md). Confirm `$product-sense` appears, then test an approved narrow-copy request and an ordinary capped assessment. Inspect native instruction/reference reads. Never install the Claude package beneath the canonical Codex skill.

For Claude Code, load the external generated folder with `claude --plugin-dir /path/to/plugin`. Test `/product-sense:product-sense`, ordinary implicit selection, reference loading, the requested word cap and fixed appetite. [Claude session loading and distribution](https://code.claude.com/docs/en/plugin-marketplaces)

Run 7 confirmed selection and invocation but failed full implicit compliance. Runs 8 and 9 retain baseline and intermediate-candidate failures. [Run 10](qualification/run-10/report.md) passed all declared final native checks; an elapsed-schedule ambiguity remains. These CLI observations do not establish other-surface support or product value.

## Publication preparation

1. Include the owner's chosen licence, accurate release notes and limitations.
2. Build both formats in separate external destinations; retain hashes and validate the manifest and exact archived source.
3. Qualify the exact candidate, review failures, and commit source and evidence before tagging.
4. Upload verified assets to the chosen distribution destination. This checkout has no Git remote; do not invent its URL or claim publication.
5. A Claude team marketplace is optional. Create and validate its catalogue and test installation before sharing it; direct ZIP sharing needs no marketplace.
6. OpenAI's skills-only submission accepts the Claude-format ZIP and converts its manifest. Test the imported skill, complete listing/review fields, resolve scan findings, submit, then publish after approval. [Official submission guidance](https://developers.openai.com/plugins/guides/submit-claude-plugin)

An MCP server or UI extension is not required. Directory acceptance, a fresh desktop picker, claude.ai and Cowork remain separate from local CLI qualification.
