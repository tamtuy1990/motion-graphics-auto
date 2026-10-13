# Module mở rộng: script → tư liệu theo câu

Đầu ra đúng với nhu cầu: toàn bộ câu full script có số thứ tự, mỗi câu có 0..n hình/video và thứ tự tư liệu riêng. Không bắt buộc câu nào cũng có B-roll: có thể dùng cảnh gốc hoặc graphic.

Script nguyên văn → sentence index → keywords/visual intent → search adapters (web/image/video/YouTube) → candidate records → relevance/licensing/acquisition check → chọn assets → download hợp lệ → hash/probe → placements trong câu → timeline builder. Timing chỉ final sau khi có audio, không suy thời lượng chính xác từ độ dài chữ.

Tách kho candidates khỏi selected placements. Source URL khác download URL. Lưu source/title/author/license/license URL/attribution, nguồn truy xuất và trạng thái quyền. Với YouTube, URL/thumbnail/transcript giúp khám phá; public không đồng nghĩa được quyền tải và tái sử dụng. Không dùng download adapter để né restriction. Quyền chưa rõ → candidate, không downloaded/ready. Search API key và rate limit cấu hình từ môi trường; không đóng secrets trong skill.

Đánh số: `s000012` là câu thứ 12; `s000012_a01` là tư liệu đầu tiên của câu đó; filenames có thể `s000012_a01.mp4`. `assetOrder` không thay `sentence.order`. Cùng asset reuse nhiều câu dùng cùng asset hash và placements riêng. In/out clip nguồn không bằng start/end trong timeline.

Một câu 8 giây có thể dùng video A 0–4 giây, ảnh B 4–8 giây hoặc chồng callout. Semantic validator cần kiểm coverage theo policy, intentional gaps, overlaps và clip trim không vượt source duration. Câu dài không tự chèn nhiều media cho đủ số lượng.

Module này là plan/schema; package hiện tại không có search/downloader adapter. Nếu bật nó để thay cảnh, tạo job `script-to-media` riêng và xin đúng đầu vào còn thiếu; không thay đổi mặc định overlay-only của phương án C.
