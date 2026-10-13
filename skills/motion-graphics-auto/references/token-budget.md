# Ngân sách request — toàn kịch bản trong một lượt

Không ném video hay hàng nghìn frame vào context. Local code/STT/align/render không dùng planner tokens; API STT, vision và model khác vẫn có chi phí riêng. Không cam kết một mức tiết kiệm phần trăm khi chưa đo.

1. Probe, splitting, timing và numeric entity extraction bằng code. LLM chỉ nhìn sentence_id, nguyên văn, start/end, confidence, đề xuất anchor, dữ liệu verified và preset ID.
2. Gửi toàn bộ kịch bản/timed sentences trong một planning request, chọn style và cơ hội infographic cho cả video. Nếu bật research, trả luôn nhóm truy vấn tư liệu. Không chia mặc định theo thời lượng 30–90 giây; không thay full script bằng summary.
3. Preflight actual endpoint context/output limits. Context gần một triệu token là capability cấu hình của endpoint người dùng, không phải output guarantee. Chỉ chia ownership ranges khi input thực sự vượt context; overlap chỉ để đọc, không phát sinh duplicate events. Nếu output không đủ, báo rõ single response không thể đầy đủ và dùng bounded fallback trong cap; không silently truncate hoặc bỏ câu.
4. Tối đa một follow-up cho cả job, gộp chọn candidates và sửa unresolved semantic/layout failures. LLM xuất patches theo event ID, không regenerate toàn storyboard. Local repairs có thể thử hai lần; không tự gọi LLM vì lỗi local. Normal target 1–2 calls; tổng hard cap 5 dispatch attempts/job gồm retries và fallback batches. Dành ngân sách follow-up/retry trước dispatch batch; thiếu cap thì dừng, giữ artifacts.
5. Cache timing theo audio+model hash; planner theo timed text+policy+prompt+model hash; render theo props+fonts+templates+engine lock. Invalidate đúng stage.
6. Vision chỉ review các candidate frames và failures; lấy contact sheet có timestamp, không full video tự động. Sources snippets ngắn, dedupe URL; không gửi cả trang HTML cho planner.

Metrics: tokens input/output mỗi stage, số gọi, cache hit, cost API, GPU minutes, wall time, disk. Benchmark cùng video/script với fresh cache và warm cache. Quota budget hết thì dừng paid calls, trả artifact hiện có; không chạy API ngoài lựa chọn đã cấu hình.

## Gateway và sổ request — yêu cầu triển khai

Mọi model call đi qua một gateway; SDK hidden retries=0, concurrency=1, subagents disabled trong xử lý thường. Tối đa một transport retry cho toàn job, chỉ cho transient failures và còn budget. Không dò unsupported features bằng các paid retry. Creative Mode không tự bật.

Persistent SQLite ledger lưu job/attempt ID, purpose, payload hash, provider/model, timestamps, state, provider request ID, usage và billing confirmation. Atomic reserve trước network dispatch; tính reserved attempts để workers không vượt cap. Retry reserve lượt mới. Crash/timeout sau dispatch giữ `unknown`, không hoàn lượt hoặc reset budget khi resume. Cache hit không reserve. Phân biệt dispatched attempts, successful responses và confirmed billable requests; internal server retry không quan sát được phải ghi unknown.

Billing mode per_request/per_token configurable. Giá 3 VND/request chỉ là cấu hình minh họa từ prompt người dùng, phải xác nhận với provider thực tế; không coi là giá chính thức DeepSeek. Search/STT/vision có quota và cost riêng. Không hứa 1–2 calls cho mọi độ dài nếu input/output limit không đủ.

Planner output gọn theo sentence IDs; local manifest giữ nguyên toàn script. Coverage phân biệt `no_graphic_needed` và `unprocessed` để không nhầm không có graphic với chưa xử lý. Response rỗng, finish_reason=length, JSON lỗi hoặc thiếu coverage không được đánh dấu success. SRT IDs và sentence IDs là hai lớp, giữ mapping; SRT timing coarse, align word anchors khi cần.

Cache phải bao gồm full timed transcript, prompt/schema/registry versions, relevant media/protected regions, verified data/candidate hashes, model và settings. Không gửi full web HTML/raw frame dumps. Local fixes chỉ move box/text-fit/dedupe, không tự thay số liệu hoặc cắt chữ làm đổi nghĩa.

Acceptance cần triển khai: warm cache zero calls; whole-video plan nhiều events từ một request; render 40 events zero extra calls; local failures không auto gọi model; tối đa một follow-up; retry được đếm; cap giữ qua resume/concurrency/crash; truncated output không pass. Gateway/ledger/planner chưa có executable trong gói hiện tại.
