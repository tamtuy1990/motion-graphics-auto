# Motion Graphics Auto for DeepSeek Harness

This is an installable DeepSeek Harness bundle. It registers the existing `motion-graphics-auto` workflow as a native DSH skill and adds one deterministic tool, `motion_graphics_auto_check_releases`, for the once-per-day Remotion and HyperFrames GitHub check.

The bundle was designed against the latest GitHub release visible on 13 October 2026, `v0.2.1-alpha.2` (a prerelease). It uses the current `ctx.skills.register()` and `ctx.tools.register()` interfaces, and declares no DSH runtime package dependency of its own. The default Standard profile must provide the `skills` and `tools` services and the model-facing skill consumer.

## Install from GitHub

Install the public bundle into a Standard profile:

```sh
dsh plugin --profile standard add github:tamtuy1990/motion-graphics-auto
```

Or paste `github:tamtuy1990/motion-graphics-auto` into DeepSeek Harness's **Add plugin** dialog. Keep the Registry set to the official npm registry unless your profile deliberately uses another registry; that field configures npm dependency resolution, not the GitHub source.

Confirm the bundle appears in the profile's composed configuration:

```sh
dsh --profile standard --dump-config
```

After installing, restart a profile whose bundle composition is startup-only, then ask the Harness to use `motion-graphics-auto` on an edited video.

For local development, extract the source ZIP and run `dsh plugin --profile standard add ./dsh-motion-graphics-auto` from the parent directory.

Remove it with:

```sh
dsh plugin --profile standard remove dsh-motion-graphics-auto
```

The bundle requires a Node runtime accepted by the selected DSH release (`^22.19.0 || >=24.0.0`). It does not install FFmpeg, Python, Whisper, Remotion, or media codecs; the workflow checks for those project/runtime dependencies and reports missing ones.

## What it contributes

- `index.js` mounts the skill into DSH's skill registry and points relative resources at the packaged schemas, references, scripts, and Remotion starter.
- `motion_graphics_auto_check_releases` calls only the two fixed GitHub API endpoints for Remotion and HyperFrames. It persists the result under `$DSH_HOME/cache/motion-graphics-auto/github-release-cache.json` (or `~/.dsh/...`) and avoids another check for the same `Asia/Ho_Chi_Minh` date, including when a prior network check failed.
- Rendering and QA remain local deterministic work driven by the Harness's existing tools. The plugin itself makes no DeepSeek API request.

The original request cap and cache ledger remain design requirements in the skill. This packaging does not add a provider-call gateway that can count and block every outer DSH model request; the skill says so explicitly instead of claiming a prompt enforces it.

## Development checks

Run `node tests/plugin.test.js` from this directory. Tests use a mock DSH context and mocked GitHub responses; they do not need credentials or network access. Full profile installation requires the DSH CLI and a compatible profile, neither of which is bundled here.
