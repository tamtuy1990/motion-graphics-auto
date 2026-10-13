# Ví dụ end-to-end: từ kịch bản tới storyboard

Đây là ví dụ giả định để giải thích cách AI Director ra quyết định. Kịch bản, số liệu, nhân vật và nguồn dưới đây đều bịa để minh họa, không phải dữ liệu nghiên cứu. Timing chỉ là số giả lập; job thật lấy từ aligner/STT.

## Kịch bản đầu vào

```text
s000001 00:00.8–00:04.0: Trong ba năm, khu phố thay đổi rất nhanh.
s000002 00:04.1–00:08.0: Số cửa hàng giảm từ 120 xuống còn 75.
s000003 00:08.1–00:12.0: Trong khi đó, giá thuê mặt bằng tăng từ 10 lên 14 triệu đồng mỗi tháng.
s000004 00:12.1–00:17.0: Nhiều gia đình đã sống ở đây qua nhiều thế hệ.
s000005 00:17.1–00:22.0: Khi cửa cuốn cuối cùng hạ xuống, con phố dường như cũng khép lại một chương.
s000006 00:22.1–00:26.0: Nhưng con số không cho biết ai đã phải rời đi.
```

Giả định job có transcript này, tiếng Việt, video đã dựng, audio final và một bảng dữ liệu được cung cấp chứa chính xác hai cặp số ở câu 2–3. Không có địa chỉ hoặc lịch sử tên cửa hàng trong dữ liệu nguồn. Không có quyền tải lại cảnh phim từ YouTube.

## DeepSeek đọc mạch chuyện trước

Mạch khái quát: khu phố đổi thay → hai xu hướng đo được trái chiều → cư dân có lịch sử gắn bó → mất mát mang tính con người → số liệu không thể kể hết trải nghiệm. Vì vậy không nên bật một chart ở mọi câu.

| Câu | Chức năng trong chuyện | Đề xuất của AI | Trạng thái trong renderer hiện tại |
|---|---|---|---|
| s000001 | Mở chủ đề thay đổi | Dùng cảnh phố hiện có, giữ tiêu đề ngắn hoặc không thêm gì nếu hình đã nói đủ | Không graphic; câu vẫn được giữ trong manifest |
| s000002 | Chứng minh cửa hàng giảm | Counter 120→75, nhãn “cửa hàng” | Có `counter-v1`; nguồn số liệu phải gắn ID |
| s000003 | Tạo tương phản với câu trước | Hai thẻ hoặc bố cục đối chiếu: cửa hàng ↓, giá thuê ↑; dùng hai cặp số đã cho, đồng bộ highlight khi đọc | Bố cục cặp chưa có template trực tiếp; dùng hai counter nếu layout đặt cạnh nhau vượt QA, nếu không đánh dấu component cần thêm |
| s000004 | Gợi chiều dài lịch sử con người | Tìm ảnh/video phố hoặc cửa hàng cũ, có license rõ; có thể dùng một ảnh tư liệu cạnh cảnh hiện tại | Cần bật module media research; nếu chưa có asset hợp pháp thì không tự tìm cách tải video YouTube |
| s000005 | Cao trào cảm xúc/ẩn dụ | Đề xuất cửa cuốn khép lại thành một “chương sách” đang đóng, chỉ như hình tượng minh họa; không vẽ như sự kiện có thật | Cần `symbolic-transition`/layer animation chưa được implement; proposal `requires_component`, có thể fallback bằng cảnh video gốc |
| s000006 | Hạ kết, khẳng định giới hạn của số liệu | Để cảnh/khuôn mặt hoặc âm thanh dẫn dắt; không phủ chart lên câu này | `no_graphic_needed`, giữ nguyên câu trong danh sách |

## Một phần kế hoạch AI có thể trả

Đây là JSON **ở lớp đề xuất của planner**, để người đọc thấy ý định. Nó chưa phải `storyboard.json` hợp lệ với schema/renderer hiện tại; các ý tưởng unsupported không được chuyển thẳng vào bước render.

```json
{
  "version": "director-plan-1",
  "coverage": [
    {"sentenceId":"s000001","status":"no_graphic_needed","reason":"Cảnh mở đã truyền đạt khu phố đổi thay."},
    {"sentenceId":"s000002","status":"graphic","eventId":"e000001"},
    {"sentenceId":"s000003","status":"graphic","eventId":"e000002","requiresComponent":"comparison-cards-v1"},
    {"sentenceId":"s000004","status":"asset_search","searchGroupId":"q000001"},
    {"sentenceId":"s000005","status":"needs_review","requiresComponent":"symbolic-transition-v1"},
    {"sentenceId":"s000006","status":"no_graphic_needed","reason":"Để câu kết có khoảng lặng."}
  ],
  "events": [
    {
      "id":"e000001",
      "sentenceId":"s000002",
      "narrativeFunction":"cho thấy quy mô giảm",
      "visualIntent":"Làm thay đổi 120→75 dễ thấy trong lúc nghe câu.",
      "template":"counter-v1",
      "evidence":{"dataId":"demo-store-counts","quote":"Số cửa hàng giảm từ 120 xuống còn 75."},
      "values":{"from":120,"to":75,"unit":"cửa hàng"},
      "cueWord":"120",
      "durationSeconds":3.5
    }
  ],
  "searchGroups": [
    {"id":"q000001","sentenceIds":["s000004"],"query":"archival street shop storefront old neighborhood; Vietnamese city only if source/context confirms"}
  ],
  "requiresComponents": [
    {"id":"comparison-cards-v1","reason":"Muốn cho thấy hai xu hướng trái chiều cùng lúc."},
    {"id":"symbolic-transition-v1","reason":"Ẩn dụ cửa cuốn chuyển thành chương sách, không phải cảnh thật."}
  ]
}
```

## Code xử lý gì sau response

1. Ghép từng event với `sentenceId`, `wordIds` và timing thật; kiểm evidence/number với bảng nguồn. Không cho phép AI tự đặt thời điểm bằng cách nhìn số giây ước lượng nếu đã có word alignment.
2. Kiểm coverage: sáu câu phải có đủ sáu trạng thái; `no_graphic_needed` khác với chưa xử lý. Kiểm template/props, vùng phụ đề, overlap và quyền asset.
3. Chỉ đưa `e000001` vào storyboard hiện tại nếu evidence, cue và layout đạt validation. Các event cần component mới được báo trong proposal, không đưa vào renderer giả.
4. Remotion dựng component đã hỗ trợ. FFmpeg ghép overlay vào bản xuất và sao chép audio. QA kiểm frame đúng cue, chữ, alpha, output stream và báo mọi ý tưởng chưa thực hiện.

Toàn bộ kịch bản có thể đi trong một request. Nếu cần tìm ảnh, chương trình tra cứu sau planner bằng truy vấn nhóm. Một lượt follow-up (nếu bật) có thể chọn các candidates từ nhiều câu và xử lý toàn bộ vấn đề ngữ nghĩa còn lại trong cùng một payload; tìm thấy URL không tự cấp quyền tải/sử dụng.

## Nếu có full bin của dự án

Giả sử thư mục dự án đã có `street_old_01.jpg`, `shop_shutter_broll.mp4`, `family_archive_02.jpg` và video final. Local inventory tạo IDs/hash trước khi gọi model:

```json
{
  "version":"1.0",
  "projectId":"neighborhood-film",
  "assets":[
    {"assetId":"a000001","kind":"image","relativePath":"assets/street_old_01.jpg","sha256":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","durationSeconds":null,"width":1920,"height":1080,"fpsNum":null,"fpsDen":null,"hasAlpha":false,"sampleFrames":[{"timeSeconds":0,"relativePath":"work/contact-sheets/a000001.jpg"}],"description":"Phố cũ, ảnh lưu trữ do người dùng cung cấp","tags":["street","archive","neighborhood"],"rightsStatus":"user-provided","audioStreamCount":0},
    {"assetId":"a000002","kind":"video","relativePath":"assets/shop_shutter_broll.mp4","sha256":"bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb","durationSeconds":7.2,"width":1920,"height":1080,"fpsNum":30,"fpsDen":1,"hasAlpha":false,"sampleFrames":[{"timeSeconds":1.2,"relativePath":"work/contact-sheets/a000002_01.jpg"},{"timeSeconds":5.1,"relativePath":"work/contact-sheets/a000002_02.jpg"}],"description":"Cửa cuốn cửa hàng từ mở sang đóng","tags":["shop","shutter","closing"],"rightsStatus":"user-provided","audioStreamCount":1},
    {"assetId":"a000003","kind":"image","relativePath":"assets/family_archive_02.jpg","sha256":"cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc","durationSeconds":null,"width":1600,"height":1200,"fpsNum":null,"fpsDen":null,"hasAlpha":false,"sampleFrames":[{"timeSeconds":0,"relativePath":"work/contact-sheets/a000003.jpg"}],"description":"Ảnh gia đình trước một cửa hàng; nội dung chỉ là mô tả sơ bộ","tags":["family","store","archive"],"rightsStatus":"user-provided","audioStreamCount":0}
  ]
}
```

Hash trong ví dụ chỉ là chuỗi minh họa, không phải checksum thật. Planner nhận catalog và contact sheets nếu API vision được cấu hình, rồi có thể đề xuất:

```json
{
  "id":"edit_0001",
  "sentenceId":"s000004",
  "startFrame":405,
  "endFrame":480,
  "layer":2,
  "visualIntent":"Gắn lời kể nhiều thế hệ với ảnh gia đình có sẵn.",
  "operation":"picture_in_picture",
  "assetId":"a000003",
  "sourceInSeconds":null,
  "sourceOutSeconds":null,
  "box":{"x":0.60,"y":0.13,"w":0.32,"h":0.34},
  "fit":"contain",
  "opacity":1,
  "muteAssetAudio":true
}
```

Planner cũng có thể đề xuất `a000002` làm cutaway trong lúc câu s000005 nói tới cửa cuốn. Resolver xác minh trim/time và đặt footage lên hình trong khoảng đó; audio gốc của video final vẫn tiếp tục. Nếu asset không khớp nội dung, vùng ảnh che mặt/phụ đề hoặc hash sai, reject placement và báo cụ thể.

Catalog và edit-plan schema hiện đã có trong package. Ví dụ operation nói trên chưa chạy qua compositor hiện tại: renderer đang được khởi đầu với full-frame graphic overlay. Asset inventory/contact sheet, PiP/cutaway/effect runtime và edit-plan validator là phần cần implement ở milestone project-asset pipeline.

## Điều ví dụ này làm rõ

DeepSeek phải đọc được quan hệ giữa các câu và chọn nhiều ngôn ngữ thị giác khác nhau trong cùng video: số liệu, đối chiếu, tư liệu, ẩn dụ và khoảng lặng. Nó không bị bó vào năm template hiện có. Nhưng khả năng nghĩ ra hình khác và khả năng phần mềm vẽ hình đó là hai bước khác nhau: cần registry primitive/composition rộng hơn để những đề xuất mới chạy được.
