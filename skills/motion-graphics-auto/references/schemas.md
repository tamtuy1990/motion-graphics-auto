# Contracts

JSON Schema draft 2020-12 trong `schemas/`. Tất cả object đóng (`additionalProperties:false`). Schema kiểm kiểu; validator xử lý tính đúng liên trường và bằng chứng.

| File | Ý nghĩa |
|---|---|
| timing.schema.json | words/segments, normalized text và trạng thái alignment |
| storyboard.schema.json | canvas, FPS rational, số frame, protected vùng + sự kiện |
| sentences.schema.json | toàn bộ câu nguyên văn, thứ tự, timing và asset associations |
| asset-catalog.schema.json | media đã cung cấp, hash, metadata, thumbnails và rights status |
| edit-plan.schema.json | asset placements, effects, cards và graphics theo layer/frame |

Story event `startFrame/endFrame` dùng interval [start,end). `cueFrame` nằm trong interval; `evidenceWordIds` tham chiếu timing. Các template hiện được schema hỗ trợ: `callout-v1`, `counter-v1`, `bar-chart-v1`, `infographic-v1`, `steps-v1`. Planner được tự do đề xuất ý tưởng và bố cục mới ở bước planning, nhưng schema/renderer hiện chưa nhận composition tùy ý. Khi ý tưởng mới không khớp năm template, biểu diễn là yêu cầu `requires_component` ở proposal layer; không nhét JSON sai schema vào `storyboard.json`, không tự tạo mã chạy. Cần thêm typed composition schema và primitive whitelist trong milestone mở rộng. Tham số template có type. Chart cần unit và zero baseline, không biến giá trị thiếu thành zero. Dataset <=8 points cho MVP. Icon là glyph hoặc asset đã pin, không AI tự chọn network URL.

Protected rectangles dùng tọa độ normalized, theo khoảng thời gian. Scene face/caption detection phải tạo vùng ngoài renderer; starter chỉ tôn trọng vùng đã cung cấp, không tự detect. `asset-catalog` ID liên kết `edit-plan.assetId`; path phải relative, hash phải đối chiếu file thực. `edit-plan` giữ base audio và shot order, cho phép đặt asset images/video, cutaway, PiP, cards, preset effects và graphic event. Timing là frame rational; source trim và target frame là hai clock riêng.

`edit-plan.schema.json` là contract thiết kế, nhưng executable compositor hiện chỉ triển khai một full-frame RGBA overlay CFR/SDR. Nó chưa đọc asset catalog/edit plan để render PiP, cutaway, split-screen hoặc effects. Mọi operation chưa có runtime support phải được báo unsupported.

Scene face/caption detection phải tạo vùng ngoài renderer; starter chỉ tôn trọng vùng đã cung cấp, không tự detect. Title/data dài cần text-fit QA trong browser; validator giới hạn ký tự không bảo đảm fit mọi font.

Sentence IDs `s000001`, `s000002`; word IDs `w000001`. Sentence order liên tục và originalText bao phủ script nguyên văn (audit bằng nối originalText, có whitespace mapping). Một câu không có overlay/assets vẫn có record. `assets` là danh sách tư liệu, status phân biệt candidate/selected/downloaded/rejected, `assetOrder` là thứ tự bên trong câu, in/out là thời gian clip nguồn; placement là thời gian tương đối trong câu. File downloaded phải có path/hash, selected chưa tải không được đưa vào timeline.

Các example trong `examples/` là dữ liệu tổng hợp để test contracts, không phải dữ liệu thực hay chart chứng minh một phát biểu ngoài đời.
