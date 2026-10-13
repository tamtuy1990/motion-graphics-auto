# Dùng toàn bộ ảnh và video đã có trong dự án

## Hai đầu vào hình ảnh

Một job có thể nhận video đã dựng (base timeline) và cả thư mục media của dự án: footage gốc, ảnh, logo, scan tài liệu, biểu đồ nguồn, v.v. Video dựng là trục thời gian; kho media là các nguồn hình để tìm shot thay thế kiểu cutaway hoặc các lớp phụ như PiP, ảnh chồng, split-screen và evidence cards. Gốc luôn bất biến.

Mặc định giữ thứ tự shot, âm thanh và nhịp timeline của video dựng. Có thể đặt asset lên phần hình tại câu phù hợp; cutaway thay hình tạm thời trong khoảng đó nhưng base audio vẫn tiếp tục. Chỉ recut, reorder hoặc thay hẳn shot khi người dùng yêu cầu rõ. Clip được thêm tắt audio source mặc định để không đè narration/music.

## Inventory local

1. Quét các file user đã cung cấp trong project scope. Không tự quét home/network hoặc tải lại tài sản từ YouTube.
2. Tạo asset ID ổn định, SHA-256, relative path, media kind, duration/dimensions/FPS, orientation, codec, transparency, audio tracks, nguồn/quyền nếu có. Không dùng tên file làm nhận dạng duy nhất.
3. Sinh thumbnail/contact sheet cho hình và video. Với video lấy một vài frame rải theo thời gian/shot; lưu sample timestamps. Nếu có scene-cut detection local, dùng để lấy keyframes. Không gửi file video dài/raw frame dump vào planner.
4. Tạo compact catalog: asset ID, tên file, duration/dimensions, sample frame refs, user description/metadata và trạng thái rights. Model có thể nhận contact sheets nếu endpoint multimodal được cấu hình; nếu không thì dựa vào user metadata/captions và không khẳng định đã nhìn thấy hình. Hình gửi API vẫn là request phụ phí/quota của provider nhưng thuộc cùng một lần planning call nếu endpoint nhận được.
5. Planner tham chiếu asset IDs và source time ranges; deterministic code kiểm file/hash/duration, trim hợp lệ, placement bounds, duplicate usage và protected picture/audio. Missing IDs phải bị reject.

Nếu bin lớn, local prefilter candidate assets theo tags/filename/user metadata, aspect ratio/duration và optional local embeddings. Giữ candidate choice rộng đủ; ghi `candidate_pool` để biết các asset nào model đã được cho xem. Không bí mật chỉ đưa một asset rồi nói AI đã chọn từ toàn project.

## Kiểu placement

| Operation | Hành vi | Âm thanh |
|---|---|---|
| `image_overlay` | ảnh asset đặt trên base, có fit/opacity | không đổi |
| `picture_in_picture` | khung footage/ảnh trong vùng an toàn | audio asset tắt |
| `cutaway` | footage/ảnh phủ hình base tạm thời, có source in/out | base audio tiếp tục |
| `split_screen` | chia frame cho base và asset hoặc hai assets | base audio tiếp tục |
| `graphic` | chart/card/callout/diagram | không đổi |
| `visual_effect` | effect preset áp dụng khoảng frame trên base/overlay | không đổi |

Effect parameters là whitelist data: opacity, scale, crop, position, blur radius/color preset và motion curve. Không arbitrary FFmpeg filter strings, CSS, JSX, URLs hay executable code trong model output. Effect mới cần preset ID + deterministic implementation + QA fixture.

## Timeline và xử lý

Asset placement có hai đồng hồ: source in/out của media phụ và target frame trên video base. Resolver đổi sang rational frames/PTS, clamp/validate trim, tạo các track layer order. Cutaway mute asset audio; overlay video cũng tắt audio. Placement trùng nhau được phép nếu layer order rõ và không che protected zones; base audio được map một lần nguyên trạng.

Renderer assembly: base video → time-local effects → assets/cutaways/layers theo z-order → graphic alpha → final encode. Nhiều track có thể cần FFmpeg `filter_complex` branches hoặc compositor frame-based; sample compositor hiện tại chỉ xử lý một full-frame RGBA overlay trên CFR SDR, nên không thể tuyên bố đã thực thi cutaway/PiP/effect. Các operation mới cần renderer và QA bổ sung. Codec/container/audio stream invariants từ architecture vẫn áp dụng.

## Tìm tư liệu ngoài

Chỉ chạy web/YouTube research khi user bật mode này hoặc asset pool không đáp ứng và user yêu cầu research. Search results là ứng viên; quyền xem công khai không trao quyền download/reuse. Ưu tiên asset đã cung cấp. Xem thêm [media research](media-research.md).
