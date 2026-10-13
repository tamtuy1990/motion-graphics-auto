# Timing và nội dung

## Có script

1. Chọn audio từ bản dựng cuối. Nếu audio rời có khác đoạn cắt, offset duy nhất không đủ: cần anchor mapping theo từng đoạn hoặc dùng audio trong video. Không tự suy offset=0 khi chưa có bằng chứng.
2. Giữ `originalText`; tạo bản normalization có mapping char/word về nguyên văn (số viết thành chữ, viết tắt, punctuation). Chia câu deterministic, không bỏ câu; với tiếng Việt một token khoảng trắng không nhất thiết là một từ ngôn ngữ học.
3. Forced alignment bằng model phoneme/CTC phù hợp ngôn ngữ. WhisperX align nhận các segment text+start/end; script thuần không có segment windows cần VAD + đối chiếu ASR draft với script để định vị cửa sổ, rồi align script trong cửa sổ đó. Không đưa toàn bộ video dài vào một segment mặc định.
4. Phát hiện script lệch lời đọc: skipped/repeated/changed words. Ghi `unaligned` với times=null, không ép khớp. Không giả định Vietnamese có default model: kiểm tra registry ở phiên bản pin; chọn model đã thử hoặc fallback coarse sentence timestamps gắn confidence thấp.

## Không script

Audio → VAD → STT (Whisper/faster-whisper hoặc adapter đã cấu hình) → language-matched alignment → words. Model STT chạy local không tiêu token context của planner, nhưng tốn CPU/GPU; API tính theo nhà cung cấp. Diarization optional khi nhiều người; không cần nếu chỉ muốn sync lời thoại.

## Quy ước

Thời gian words là giây tương đối với video origin: t_video=t_audio+offsetSeconds. `null` biểu thị không align. Confidence provider khác nhau không so trực tiếp: adapter ghi `method`, confidence nullable, kiểm tra sample thủ công để hiệu chuẩn. Đánh dấu một câu `partial` khi thiếu bất kỳ word timing nào; không biến nó thành `aligned` chỉ vì có hai biên.

Frame start=floor(t_start*fps_num/fps_den), end=ceil(t_end*fps_num/fps_den); end exclusive. Clamp vào [0,durationFrames]. Không quantize đi quantize lại. `cueFrame` là frame từ word anchor để số/callout hiện đúng lúc nhắc; entrance có thể bắt đầu 4–8 frame trước cue. Đối với VFR dùng PTS lookup thay công thức này.

QA timing mặc định: trigger lệch anchor không quá 2 frame khi alignment đáng tin; STT uncertain yêu cầu review hoặc omit. Benchmark accuracy timing chỉ tính với nhãn đối chiếu bằng nghe/quan sát, không tự đo độ đúng từ output của chính aligner.

MVP validator dùng ngưỡng confidence 0.75 cho anchor; adapter phải hiệu chuẩn score hoặc gắn confidence sau review. Khi provider không có score, không tự điền 1.0; review hoặc omit event. Ngưỡng này là policy ban đầu, cần đổi theo benchmark của provider/ngôn ngữ.

Adapter contract: input waveform + source offset + original script optional; output `timing.schema.json`. Khóa cache theo audio hash, script hash, normalization version, language, model/revision và offset. Không cache chỉ theo filename.
