# Overlay rendering

Copy `assets/remotion-starter` vào workspace. Starter là JSX frame-driven; pin các package `remotion`, `@remotion/cli`, `@remotion/renderer` cùng một version tương thích với React/ReactDOM, cùng fonts và lockfile. Không để version `latest` trong job đã xác nhận. Package manifest được tạo ở milestone setup, vì gói này không tải dependencies hoặc tuyên bố version đã smoke-test.

Validate storyboard; truyền `--props=storyboard.json` vào composition `Overlay`. Composition lấy width/height/fps/duration từ metadata; không render base video/audio trong React.

```text
npx remotion render src/index.tsx Overlay frames --sequence --image-format=png --props=storyboard.json
python scripts/composite.py source.mp4 frames storyboard.json enriched.mkv --execute
```

Script chuẩn hóa số thứ tự PNG mà Remotion xuất thành sequence bắt đầu 0 và kiểm số lượng/dimensions/mode RGBA. Preview (không --execute) chỉ in argument list. Mặc định MKV để copy nhiều codec audio; MP4 chỉ khi container hỗ trợ mọi audio stream. Ví dụ compositor chỉ hỗ trợ CFR SDR không rotation, timestamps gần zero. HDR/VFR/timecode/phụ đề cần adapter mở rộng; không silently drop nếu người dùng yêu cầu giữ các stream đó.

FFmpeg graph nền và overlay cùng origin, `overlay=eof_action=pass:repeatlast=0:shortest=0`, tắt tự chọn streams; map filtered video + `0:a?`, `-c:a copy`, `-c:v libx264`, `-crf 18`. Không dùng `-shortest`: audio không bị cắt theo kết thúc overlay. Bản xuất không auto thêm SFX/audio. Không dùng `-c:v copy` sau filter.

PNG RGBA là đường chuẩn. ProRes 4444 alpha có thể thay thế để giảm số file, nhưng phải kiểm pixel format/alpha. WebM alpha cần test decoder thực tế; không mặc định cho pipeline FFmpeg. Render một đoạn có nền khác nhau để bắt lỗi black background/premultiplied alpha. Output SDR yuv420p có thay đổi màu/quantization do encode; giữ tags không đủ để bảo toàn HDR.

Scale up: render theo active event windows với bảng global offsets; dựng overlay transparent full timeline hoặc FFmpeg movie branches với setpts offset. Không concatenate riêng các vùng có overlay vì sẽ làm mất thời gian trống. Hash event props + template version + fps + font + dimensions để chỉ rerender vùng đổi. MVP full sequence đơn giản hơn, nhưng disk lớn; probe dung lượng trước render.
