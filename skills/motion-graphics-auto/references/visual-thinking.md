# DeepSeek visual director

## Request purpose

Make one batch request for the full timed script. Ask the model to act as a visual director: explain the script with fitting visual ideas, not merely fill templates. The model may recommend charts, bespoke compositions built from registered primitives, imagery research queries, restraint, or no overlay. The renderer registry constrains what is executable; it does not constrain the model's idea generation.

## Planning rubric

For each script passage:

1. State its narrative function in a short phrase: introduce, compare, explain cause, reveal change, support with evidence, create scale, locate, transition, evoke, or conclude.
2. Identify the one viewer question the visual should answer. Do not decorate sentences whose meaning is already clear in the footage.
3. Choose a visual metaphor/layout that fits that function and the full story context. Prefer a specific shape/relationship over a generic title card. Use a data chart only when it improves comparison/trend/proportion and the supplied data supports it.
4. Name exact evidence: sentence IDs, word IDs and quote; source data IDs for values. Preserve qualifiers, dates, units, uncertainty and comparison basis.
5. Specify what appears, where, in what sequence, and why that timing helps comprehension. Limit simultaneous elements according to reading speed.
6. Pick a registered template or describe a typed composition from approved primitives. If no current renderer can express it, return a `requires_component` proposal with rationale and fallback. Never emit JSX, source code, arbitrary HTML, external URLs as executable assets, or invented chart data.
7. First consider the user's supplied project bin. If a supplied image/video is a better fit than a graphic, reference its catalog `asset_id` and choose a cutaway, picture-in-picture, split-screen or image overlay treatment. Give an external asset-search query only when supplied assets do not cover a real need and research mode is enabled. Search groups may serve multiple sentence IDs. A result being found does not establish usage rights.

Do not require one graphic per sentence. Mark sentence coverage as one of `graphic`, `asset_search`, `no_graphic_needed`, or `needs_review`; never silently omit sentence IDs. Prefer fewer strong visuals over repetitive restatement. Reuse a visual motif across the video only when the story benefits from it; do not impose one motif on unrelated scenes.

## Prompt skeleton

Use as the AI Director system instructions, alongside the strict JSON schema and current renderer catalog:

```text
You are the visual director for a finished speech-led video. Read the entire script before planning any visual so each idea fits the story context. Decide what each passage is doing and how a viewer would understand it fastest. The renderer template catalog is a set of available tools, not a limit on your ideas. You may invent a composition by arranging the listed deterministic primitives, or propose a missing component with requires_component. Do not write code.

For every sentence ID, return one coverage status: graphic, asset_search, no_graphic_needed, or needs_review. Create an event only when a visual materially improves comprehension or emotional clarity. Choose its form from its meaning: comparison, change, causality, process, scale, space, evidence, uncertainty, abstract metaphor, or human moment. A number alone does not mandate a chart. A metaphor must be visibly illustrative, not presented as literal footage or measured data.

Use only source-linked claims and supplied data. Preserve units, qualifiers and uncertainty. Every factual number or quotation needs evidence IDs. Do not infer missing values. Keep the original script untouched in the local manifest; refer to sentence and word IDs. Plan concise on-screen text, normalized safe placement, cue word, duration and ordered animation beats. Prefer no overlay over a generic/repetitive visual.

Return one complete JSON object for the whole script. Do not summarize away sentences. Do not split your answer into prose or tool calls. If a design needs rendering support absent from the registry, return a typed component proposal and requires_component status; never pretend it is renderable. If the full response cannot fit, state output_limit instead of truncating or omitting later sentences.
```

This is a prompt pattern, not a request-cap enforcement mechanism. Gateway, output preflight, persistent ledger, response-completeness check and local schema validation enforce runtime limits.

## Example of an original composition

For “the city expanded outward while the old center emptied,” do not invent population figures. A suitable proposal could animate a simple map-like center and outer ring: small people markers leave the center as the outer boundary grows, with labels “old center” and “outer districts.” This composes circles, boundary, arrows and labels. If only cards/counters are installed, mark the map composition unsupported; do not disguise it as a chart or claim population measurements.

For “a policy looked cheaper at first, but the hidden maintenance cost accumulated,” a two-stage scene could reveal a low purchase-price block, then progressively stack a separate maintenance column. Values only appear if supplied. With no numbers, use unlabeled relative shapes plus clear “initial cost” and “ongoing cost” labels, or choose an asset search. The visual is a conceptual explanation, not a quantitative comparison.

## Integration boundary

Current `storyboard.schema.json` and Remotion starter accept five fixed templates. They do not yet accept or render arbitrary compositions. Extending the product requires a typed composition schema (primitive whitelist, layout boxes, layer order, animation tokens, evidence refs), deterministic renderer and tests for overlap, accessibility, text fit, timing and output. Add a new registry component only where a real script demonstrates the need. Until then, the agent can reason broadly, but unsupported artwork must be surfaced rather than fabricated.
