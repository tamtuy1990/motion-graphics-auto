# Kiến trúc và kế hoạch triển khai

## Bundle DSH hiện có

```text
dsh-motion-graphics-auto/
  package.json                 # declares a DeepSeek Harness bundle
  cordis.patch.yml             # mounts the runtime plugin
  index.js                     # registers the Skill and release-check tool
  version-check.js             # once-per-day GitHub Releases cache
  skills/motion-graphics-auto/
    SKILL.md
    references/                 # architecture, timing, schemas, rendering, QA, budgets
    schemas/                    # storyboard, timing, sentences, assets, edit plan
    examples/                   # sample inputs and plans
    scripts/                    # deterministic validation/composition helpers
    assets/remotion-starter/    # frame-driven overlay starter
```

The plugin mounts instructions and a small GitHub cache tool into DeepSeek Harness. It does not install FFmpeg, Python, Whisper, Remotion or codecs. Python helpers need Python 3.10+, `jsonschema` and Pillow for composition; the renderer needs compatible pinned Node/Remotion/React versions. STT may require a separate Python/GPU environment.

## Media pipeline still to implement as an application

1. **Probe and inventory:** inspect CFR/SDR and asset metadata, fingerprint the project bin, produce contact sheets, and establish audio offset. Expand explicit VFR/HDR/rotation handling.
2. **Alignment and sentence index:** use forced alignment when a script is supplied; otherwise transcribe locally. Keep original script text distinct from normalized aligner text and never invent timestamps.
3. **One batch visual plan:** send the compact full timed script and relevant asset facts to the configured DSH model. Use the JSON schemas, broad visual reasoning rules and deterministic templates; avoid one planning call per sentence.
4. **Local validation and render:** validate the storyboard once, render supported overlays/cutaways, and composite with FFmpeg while preserving original video/audio streams.
5. **Automated QA:** verify frame/time boundaries, safe areas, fonts, alpha, audio and output streams. Repair deterministic failures locally; use at most one batch semantic repair if the user-configured budget permits.
6. **Request accounting:** implement a persistent provider-call ledger and hard request cap in an application-level gateway if actual enforcement is required. The current DSH plugin is a skill bundle and does not intercept all outer Harness model calls.

Do not mistake this plugin package for a completed desktop editor or a fully enforced request-budget runtime. Its deliverable is the DSH-native workflow skill, schemas/examples/helpers already present in the previous skill package, Cordis bundle registration and once-per-day release checker.
