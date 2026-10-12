# Product Sense

Turn an ambiguous product request into a defensible decision and a bounded next step.

Product Sense is a provider-neutral skill for product and engineering teams working with coding agents. It helps assess ideas, shape work to a fixed appetite, review user journeys and distinguish evidence from hypotheses. Its four pillars are user capability, understandable design, continuous discovery and coherent strategy. See the [source map](plugins/product-sense/skills/product-sense/references/canon.md).

## Status

Version **0.2.0** is the first public release candidate for Claude Code and Codex, under the MIT licence. Both hosts use the same instructions and references, kept in [plugins/product-sense](plugins/product-sense). Synthetic evaluations found the skill makes Claude keep to word limits, invent fewer figures, review flows more completely and stop unpromising work more decisively; it did not consistently change which verdict Claude reaches. Passing and failing observations remain in [qualification](qualification/README.md).

Evidence comes mostly from Claude Code. Behaviour on claude.ai and in Cowork is less tested.

## Install in Claude Code

Add this repository as a marketplace, then install the plugin:

```sh
claude plugin marketplace add opsydyn/product-sense
claude plugin install product-sense@opsydyn
```

Invoke `/product-sense:product-sense`, or ask an ordinary product question. Sonnet loads the skill automatically less reliably than Opus, and Haiku rarely does ([run 12](qualification/run-12/report.md), [run 15](qualification/run-15/report.md)), so invoke it explicitly on those models. To try a local checkout for one session, run `claude --plugin-dir plugins/product-sense`. [Claude plugin installation guidance](https://code.claude.com/docs/en/plugins/publish)

## Install in Codex

Use the **Codex skill ZIP**, whose top-level folder is `product-sense/`. Extract that folder into `~/.agents/skills/` for user scope, or your repository's `.agents/skills/` for project scope. It includes the skill, references, UI metadata and icon.

For local development, run from this checkout when the destination does not already exist:

```sh
mkdir -p ~/.agents/skills
ln -s "$PWD/plugins/product-sense/skills/product-sense" ~/.agents/skills/product-sense
```

Keep one installed copy; update it in place. Codex detects changes automatically; restart it if an update does not appear. [Official installation guidance](https://developers.openai.com/codex/skills)

Invoke explicitly with `$product-sense`, or ask an ordinary product question and let the host select it.

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

See [PACKAGING.md](PACKAGING.md) for reproducible builds, installation checks and publication steps, and [CHANGELOG.md](CHANGELOG.md) for candidate changes. Generated packages stay outside the source tree to avoid duplicate discovery.

## Licence

MIT. See [LICENSE](LICENSE).
