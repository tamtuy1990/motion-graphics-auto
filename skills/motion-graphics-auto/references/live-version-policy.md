# Kiểm tra GitHub Releases mỗi ngày

## Quy tắc tra cứu trong DeepSeek Harness

Trước công việc cài đặt, nâng cấp hoặc chọn API của Remotion/HyperFrames, gọi tool `motion_graphics_auto_check_releases` đúng một lần trong ngày theo múi giờ `Asia/Ho_Chi_Minh`. Tool chỉ gọi hai endpoint cố định:

- Remotion: https://api.github.com/repos/remotion-dev/remotion/releases/latest
- HyperFrames: https://api.github.com/repos/heygen-com/hyperframes/releases/latest

Kết quả được lưu chung cho mọi job/profile tại `$DSH_HOME/cache/motion-graphics-auto/github-release-cache.json` (mặc định `~/.dsh/cache/...`). Những lần gọi sau trong cùng ngày trả về cache, không gửi request GitHub mới. Cache chứa cả lỗi của lần kiểm tra để tránh retry ẩn trong ngày. Gói này mang theo snapshot được xác minh ngày 13/10/2026 để lần dùng đầu tiên trong ngày đó không cần tra lại.

Nếu tool trả `not_checked`, `check_incomplete`, `partial` hoặc `checked_but_cache_write_failed`, báo đúng trạng thái; không tuyên bố đã xác minh đủ hai phiên bản và không tự lặp lại request hôm đó. Nếu cần chọn phiên bản cho một project đã pin, giữ nguyên lockfile cho đến khi người dùng yêu cầu nâng cấp hoặc quyết định tương thích được kiểm tra.

`releases/latest` là latest stable GitHub Release của repository; đây không nhất thiết là tag prerelease mới nhất hoặc phiên bản `npm latest`. Khi thực sự cài/nâng cấp, kiểm tra package names và versions cần dùng, peer dependencies, Node engines, breaking changes, licensing, codecs, OS/GPU và alpha/audio needs từ nguồn tương ứng. Ghi tag GitHub, package versions đã pin, compatibility decision, ngày kiểm tra và smoke-render vào job manifest. Không tự nâng cấp chỉ vì release mới xuất hiện.

Không có lịch chạy nền. Việc kiểm tra xảy ra khi agent gọi tool ở job renderer đầu tiên trong ngày; plugin không tự gọi DeepSeek và không tự cài/nâng cấp dependencies.

## Snapshot đã xác minh

GitHub Releases được kiểm tra ngày 13/10/2026:

- Remotion: `v4.0.535` — https://github.com/remotion-dev/remotion/releases/latest
- HyperFrames: `v0.8.150` — https://github.com/heygen-com/hyperframes/releases/latest

Snapshot được lưu trong `github-release-cache.json`. Không dùng nó sau ngày 13/10/2026; tool kiểm tra lại khi ngày địa phương đổi.
