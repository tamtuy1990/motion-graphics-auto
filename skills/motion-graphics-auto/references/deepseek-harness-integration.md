# DeepSeek Harness integration

## Bundle shape

The package is a DSH bundle, not a Codex/OpenAI plugin archive. `package.json` declares `dsh.bundle.patch`; `cordis.patch.yml` mounts `index.js` as a Cordis plugin. The plugin injects DSH's `skills` and `tools` services, registers the bundled workflow using `ctx.skills.register()`, and exposes one fixed-purpose release-check tool using `ctx.tools.register()`. The skill's `resourceBase` points to its packaged references, schemas, scripts, examples and Remotion starter.

This design follows the current DSH split between reusable procedural Skills and executable Cordis plugins. The skill contains planning, alignment, storyboard and QA instructions. The Cordis plugin contributes runtime registration and the small deterministic GitHub cache tool; it does not create a separate agent or direct DeepSeek API client.

## Model requests and the hard cap

The plugin makes **zero DeepSeek API requests** itself. Its release tool makes up to two fixed GitHub requests once per local date. Motion planning uses the model already configured by the active Harness profile and calls its normal tool loop.

The target of 1–2 model requests and hard maximum of 5 per video remain requirements for a future application-level planner/gateway. This plugin's skill can direct the agent to plan the whole script in one batch and avoid scene-by-scene model calls, but a skill prompt alone cannot count or block all outer Harness requests, retries or subagent requests. Do not tell the user that the hard cap is enforced by this package.

## Host and profile requirements

Targeted against DeepSeek Harness GitHub release `v0.2.1-alpha.2`, the latest release visible on 13/10/2026. That tag is a prerelease. The selected profile needs the `skills` registry, model-facing skill tool, and `tools` registry mounted; the Standard profile is the intended target. The package declares no DSH runtime imports or separate npm dependencies, avoiding a second Cordis/tools registry instance. The DSH runtime itself requires Node `^22.19.0 || >=24.0.0` in the referenced release.

The bundle is a local package that `dsh plugin --profile <profile> add <folder>` links into a profile. Verify composition with `dsh --profile <profile> --dump-config` before starting a real job. The current workspace does not contain the `dsh` CLI, so this artifact was checked with a mock Cordis context and unit tests rather than installed into a live Harness profile.

## Official references

- DSH plugin package/install guide: https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/user/develop/basic/publish.md
- DSH Cordis plugin and `ctx` API: https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/user/develop/basic/index.md
- DSH skill registry and runtime registration: https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/subsystems/skills.md
- DSH tool authoring/API: https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/cookbook/adding-a-tool.md
- DSH release: https://github.com/deepseek-ai/deepseek-harness/releases/tag/v0.2.1-alpha.2
