# Kiến trúc kỹ thuật — phương án C

Luồng chính: video đã dựng + project media bin → probe/fingerprint/catalog/contact sheets → audio phân tích → script alignment hoặc STT+alignment → sentences/words → one-request whole-script visual plan (events + project asset IDs + edit operations) → schema + semantic QA → render graphic/effect/asset layers → FFmpeg composite → QA → bản xuất mới.

Video dựng là base timeline. Default giữ nguyên shot order, shot timing và audio gốc; image/footage từ bin có thể được đặt thành overlay, PiP, split-screen, hoặc cutaway (thay hình tạm thời, base audio vẫn chạy). Chỉ recut/reorder/replace shots nếu user yêu cầu. Added asset audio muted. Graphics/effects/assets chạy như các visual tracks có layer order. Burn-in làm thay đổi bitstream video và cần re-encode; source luôn bất biến. MKV có thể giữ thêm audio codec; MP4 không hỗ trợ mọi codec. Không âm thầm đổi audio.

## Thành phần

| Thành phần | Công việc | Dùng LLM? |
|---|---|---|
| Ingest/catalog | ffprobe, SHA-256, asset IDs, thumbnails/contact sheets, FPS/PTS/audio/color | Không |
| Timing worker | script normalizer, forced aligner; STT khi thiếu script | Không cần LLM planner |
| Sentence index | nguyên văn, thứ tự, word IDs, confidence, timing | Không |
| Planner | chọn biểu đạt, project asset IDs, template/composition, operations, evidence | Có, một JSON cho full script |
| Layout compiler | time→frame, tránh protected regions, fit chữ | Không |
| Remotion worker | deterministic templates, PNG alpha | Không |
| FFmpeg worker | xếp base/effect/asset/graphic tracks, compositing, audio stream copy | Không |
| QA worker | streams, timestamps, decoded audio hash, ảnh kiểm tra | Chủ yếu code; vision chọn lọc |

Orchestrator lưu state: INGESTED → TIMED → PLANNED → VALIDATED → RENDERED → COMPOSITED → QA_PASSED. Failed stage có lỗi, artifact hash, command args và retry count. Chỉ render/composite storyboard đã validate. Không dùng success file cũ nếu manifest hash thay đổi. Ghi file tạm rồi atomic rename sau thành công; không ghi đè nguồn.

Một job có input paths/hashes, ffprobe JSON, timeline origin, speech stream selector, audio offset, script hash, provider/model revision, normalized words, sentence index, storyboard, render props, overlay frames, QA report và output. Thư mục runtime không nằm trong thư mục skill. Paths untrusted không được nối thành shell command; dùng argument arrays.

## Quyết định timeline

Store source video PTS, stream time_base, first decoded video timestamp và audio timestamp. Với CFR SDR start-zero, overlay frame n tại n·fps_den/fps_num. Ưu tiên fps rational (30000/1001), không round thành 30. Frame count lấy decoded/probed count nếu đáng tin, không chỉ duration*FPS. Với VFR, xây PTS table và lookup frame; MVP helper từ chối VFR thay vì âm thầm đổi CFR. HDR/rotation/negative PTS cần compositor riêng để giữ color/geometry/timeline; MVP cũng từ chối.

## Nguồn tham khảo chính thức (kiểm tra 13/10/2026)

- https://www.remotion.dev/docs/transparent-videos — PNG frames, ProRes 4444 alpha, WebM alpha.
- https://www.remotion.dev/docs/cli/render — CLI frame ranges, sequence rendering.
- https://ffmpeg.org/ffmpeg-filters.html — overlay/framesync.
- https://ffmpeg.org/ffmpeg.html — stream mapping/copy.
- https://github.com/m-bain/whisperX — ASR + alignment, giới hạn ngôn ngữ/từ không align được.

Các ngưỡng QA, mật độ và cách chia worker là thiết kế của gói này, không phải bảo đảm từ các thư viện.
