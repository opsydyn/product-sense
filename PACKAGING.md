# Product Sense packages

`plugins/product-sense/` is the canonical plugin folder and the only source for both hosts:

- `.claude-plugin/plugin.json`, `README.md` and `LICENSE`: the Claude plugin manifest, listing description and licence.
- `skills/product-sense/`: the skill (`SKILL.md`, `references/`) plus Codex metadata (`agents/openai.yaml`, `assets/icon.svg`). This folder is a complete Codex skill on its own.

The root `.claude-plugin/marketplace.json` lists the plugin, so the repository is also a Claude marketplace named `opsydyn`. Version `0.2.0` is the first public release candidate.

## Build and check

Requires Python 3.9 or newer, and Claude Code for native validation.

```sh
python3 -m unittest discover -s tests -v
python3 scripts/build_claude.py --format claude
python3 scripts/build_claude.py --format codex
```

Each build prints its ZIP path. Defaults are in the system temporary directory under `product-sense-release/claude/` or `product-sense-release/codex/`. Each destination contains a generated `product-sense/` folder and `product-sense.zip`.

Use `--output-dir /absolute/path/outside-this-checkout` for persistent staging. The builder rejects output inside the installed source tree and destinations that could replace source. Keep the two formats in separate destinations. Rebuilds replace the generated folder and ZIP. Temporary output may be cleared by the operating system; copy verified assets to your release destination before publishing.

Both ZIPs have fixed timestamps, permissions and ordered members, and contain nothing from outside the plugin folder. The Claude ZIP is exactly the plugin folder, minus operating-system files such as `.DS_Store`. The Codex ZIP has a top-level `product-sense/` folder holding the skill folder and the plugin's `LICENSE`. A missing licence fails both builds. Tests check exact bytes, reproducibility, missing inputs, symlink rejection and output isolation.

Validate the plugin and the marketplace:

```sh
claude plugin validate --strict plugins/product-sense
claude plugin validate --strict .
```

## Installation checks

Install a single Codex skill folder as described in [README.md](README.md). Confirm `$product-sense` appears, then test an approved narrow-copy request and an ordinary capped assessment. Inspect native instruction/reference reads. Never install the Claude package beneath the canonical Codex skill.

For Claude Code, load `claude --plugin-dir plugins/product-sense`, or add the local marketplace with `claude plugin marketplace add ./` and install `product-sense@opsydyn`. Test `/product-sense:product-sense`, ordinary implicit selection, reference loading, the requested word cap and fixed appetite. [Claude session loading and distribution](https://code.claude.com/docs/en/plugin-marketplaces)

Run 7 confirmed selection and invocation but failed full implicit compliance. Runs 8 and 9 retain baseline and intermediate-candidate failures. [Run 10](qualification/run-10/report.md) passed all declared final native checks; an elapsed-schedule ambiguity remains. These CLI observations do not establish other-surface support or product value.

## Publication

**Own marketplace (live on push).** Users run `claude plugin marketplace add opsydyn/product-sense` and `claude plugin install product-sense@opsydyn`. Raise `version` in `plugin.json` with every release, or users keep the old copy.

**Anthropic's directory (reviewed).** Submit from [claude.ai/directory/manage](https://claude.ai/directory/manage): **Submit new** → **Plugin bundle**, repository `opsydyn/product-sense`, plugin path `plugins/product-sense`. Select **Validate** and fix anything marked **Blocking**, then complete the data-handling and compliance steps and submit for review. The plugin reads no personal data, sends nothing and keeps nothing. Work through the [pre-submission checklist](https://claude.com/docs/plugins/pre-submission-checklist) first; the portal checks more than `claude plugin validate`. The generic name may be held for a reviewer. [Submission guide](https://claude.com/docs/plugins/submit)

**Codex.** OpenAI's skills-only submission accepts the Claude-format ZIP and converts its manifest. [Official submission guidance](https://developers.openai.com/plugins/guides/submit-claude-plugin)

Before each release: run the tests, validate both manifests, install from the local marketplace, update the changelog, and keep qualification evidence for the exact candidate.
