# Visual repertoire and deterministic templates

This is a repertoire, never a closed list of ideas. DeepSeek should reason from the script's meaning and story function. It can choose a listed template, combine registered primitives into a fresh composition, or propose a renderer capability that does not exist yet. It must not force every sentence into a familiar chart/card.

## Think before choosing a visual

For each candidate passage, determine: (1) what changes in the viewer's understanding, (2) the key entities and their relationship, (3) whether the passage is factual, comparative, sequential, spatial, causal, emotional, or reflective, (4) what visual makes that relationship easiest to perceive, (5) which exact spoken words anchor its timing, and (6) whether the necessary data/assets are available. Return `no_graphic_needed` when footage/narration already communicates the point.

Prefer the simplest visual that explains the intended idea. Numbers do not automatically imply charts. A percentage with no comparison group may call for a typographic statistic; a change over time can use a timeline; a causal chain can use linked nodes; a personal memory may be better served by an archival image or gentle annotation than a data graphic. Metaphor can clarify abstract ideas, but label it as metaphor and never let it appear to be documentary evidence.

Build new scenes by arranging the renderer's reusable primitives: text, number, shape, line/arrow, icon/glyph, connector, timeline tick, chart mark and image/video window. Reuse the same primitive across different compositions with different hierarchy, direction, grouping, pacing and animation. The composition can be novel even when each part is deterministic. Plan in normalized boxes and an explicit layer/order list; use local layout code to resolve fit and safe regions.

Potential visual families below prompt thinking; they are not an exhaustive menu:

| Story/content function | Possible visual language |
|---|---|
| Compare choices or opposing forces | Split stage, paired objects, balance, diverging bars, before/after |
| Explain cause and consequence | Connected nodes, branching path, domino sequence, causal loop |
| Show process or escalation | Path, stepped reveal, funnel, flow, timeline, accumulation |
| Explain proportions or composition | Nested shapes, stacked blocks, exploded components, proportional marks |
| Locate a person/event | Map marker, route, region callout, spatial layers |
| Ground a claim in evidence | Document crop, quote highlight, source card, annotated still |
| Make an abstract idea legible | Carefully labeled metaphor, scale shift, visual analogy, symbolic transformation |
| Human/emotional passage | Restraint, typography, meaningful still/B-roll, pause without graphics |
| Explain an unseen system | Cutaway, schematic, layers, inputs→transformation→outputs |
| Describe uncertainty or disagreement | Range, confidence band, competing hypotheses, source comparison |

These visual families are design prompts; only render what the registry can produce. Do not represent an illustrative metaphor as measured data or as a literal event.

## Current registered templates

| ID | Input | Hành vi |
|---|---|---|
| callout-v1 | title, body | Fade/slide card, không thay đổi nội dung |
| counter-v1 | label, from, to, unit, decimals | Count theo frame, ease-out, giữ giá trị cuối |
| bar-chart-v1 | title, unit, data(label,value) | Thanh từ zero baseline; scale theo max |
| infographic-v1 | title, items(glyph,label) | Card với danh sách glyph và nhãn |
| steps-v1 | title, steps | Đánh số bước, highlight theo frame |

Starter currently supports one graphic at a time and only the five templates listed below. It does not yet render arbitrary primitive compositions. If the planner's best idea requires a new composition, include its visual rationale and a typed primitive-level proposal in the plan, mark it `requires_component`, and continue with the closest supported design only if meaning is preserved. Otherwise leave it unrendered and report the gap. Add a real renderer component only as a deliberate implementation change with schema and QA.

Counter `from` is an animation state, not a factual value; `to` must have evidence. Bar charts currently support non-negative values only, no stacked or dual-axis display. A schema-valid chart is not automatically fact-checked.

Template props không chứa HTML/CSS/JS tùy ý. Một event sửa tham số vẫn dùng component cố định. Frame-driven easing và opacity không phụ thuộc thời gian render. Locale/font được truyền và pin bởi môi trường job. Font fallback giữa hai máy có thể khác: production phải bundle font phù hợp license và kiểm glyph tiếng Việt.

Starter has character limits but no automatic text fitting. Cards need visual QA or browser text measurement. The Remotion CLI/TypeScript rendering and these templates were not smoke-tested with Remotion dependencies in this package; milestone 1 is required before production use.
