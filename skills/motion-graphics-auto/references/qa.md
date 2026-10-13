# QA và acceptance

## Trước render

- Mọi sentence/word/event ID unique, timings hợp lệ, event trong timeline và confidence đủ; số liệu có exact quote/source.
- Nội dung có template đúng loại; không overlapping event/protected vùng. Gap/density là policy trong planner, không hardcoded schema.
- Tất cả assets/fonts local và hash pinned. Không load code từ URL/storyboard. Fit chữ ở đúng font, không cắt/sai dấu tiếng Việt.

## Sau render/composite

- Inspect event first visible/peak/last visible, cueFrame, frame trước/sau; thêm sample mỗi shot và shot cut gần event. Đọc trên kích thước người xem thực tế, không chỉ full-resolution monitor.
- RGBA alpha transparent ở ngoài card; không black matte/flicker. Kiểm faces/captions/brand lockup không bị che. Protected regions manual cần review, không gọi là automatic vision QA.
- ffprobe: output dimensions/FPS/frame count bằng canonical input, video duration lệch <=1 frame, số audio streams và codec/channel/sample rate giữ nguyên.
- Stream-copy audio payload hash (demux data hash) khi khả dụng + hash decoded PCM theo từng stream; kiểm timestamp/duration riêng. PCM hash giống chưa chứng minh timestamps giống. Không dùng hash toàn container.
- Detect source/output audio start PTS drift <=1 ms cho đường CFR/start-zero; báo codec priming/mux rounding nếu vượt. Event timing ±2 frame so với nhãn manual/verified alignment.
- Không yêu cầu pixel hash video giống vì encode lại; optional so sánh vùng ngoài overlay với metric cho codec đã chọn. Encode CRF 18 không được gọi lossless.

QA report gồm status pass/fail/review_required, metrics, tool versions, input/output hashes, từng event evidence + cue delta + screenshot paths + human review, exclusions và repairs. Phải chạy checks, không đánh dấu pass từ planned checks. Tối đa hai local repairs cho cùng lỗi; model-assisted repair gộp vào một follow-up duy nhất cho cả job theo request budget. Nếu không đạt, omit optional overlay hoặc giữ output ở trạng thái failed.
