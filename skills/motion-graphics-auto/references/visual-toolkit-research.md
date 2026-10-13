# Nghiên cứu: làm hình ảnh đẹp hơn trong Motion Graphics Auto

Kiểm tra tài liệu chính thức ngày 13/10/2026. Đây là đề xuất kiến trúc cho loại video này, không phải benchmark hiệu năng trực tiếp.

Trước job đầu tiên trong ngày có thay đổi renderer, tra release GitHub theo [live version policy](live-version-policy.md); các chi tiết dưới đây là phân tích capability, không phải lockfile hay cam kết rằng phiên bản này vẫn là mới nhất.

## Kết luận

Chất lượng hình không đến từ việc nhét nhiều framework vào một video. Dùng một timeline/render owner, một design system rõ ràng, visual phù hợp nội dung, typography tốt và assets có chủ đích. Thêm thư viện chuyên dụng vào renderer hiện tại để giải quyết những loại hình mà nó thiếu.

### Hai renderer chính

| Công cụ | Mạnh ở | Hợp với dự án này khi |
|---|---|---|
| Remotion | React/TypeScript, frame-based components, parameterized templates, SVG/data vis, renderer đã phổ biến | Tự động tạo graphic theo JSON, nhiều video dùng cùng thư viện và cùng style |
| HyperFrames | HTML/CSS/JS timeline, nhận web design/animation gần nguyên bản, Studio cho layers/assets, effect/media treatment có sẵn, render seek từng frame | Muốn chỉnh video/layers/media như một HTML project và AI dựng composition trực tiếp từ web elements |

HyperFrames mô tả hai bên cùng xuất frame từ browser nhưng khác cách author: React + frame number ở Remotion, HTML + timeline/seek ở HyperFrames. HyperFrames có hướng dẫn import media, trim/crop/reframe và mute source asset; có media effect families như halftone, tape/CRT, ASCII, grain/vignette. Đây là capability của HyperFrames, không tự áp dụng vào FFmpeg/Remotion pipeline.

**Chọn một làm primary timeline.** Cho kế hoạch hiện tại tiếp tục Remotion + FFmpeg để charts/graphics được data-driven và typed. Làm một spike nhỏ với HyperFrames cho use case có nhiều source assets, cutaways và effects/editable HTML layers. Chuyển hẳn sang HyperFrames nếu project editing/HTML layers quan trọng hơn React component library. Đừng render cùng một composition hai lần qua cả hai engines trong production.

### Thêm vào Remotion khi có nhu cầu cụ thể

| Thư viện | Gì sẽ đẹp hơn/có ích hơn | Khuyến nghị |
|---|---|---|
| SVG + `@remotion/shapes` | Mũi tên, callout, shape, đường nối và diagram có thể animate từng frame | Thêm vào core; nhẹ, tạo primitive cho bố cục mới |
| `d3-scale`, `d3-shape`, `d3-geo` | Trục, scale, line/area, flow, map, proportional/custom charts | Thêm dần cho visualization; dùng D3 tạo hình/data geometry, Remotion điều khiển frame animation |
| `@remotion/transitions` | Wipe, slide, film burn, dissolve, zoom blur và transition overlays | Dùng chọn lọc ở điểm chuyển ý/scene, không đặt transition sau mọi câu |
| `@remotion/lottie` | Reuse animation vector đã được thiết kế bởi người dùng/designer | Dùng như accent/asset. Test từng Lottie; docs cảnh báo một số expressions có thể không seek deterministic và flicker |
| `@remotion/three` + React Three Fiber | 3D map, model/cấu trúc bóc lớp, chiều sâu và parallax | Optional profile-specific module; WebGL rendering cần cấu hình GPU và thường concurrency thấp hơn |
| `@remotion/motion-blur` | Blur thật hơn cho title/shape motion nhanh | Dùng nhẹ. Supersampling/blend có chi phí render và có thể đổi opacity/color |

GSAP là lựa chọn tốt khi có nhiều keyframe phụ thuộc nhau hoặc tận dụng animation HTML hiện có. HyperFrames tự nhiên hơn với GSAP timeline/seek. Trong Remotion, ưu tiên hàm animation thuần theo frame (`spring`, `interpolate`) để mỗi frame render độc lập, dễ lặp lại và dễ kiểm tra.

### Dùng renderer khác như module chuyên biệt

- **Motion Canvas** phù hợp explanatory vector sequence đồng bộ narration, có editor preview và TypeScript generator. Nó cũng là một môi trường author/render riêng, nên chỉ chọn làm primary khi animation vector kể chuyện là trọng tâm; không thêm bên cạnh Remotion chỉ để vẽ chart.
- **Blender** cho cảnh 3D thực sự đặc biệt, sau đó render PNG/EXR sequence có alpha và nhập như asset. Đẹp nhưng thời gian render, quản lý camera/lighting và bảo trì scene cao; chỉ dùng cho những đoạn giá trị cao.
- **Manim** có thể phù hợp giải thích toán/công thức, nhưng phong cách mặc định thường thiên giáo dục/toán; không phải general motion-graphics engine cho toàn video.
- **Rive** mạnh cho animation có state machine tương tác/nhân vật/brand mascot. Với video đã dựng cần frame seeking lặp lại chính xác, Lottie/SVG/Remotion native thường dễ kiểm soát hơn; Rive cần test workflow render frame thật trước khi đưa vào pipeline.

## Chất lượng hình: quy trình quan trọng hơn số package

1. **Style bible cho mỗi video**: palette 3–5 màu có ý nghĩa, hai font tối đa (font có glyph tiếng Việt/Hàn), type scale, grid/margin, stroke, shadow, corner, chart color và transition curve. Giữ 1–2 motif xuyên suốt chỉ khi hợp mạch kể.
2. **Visual beats**: mỗi cảnh có hierarchy rõ: điểm nhìn đầu tiên → chi tiết giải thích → nguồn/đơn vị → exit. Chia nhịp theo ý thoại, không theo fixed number of graphics per minute.
3. **Chart đúng số liệu**: chọn chart theo câu hỏi, giữ baseline/units/denominator/qualifiers; D3 không tự đảm bảo trung thực dữ liệu. Source evidence và validator riêng.
4. **Footage treatment**: ưu tiên project asset đúng đoạn, crop có chủ ý và cutaway theo narration. LUT/effect chỉ tạo cảm xúc/phân tách tư liệu; tránh effect mạnh đồng thời với biểu đồ đọc số liệu.
5. **Typography**: fit/wrap theo browser sau khi load font, kiểm font thật và đọc ở mobile display size. Không để AI xuất text thành ảnh raster.
6. **Motion restraint**: cùng một easing family, vào/ra ngắn, stagger chỉ cho quan hệ cần đọc. Graphic để đủ thời gian đọc; nhiều animation cùng lúc làm giảm cảm giác chuyên nghiệp.
7. **Preview gần output**: contact sheet + real-time preview; kiểm typography, safe zones, faces/subtitles, alpha, effect artifacts. Một frame đẹp không đảm bảo clip chuyển động ổn.

## Kết nối với AI planner và request budget

Các package trên là renderer/code, không yêu cầu model API call theo từng scene. Giữ một DeepSeek plan request toàn kịch bản. Đưa vào đó catalog capabilities + style tokens + tóm tắt asset IDs; model trả scene intent, template/primitive IDs, exact evidence và animation beats. Code validate, đo chữ, resolve assets, render và QA local. Không hỏi model cách set mỗi điểm màu hoặc mỗi keyframe.

Output budget JSON có thể lớn hơn ý tưởng 1M input context: chỉ trả scene có visual và trạng thái coverage gọn cho tất cả sentence IDs. Nếu scene graph chi tiết quá lớn, planner trả reference đến reusable style/motion presets. Giữ full script/timing local và liên kết bằng IDs.

## Thứ tự triển khai đề xuất

1. Cải thiện typography, spacing, palette, SVG primitives, D3 custom chart và Remotion transitions. Đây thường là nâng cấp hình đáng kể với dependency/API complexity thấp.
2. Asset catalog + editable timeline operations từ project bin (cutaway, PiP, cards/effects) và QA trên sequence liên tục.
3. Thêm curated Lottie pack nếu có các accent/logo animation được phép sử dụng.
4. Chỉ sau đó mới thử Three/Blender cho những scene mà 2D không giải thích được.
5. Chạy HyperFrames spike đối chiếu một video ngắn thực tế; so số hạng mục: editability, render time, visual QA, audio stream preservation, reproducibility và công sức bảo trì. Chọn primary engine dựa trên kết quả đó.

## Tài liệu

- [HyperFrames overview](https://hyperframes.heygen.com/introduction)
- [HyperFrames vs Remotion](https://hyperframes.heygen.com/guides/hyperframes-vs-remotion)
- [HyperFrames images/video](https://hyperframes.heygen.com/guides/video-components)
- [HyperFrames media effects](https://hyperframes.heygen.com/guides/media-effects)
- [Remotion transitions](https://www.remotion.dev/docs/transitioning)
- [Remotion shapes](https://www.remotion.dev/docs/shapes)
- [Remotion Three.js integration](https://www.remotion.dev/docs/three)
- [Remotion Lottie](https://www.remotion.dev/docs/lottie)
- [Remotion motion blur](https://www.remotion.dev/docs/motion-blur)
- [D3](https://d3js.org/)
- [GSAP timeline seek](https://gsap.com/docs/v3/GSAP/Timeline/)
- [Motion Canvas](https://motioncanvas.io/docs/)
- [Blender transparent film background](https://docs.blender.org/manual/id/4.0/render/cycles/render_settings/film.html)
