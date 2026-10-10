# Product Sense

Turn an ambiguous product request into a defensible decision and a bounded next step.

Product Sense is a provider-neutral skill for product and engineering teams working with coding agents. It helps assess ideas, shape work to a fixed appetite, review user journeys and distinguish evidence from hypotheses. Its four pillars are user capability, understandable design, continuous discovery and coherent strategy. See the [source map](references/canon.md).

## Status

Version **0.1.2 is an unpublished beta candidate** for Codex and Claude Code. Both use identical canonical instructions and references. Native discovery and invocation have been observed on both hosts. Synthetic qualification does not establish real-user value, superiority over ordinary model judgment or reliable behaviour across all models. The final bounded check passed five Claude assessments, a Codex assessment and exact-copy guards on both hosts. One Claude answer still leaves its elapsed schedule ambiguous. Passing and failing observations remain in [qualification](qualification/README.md).

Claude Code evidence does not establish support on claude.ai or Cowork. Local Codex tests do not establish public-directory acceptance.

## Install in Codex

Use the **Codex skill ZIP**, whose top-level folder is `product-sense/`. Extract that folder into `~/.agents/skills/` for user scope, or your repository's `.agents/skills/` for project scope. It includes the skill, references, UI metadata and icon.

For local development, run from this checkout when the destination does not already exist:

```sh
mkdir -p ~/.agents/skills
ln -s "$PWD" ~/.agents/skills/product-sense
```

Keep one installed copy; update it in place. Codex detects changes automatically; restart it if an update does not appear. [Official installation guidance](https://developers.openai.com/codex/skills)

Invoke explicitly with `$product-sense`, or ask an ordinary product question and let the host select it.

## Try in Claude Code

Extract the **Claude plugin ZIP** outside your Codex skill directories, then load it for one session:

```sh
claude --plugin-dir /path/to/extracted-plugin
```

Invoke `/product-sense:product-sense`, or ask an ordinary product question. On Haiku, invoke it explicitly; Haiku rarely selects it automatically ([run 12](qualification/run-12/report.md)). This is session-only loading. A team marketplace is optional for managed installation and updates. [Claude distribution guidance](https://code.claude.com/docs/en/plugin-marketplaces)

## Example requests

```text
Quick assessment, at most 180 words: Three club organisers say they
would use an AI weekly summary. Today they use email and messages.
We have no observed failures or payment commitments. One engineer has
ten days. Should we build? Assess only; label hypotheses and fit the
next step into the available time.
```

```text
We have chosen the existing stack and have five days. Shape this
approved workflow improvement into a bounded bet with exclusions,
access and recovery, completion criteria and unresolved assumptions.
```

```text
The button already opens the first lesson. We approved changing its
label from Continue to Start lesson. Return only the replacement copy.
```

The skill supports your chosen scope. It does not authorise user contact, live experiments or external changes.

## Build and release

See [PACKAGING.md](PACKAGING.md) for reproducible builds, installation checks and publication steps, and [CHANGELOG.md](CHANGELOG.md) for candidate changes. Generated packages stay outside the installed source tree to avoid duplicate discovery.

## Licence

Public reuse terms await the owner's licence selection. Do not describe this candidate as an open-source release until a licence is included.
