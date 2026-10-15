# Editorial craft — A-roll / B-roll, nhịp cắt, và chín cơ chế

File này bù phần **thiếu nhất** của bộ skill. Các reference khác dạy *hợp đồng kỹ
thuật* (schema, timing, render). File này dạy **tư duy dựng hình** — thứ quyết
định video đẹp hay dở, và là chỗ một agent đi theo công thức sẽ làm hỏng.

Đọc file này **trước khi** chọn dạng hình cho bất kỳ beat nào.

> **Quan trọng — đọc kèm [inventing visuals](inventing-visuals.md).** Chín cơ chế
> ở §7 là **kết quả của việc suy nghĩ**, không phải cách suy nghĩ. Nếu chỉ tra
> bảng "câu này dạng gì" thì mãi chỉ xoay quanh chín thứ đó, và video vẫn đọc ra
> nhàm dù đã "đa dạng cơ chế". File `inventing-visuals.md` dạy quy trình năm bước
> để **nghĩ ra** hình cho từng đoạn, và ba mức sáng tạo (tra bảng / ghép có biến
> đổi / nghĩ mới). Mục tiêu: 70% mức A · 25% mức B · **5% mức C** — tức trong
> 5 phút phải có **1–2 đoạn được nghĩ riêng hoàn toàn**. Đó là những đoạn người
> xem nhớ.

> Nguồn: rút từ một job thật bị phản hồi nặng ("lặp công thức", "không biết làm
> A-roll/B-roll", "bị rung"), sau đó đối chiếu với một bộ 40 ảnh tham chiếu do
> người dùng cung cấp và bản master prompt 1 028 dòng kèm theo. Mọi luật dưới
> đây đều có bằng chứng từ lần hỏng đó hoặc từ ảnh tham chiếu.

---

## 0. Năm lỗi chết người, và cách tránh

Đây là năm lỗi đã ship thật. Mỗi cái đều **qua được `check`** — không có
validator nào bắt được. Chỉ mắt người mới bắt.

| Lỗi | Dấu hiệu | Cách tránh |
|---|---|---|
| **Rung** | nền giật, chóng mặt | xem §4 |
| **Không có B-roll** | video phẳng, chỉ một tuyến nền | xem §2 |
| **Chọn hình theo số file** | hình không khớp lời | xem §1 |
| **Lặp một công thức** | 47% event cùng một dạng | xem §3, §7 |
| **Rải accent** | nhiều màu nhấn cùng frame | xem §5 |

---

## 1. Chọn hình theo NGHĨA, không theo thứ tự file

**Lỗi đã ship:** agent nhận 110 file media, cho *file thứ n chạy ở slot thứ n*.
Kết quả: ảnh ngân hàng ghép vào câu nói về cổ phiếu, ảnh xe hơi ghép vào câu nói
về sofa. Hình và lời không khớp — đây là gốc của "chán", và nó không lộ ra trong
bất kỳ frame đơn lẻ nào.

**Luật:** trước khi chọn hình, phải biết mỗi file **chứa cái gì**. Với một bộ
media dày, hãy:

1. **Nhìn** contact sheet của toàn bộ media (không đọc tên file).
2. **Gán nhãn nội dung** cho từng file bằng lời — "ngân hàng, quầy giao dịch,
   nhân viên đưa giấy". Lưu thành `media-labels.json`.
3. **Suy bối cảnh từ câu thoại**, rồi chọn file có nhãn khớp.

Nhãn nội dung là thứ cho phép chọn hình theo nghĩa. Không có nó thì chỉ còn cách
chọn theo số — và đó là lỗi.

**Cảnh báo:** đừng kết luận vội rằng một bộ ảnh "lặp lại". Nhìn kỹ thường thấy
nó đa dạng hơn tưởng: cùng nhân vật nhưng khác bối cảnh (ngân hàng / công viên /
xe hơi / sofa / bếp / đêm khuya). Vấn đề nằm ở **cách gán**, không ở kho.

---

## 2. A-roll và B-roll

### Định nghĩa dùng được

| | A-roll | B-roll |
|---|---|---|
| Là gì | mạch chính, mang câu chuyện | hình cắt vào minh hoạ MỘT ý trong câu |
| Chọn theo | **phân cảnh ngữ nghĩa** | **khoá ngữ nghĩa của câu** |
| Thời lượng | 3–8s, đủ để đọc | 1,5–3,5s |
| Quan hệ với lời | chạy song song | **neo đúng từ được nói** |

### B-roll không cần media mới

Ba cách lấy B-roll từ chính kho có sẵn:

1. **Crop cận** — từ một khung rộng lấy ra chi tiết: bàn tay trên sổ, màn hình
   điện thoại, tờ giấy, cốc nước. **Một file thành 2–3 hình khác cỡ khung.**
   Đây là cách mạnh nhất và cũng dễ bỏ quên nhất.
2. **Dùng lại ở đoạn khác với nghĩa khác** — cùng cảnh ngân hàng, lần đầu là hy
   vọng, lần sau là nỗi lo. Người xem không nhận ra vì bối cảnh đã đổi.
3. **Đảo thứ tự** để hình theo nghĩa, không theo số file.

### Luật chọn B-roll

> Chỉ cắt B-roll khi lời thoại nhắc tới **một thứ cụ thể nhìn thấy được**.

Nếu câu chỉ nói cảm xúc ("lúc đó thật sự là như vậy") thì **để A-roll chạy,
không cắt gì**. Cắt vào là phá. Thà thiếu còn hơn cắt bừa.

### Cảnh footage sạch — cơ chế bị bỏ quên nhiều nhất

Trong 40 ảnh tham chiếu, cảnh **đẹp nhất** là cảnh **không có infographic**:
footage toàn màn hình + chỉ một card định danh nhỏ ở góc (sọc accent dọc, tên
địa điểm/chủ thể, một dòng chú thích, credit nhỏ).

> ⚠ **ĐỌC KỸ: "không graphic" KHÔNG có nghĩa là "ảnh gốc để nguyên".**
>
> Đây là chỗ hiểu sai tai hại nhất, và đã hiểu sai thật một lần. Cảnh footage sạch
> là cảnh **không có đồ họa thông tin** — nhưng ảnh vẫn phải đi qua **biến đổi**:
> crop lại khung, chuyển động camera chậm, grade màu, card định danh. Bốn thứ đó
> đã là ba–bốn lớp biến đổi.
>
> Để ảnh gốc nguyên bản **không phải là phong cách** — đó là rủi ro bản quyền và
> bị YouTube đánh reused content. Xem [faceless transform](faceless-transform.md).

Luật:
- **Không** đặt thanh, số, biểu đồ lên cảnh này.
- Card là **bối cảnh**, không phải nhân vật chính — entrance ngắn, tinh tế.
- Lớp phủ tối **rất nhẹ** — mục đích là để footage tự nói, không phải làm tối nó.
  (Nhưng vẫn phải có grade; "nhẹ" khác "không có".)
- **Bắt buộc ≥ 2 lớp biến đổi** như mọi cảnh khác. Thường là 3–4: crop lại + camera
  chậm + grade + card.
- Ảnh minh hoạ phải ghi `참고 사진` / "ảnh minh hoạ", **không** ghi `실제 사진`
  nếu chưa xác minh.

Tỉ lệ nên có: **≥ 25% số cảnh** là footage sạch hoặc gần sạch.

---

## 3. Nhịp cắt — bốn mức, không phải một hằng số

**Lỗi đã ship:** cắt đều 2,67s/ảnh suốt 5 phút. Đó là lỗi thiết kế: *nhịp là thứ
để kể chuyện, không phải hằng số*.

| Mức | Độ dài | Dùng khi |
|---|---|---|
| **Chậm** | 6–10s | đoạn cảm xúc, câu triết lý, kết chương. Ít cắt = để người xem nghĩ |
| **Thường** | 3–5s | kể chuyện bình thường |
| **Nhanh** | 1,5–2,5s | liệt kê, leo thang, "và rồi… và rồi…" |
| **Dồn** | 0,7–1,2s | cao trào, cắt như trống — **cả phim chỉ 1–2 lần** |

**Luật:** nhịp phải **thay đổi theo nội dung**. Đoạn leo thang thì cắt mau dần;
đoạn buông lơi thì cắt thưa hẳn. Cả phim cùng một nhịp thì dù hình đẹp vẫn đọc
ra "máy".

**Nghiệm thu:** đếm độ lệch chuẩn độ dài cảnh. Nếu gần 0 → nhịp đều tăm tắp →
FAIL. Cần ít nhất **3 mức nhịp** trong 5 phút.

Ba "nhiệt độ" thị giác phải luân phiên, không đặt 5 cảnh infographic nhiều chữ
liền nhau:

| Nhiệt độ | Là gì | Tỉ lệ |
|---|---|---|
| **LẠNH** | footage sạch, không/gần như không chữ | ~35% |
| **ẤM** | footage + một card nhỏ / headline / quote | ~35% |
| **NÓNG** | infographic đầy: thanh, timeline, pictogram, bảng | ~30% |

---

## 4. Chống rung — luật cứng

**Lỗi đã ship:** mỗi ảnh được cho Ken Burns zoom 6,5% trong slot 2,67s, **lại
thêm một lớp camera 2% nữa**. Hai lớp scale lồng nhau, đổi hướng zoom mỗi 2,67s.
Đó chính là cái "rung" người xem thấy.

Luật:

1. **Cảnh ngắn (< 5s): KHÔNG camera.** Cắt là cắt, ảnh đứng yên hoàn toàn.
2. **Cảnh dài (≥ 5s): đúng MỘT chuyển động camera**, chạy suốt cảnh, **không
   đổi hướng giữa cảnh**. Biên độ ≤ 3%.
3. **Không bao giờ hai lớp scale lồng nhau** (camera ngoài + zoom trong).
4. Pan ngang chỉ **dịch chuyển** (`xPercent`), không cộng scale.
5. B-roll ngắn chỉ fade + dịch 12–16px. **Không zoom.**
6. Với ảnh tĩnh, Ken Burns **nhẹ** (1→1.02 hoặc 1.04) **chỉ trong đoạn dài** —
   và ảnh vẫn cần label/source, không được giả là video quay thật.

---

## 5. Một màu accent mỗi frame

Đây là luật bị vi phạm nặng nhất trong lần ship hỏng: accent rải khắp banner,
counter, callout, khối, glint, underline.

Bằng chứng từ ảnh tham chiếu:

| Ảnh | Nội dung | Accent ở đâu |
|---|---|---|
| hai thanh so sánh | A vs B | thanh A xanh, thanh B đỏ — **không thêm gì khác** |
| biểu đồ nhiều năm | 2017 vs 2023 | 2017 **xám**, 2023 **đỏ** |
| biểu đồ bậc thang | 5 cột | **tất cả xám**, cột cuối **đỏ** |
| pictogram | 10 người → 1 | **vàng** cho cái còn, **xám** cho cái mất |

**Luật:** nền và dữ liệu trung tính = **xám/trắng**. Accent = **đúng MỘT thứ**
đang được lời thoại nói tới. Nhiều hơn một accent mỗi frame = rẻ tiền.

---

## 6. State xuyên cảnh — thứ mạnh nhất và dễ bỏ nhất

Trong 40 ảnh tham chiếu có **bốn ảnh là CÙNG một bảng xếp hạng** ở bốn thời điểm:
hạng 7 mở → hạng 6 mở → hạng 5, 4, 3 mở dần. **Hạng đã mở KHÔNG BAO GIỜ trở lại
dấu `?`.**

Đó là **state xuyên cảnh**. Nó mạnh vì tạo suspense: người xem chờ xem hạng tiếp
là ai. Và nó là thứ một agent làm theo công thức sẽ không bao giờ tạo ra — vì mỗi
graphic của nó là một khối độc lập hiện ra rồi biến mất.

Luật:
- Nếu một đối tượng được nói tới **nhiều lần** trong video, nó phải **tồn tại và
  tiến hoá**, không được dựng lại từ đầu mỗi lần.
- Trạng thái là **hàm của thời gian**: `stateAtTime(frame)`. Deterministic.
- Quay lại bảng sau: hạng cũ **vẫn còn tên**.

---

## 7. Chín cơ chế — chọn theo CHỨC NĂNG KỂ CHUYỆN

**Lỗi đã ship:** 49 event, nhưng **23 cái (47%)** cùng một dạng "chữ đặt ở một
góc". Toạ độ lặp y hệt nhau. Người xem thấy cùng một thứ 49 lần.

Gốc của lỗi: đổi *template* nhưng giữ nguyên *bố cục*. Đổi tên không phải đổi
cách kể.

**Luật:** mỗi đoạn phải trả lời — *"hình này làm được việc gì mà lời thoại không
làm được?"* Nếu chỉ để "hiện chữ ra" thì **bỏ hình, để footage tự nói.**

**Nhưng bảng dưới đây là mức A.** Dùng nó cho đoạn thông tin bình thường, rồi
đọc [inventing visuals](inventing-visuals.md) để nâng một hai đoạn quan trọng
lên mức B/C. Tra bảng cho cả video = vẫn nhàm.

### Bảng tra: câu thoại → cơ chế

| Thoại nói về | Cơ chế | KHÔNG dùng |
|---|---|---|
| "A gấp N lần B" | **Thanh cùng scale** | hai counter cạnh nhau |
| "Năm X → năm Y" | **Trục thời gian vẽ dần**, mốc ló khi chạm | hai số đứng cạnh |
| "Hạng 7, hạng 6…" | **Bảng state**, mở dần, không reset | 7 card hiện cùng lúc |
| "Có thể A, hoặc B" | **Hai card đối**, cùng nền, cùng cỡ | một card hai dòng |
| "10 người còn 1" | **Pictogram**, vẽ tuần tự, xám dần | số 10 → 1 |
| "Giá 650 → 760" | **Trước/sau + con dấu** | một số 760 |
| "Ai đó nói rằng…" | **Quote card** (biến thể sáng hoặc tối) | banner chữ |
| "Cảnh này quan trọng" | **Footage sạch + card nhỏ** | thêm infographic |
| "Đổi chương" | **Intertitle** | headline |
| "Xu hướng nhiều năm" | **Biểu đồ bậc thang**, cột cuối đỏ | đường cong mượt |
| "Tăng/giảm %" | **Signed count**, giữ dấu cố định | số âm tăng từ −12.8 lên 0 |
| "Số tuyệt đối" | **Count-up rồi KHOÁ** | số nhảy không dừng |

### Chi tiết từng cơ chế

**Thanh cùng scale.** Hai thanh **ngang**, xếp trên/dưới, **cùng trục 0**, chia sẻ
`maxValue`. Thanh dài gấp N lần thì **trông phải dài đúng N lần**. Nhãn ở trái,
số ở phải. Thứ tự bắt buộc: thanh 1 grow → HOLD → thanh 2 grow → callout chốt.
**Tuyệt đối không** chuẩn hoá mỗi thanh theo giá trị riêng — 685.000 mà dài 60%
của 1.956.000 là *nhìn sai*.

**Trục thời gian vẽ dần.** Một đường ngang làm trục. Đường accent **chạy từ trái**,
và **mốc chỉ ló khi đầu đường chạm tới**. Mốc chưa tới **không tồn tại** — không
hiện chấm xám trước. Mỗi mốc: nhãn to trên, chú thích nhỏ dưới.

**Bảng state.** N ô xếp hàng. Hạng đã mở hiện tên thật; chưa mở hiện `?` lớn. Ô
đang nói có viền accent và hơi nổi. **Không reset.**

**Hai card đối.** Hai card **cùng nền, cùng màu chữ** — không tô khác nhau để
"phân biệt". Card 1 pop trước, card 2 vào khi lời nhắc. Cả **khung + chữ di
chuyển như MỘT khối**. Kết luận hiện sau cùng.

**Pictogram.** Icon vẽ **tuần tự**, không hiện cả loạt. Trạng thái đổi **khi lời
nói tới**. Nhóm giảm: icon chuyển **xám từng cái**, không xoá.

**Trước/sau + dấu.** Thứ tự **không được đảo**: giá cũ → gạch ngang khi lời nói
nó không còn → **mũi tên VẼ ra** → giá mới count → **dấu pop** có xoay nhẹ.

**Quote.** Hai biến thể **khác hẳn nhau**: (a) **trên footage** — card nền trắng
chữ đen, từ khoá đỏ, nguồn nhỏ dưới; (b) **trên nền tối** — chữ trắng + hạt bụi,
gạch chân mảnh, không khung. Đừng chỉ làm một biến thể rồi lặp 4 lần.

**Intertitle.** Nền tối hoàn toàn + hạt bụi seed cố định + typography lớn reveal.
**Cả phim 1–2 lần.**

**Biểu đồ bậc thang.** N cột, **tất cả xám**, cột cuối **đỏ** + badge. Mỗi cột
một nhãn năm. Đây là cách vẽ "xu hướng nhiều năm" mà không cần đường cong.

---

## 8. Không lộ thông tin trước

- Trước mốc thoại thì item **`visible = false`** — và nếu pipeline có nguy cơ lộ
  (snapshot, accessibility), thì **không mount DOM**, không phải `opacity: 0`.
- **Lead-in mặc định = 0** cho thông tin mới. Không "đón câu" bằng cách hiện sớm.
  (Lần ship hỏng dùng lead 6 frame — đó chính là đón câu.)
- Nếu một câu chứa nhiều keyword, **chia span** và reveal từng keyword.
- Chưa tới lượt thì **để trống**, không hiện `0` — hiện `0` đọc ra như dữ liệu
  là 0.

---

## 9. Nối cảnh — sáu cách, không phải cắt phũ

| Cách | Dùng khi |
|---|---|
| **Đẩy trắng (flash-cut)** | hai năng lượng gần nhau, đổi không gian |
| **Chuồn qua tối** | năng lượng cao → cao; trục chính của phim tối |
| **Nhả nét (focus pull)** | cùng không gian, đổi khối — không cắt hẳn |
| **Thẻ chữ trên nền tối** | cắt chương + nghỉ, gộp làm một |
| **Vung máy (whip-pan)** | đoạn nhanh, nhịp dồn |
| **Xuyên cửa sổ (mask-wipe)** | "mở cái này ra để vào thế giới của nó" |

**Một mối nối chỉ dùng một cách.** Hướng chuyển động phải **liên tục** giữa hai
cảnh (ra phải → vào từ phải).

---

## 10. Tự kiểm trước khi nộp

Trả lời từng câu, không cần viết dài:

- [ ] Có element nào hiện **trước** khi thoại nhắc không?
- [ ] Có element nào **đáng ra phải chạy/vẽ/đếm** nhưng chỉ fade-in không?
- [ ] Có cảnh nào quá nhiều chữ/đồ họa **đè lẫn nhau** không?
- [ ] Có dùng **một animation y hệt quá nhiều lần** liên tiếp không?
- [ ] Đã **nhìn** ít nhất 6 frame trải đều, hay chỉ chụp frame cuối?
- [ ] Có cảnh footage sạch nào không, và nó có **xem được** không?
- [ ] **Một accent mỗi frame** chưa?
- [ ] Có state nào **reset** đáng ra phải persist không?
- [ ] Nhịp có **nhiều mức** hay đều tăm tắp?
- [ ] Có cảnh ngắn nào bị **zoom** gây rung không?
- [ ] Có hình nào **không khớp nghĩa câu thoại** không?
- [ ] Hình có **mang nghĩa** không, hay chỉ là chữ đặt lên màn hình?

**Có lỗi nào ở nhóm trên thì sửa trước khi xuất.**

---

## 11. Đối chiếu nhanh: công thức vs tư duy

Bảng này để tự phát hiện khi đang đi theo công thức.

| Đi theo công thức | Đi theo tư duy |
|---|---|
| "Câu này dạng gì?" | "Câu này nên **thấy gì**?" |
| Đổi template, giữ bố cục | Đổi **cách kể** |
| Cảnh nào cũng cần graphic | ~25% cảnh **để footage tự nói** |
| File thứ n → slot thứ n | Chọn file theo **nghĩa câu** |
| Graphic hiện ra rồi biến mất | Đối tượng **tồn tại và tiến hoá** |
| Accent rải khắp nơi | **Một** accent, đúng cái đang nói |
| Cắt đều một nhịp | Nhịp **theo nội dung**, 3–4 mức |
| Zoom mọi ảnh | Ảnh ngắn **đứng yên** |
| `check` pass là xong | **Nhìn frame** mới biết |

`check` bắt được lỗi cú pháp, tràn khung, va chạm. Nó **không** bắt được: hình
không khớp lời, lặp công thức, rải accent, nhịp đều, rung do zoom chồng lớp,
hay mặt người bị che. Những thứ đó chỉ **mắt người** bắt được.
