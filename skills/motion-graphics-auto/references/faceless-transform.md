# Faceless — biến đổi tài sản, không chỉ trang trí

## Vì sao có file này

Bộ skill này dạy chọn asset theo **giấy phép** (được dùng hay không). Nhưng với
một kênh faceless, câu hỏi thứ hai quan trọng ngang: **hình này đã đủ khác chưa?**

Hai vấn đề khác nhau, và bộ skill cũ chỉ giải quyết cái thứ nhất:

| | Câu hỏi | Nếu sai |
|---|---|---|
| **Giấy phép** | mình có **quyền** dùng hình này không? | gậy bản quyền, kiện |
| **Biến đổi** | hình này đã **đủ khác** bản gốc chưa? | YouTube đánh **reused content**, không kiếm tiền được |

Một ảnh stock mua hợp lệ vẫn có thể khiến video bị đánh reused content, nếu nó
xuất hiện **nguyên bản** và **không thêm giá trị gì**. Ngược lại, một ảnh lấy từ
nơi khác vẫn qua được nếu đã được **xử lý thành thứ mới**.

> **Hệ quả thực tế: mọi hình trong video đều phải qua xử lý.** Không có hình nào
> được đứng nguyên. Kể cả cảnh "đơn giản" — cũng phải có ít nhất một lớp biến đổi.

Đây không phải chuyện thẩm mỹ. Đây là **điều kiện để video tồn tại**.

---

## 1. Vì sao "để nguyên cho đẹp" là sai

Trực giác thường nói: *ảnh này đẹp rồi, thêm hiệu ứng vào là làm hỏng.*

Trực giác đó sai với faceless, vì ba lý do:

**Lý do 1 — trùng khớp.** Nếu ảnh đến từ stock, từ nguồn công cộng, hoặc từ một
kênh khác, thì **nhiều người khác cũng đang dùng đúng ảnh đó**. Hệ thống nhận
dạng nội dung so khớp hình ảnh, không so khớp ý tưởng. Ảnh càng phổ biến, rủi ro
càng cao.

**Lý do 2 — thiếu giá trị gia tăng.** Tiêu chí "reused content" không hỏi *bạn có
quyền không*, mà hỏi *bạn có thêm gì không*. Một video ghép ảnh gốc + nhạc + đọc
lời là đúng định nghĩa reused content, dù mọi ảnh đều hợp lệ.

**Lý do 3 — ảnh do AI tạo cũng không miễn.** Ảnh AI tạo từ một prompt phổ biến có
thể trùng với hàng trăm video khác dùng cùng prompt/model. "Không vi phạm bản
quyền của ai" không có nghĩa là "không bị đánh trùng".

---

## 2. Năm lớp biến đổi — mỗi hình phải có ÍT NHẤT HAI

Không phải chọn một. Phải chồng lên nhau. Mỗi lớp làm hình khác đi ở một khía
cạnh khác nhau (không gian, thời gian, màu, bố cục, ngữ cảnh).

| Lớp | Làm gì | Ví dụ |
|---|---|---|
| **1. Khung** | đổi bố cục — crop, tỉ lệ, vị trí | crop cận chi tiết; ảnh chỉ chiếm nửa khung |
| **2. Chuyển động** | đổi trạng thái theo thời gian | đẩy/kéo chậm, pan, phần tử vẽ dần |
| **3. Màu** | đổi tông | grade, overlay màu, tương phản |
| **4. Chồng lớp** | thêm thứ lên trên | chữ, số, đường vẽ, khối, đồ họa |
| **5. Ngữ cảnh** | đổi nghĩa bằng thứ đi kèm | cắt ghép hai hình, đặt cạnh dữ liệu, đổi thứ tự |

**Luật cứng: mỗi hình ≥ 2 lớp.** Hình nào chỉ có 1 lớp (ví dụ chỉ chèn chữ lên
ảnh gốc) → **chưa đủ**, phải thêm.

**Và: không dùng cùng một tổ hợp lớp cho mọi hình.** Nếu mọi ảnh đều "crop 1.1×
+ đẩy chậm + grade xanh" thì đó là **một công thức** — vừa nhàm vừa dễ bị nhận ra
là sản xuất hàng loạt.

---

## 3. Sáu cách biến đổi, xếp theo mức độ thay đổi

Từ nhẹ tới mạnh. Càng xuống dưới càng an toàn nhưng càng tốn công.

### (1) Đổi khung — nhẹ nhất, nhanh nhất

Crop khác đi, đổi tỉ lệ, để ảnh chỉ chiếm một phần khung, hoặc đặt trong khung
bo góc. Đây là lớp **bắt buộc tối thiểu** khi không làm gì khác.

> Ví dụ: ảnh gốc 16:9 → crop cận một chi tiết thành 4:3, đặt lệch trái, chừa nửa
> phải cho chữ.

### (2) Đổi thời gian — chuyển động

Đẩy/kéo cực chậm, pan, hoặc để phần tử vẽ dần. Đây là lớp biến đổi **theo thời
gian** — thứ mà ảnh gốc không có.

> Luật chống rung vẫn áp: cảnh ngắn thì một chuyển động nhẹ, không zoom liên tục.

### (3) Đổi màu — grade

Đổi tông màu, độ tương phản, thêm overlay. Rẻ, hiệu quả, và **hợp nhất toàn video**
(vì nó tạo tông thống nhất cho kênh).

### (4) Thêm lớp thông tin — chồng đồ họa

Chữ, số, đường vẽ, khối, mũi tên. Đây là lớp biến đổi **mạnh về ngữ nghĩa** —
hình gốc trở thành *nền* cho một thông điệp mới.

### (5) Đổi bố cục — cắt ghép nhiều hình

Hai hình đặt cạnh, chồng lên nhau, hoặc cắt thành lưới. Hình gốc không còn tồn
tại như một thực thể nguyên vẹn.

### (6) Đổi ngữ cảnh — tái sử dụng có chủ đích

Cùng một hình, dùng ở hai đoạn với hai nghĩa khác nhau (nhờ hình đi kèm khác). Đây
là lớp mạnh nhất, và nó cũng là **state xuyên cảnh** đã nói ở
[editorial-craft](editorial-craft.md).

---

## 4. "Cảnh để footage tự nói" — hiểu lại cho đúng

`editorial-craft.md` nói ~25% số cảnh nên **để footage tự nói, không graphic**.
Điều đó **vẫn đúng** — nhưng dễ bị hiểu sai thành "cảnh không cần biến đổi".

> **"Không graphic" KHÔNG có nghĩa là "ảnh gốc nguyên bản".**

Cảnh footage sạch vẫn phải có ít nhất **hai trong số**: crop lại khung, chuyển
động camera chậm, grade màu, và một card định danh nhỏ (địa điểm/chủ thể).

Bốn thứ đó đã là **ba lớp biến đổi**. Nó đơn giản về mặt *đồ họa*, nhưng không hề
"nguyên bản".

Bảng phân biệt:

| | Nguyên bản (SAI) | Biến đổi (ĐÚNG) |
|---|---|---|
| Khung | giữ 16:9 gốc | crop lại, hoặc chừa lề cho chữ |
| Thời gian | ảnh đứng yên | đẩy/kéo chậm suốt cảnh |
| Màu | giữ nguyên | grade theo tông kênh |
| Chồng lớp | không có gì | card định danh nhỏ |

---

## 5. Ba mức độ biến đổi theo loại tài sản

Không phải mọi hình cần mức như nhau. Mức cần thiết phụ thuộc **nguồn**.

| Nguồn | Rủi ro | Mức cần |
|---|---|---|
| **Người dùng tự cung cấp** (ảnh AI riêng, quay riêng) | thấp | **2 lớp** — crop lại + grade hoặc chữ |
| **Mua bản quyền / stock có phép** | trung bình | **3 lớp** — thêm chuyển động và chồng lớp |
| **Nguồn công cộng** (archive, Wikimedia, báo) | cao | **4 lớp** — thêm cắt ghép, đổi ngữ cảnh |
| **Không rõ nguồn** | rất cao | **không dùng** |

Với job này (110 file do người dùng cung cấp), mức tối thiểu là **2 lớp** — nhưng
vì chúng là ảnh AI có thể trùng prompt với kênh khác, nên **3 lớp** là mức an toàn
hơn.

> **Ảnh AI: cẩn thận riêng.** Ảnh AI tạo từ prompt phổ biến dễ trùng với video
> khác. Nếu là ảnh AI, phải xử lý như **nguồn công cộng** (4 lớp), không phải như
> ảnh tự chụp.

---

## 6. Biến đổi phải phục vụ nội dung, không phải để đối phó

Cạm bẫy: nghe xong luật "phải biến đổi" rồi **thêm hiệu ứng vô nghĩa** cho đủ số
lượng — xoay nhẹ, glitch, hạt bay, đổi màu ngẫu nhiên.

Cách đó **không** giải quyết vấn đề bản quyền (vì hình gốc vẫn nhận ra được), và
làm video dở đi.

> **Luật: mỗi lớp biến đổi phải trả lời được "lớp này giúp người xem hiểu gì?"**

| Lớp biến đổi | Trả lời câu hỏi gì |
|---|---|
| Crop cận | "chi tiết nào đáng nhìn ở đây?" |
| Chuyển động | "cảnh này đang diễn ra hay đã xong?" |
| Grade | "cảnh này thuộc tông nào của phim?" |
| Chữ/số | "con số này là bao nhiêu, thuộc về ai?" |
| Cắt ghép | "hai thứ này liên quan thế nào?" |
| Tái sử dụng | "điều gì đã thay đổi từ lần trước?" |

Nếu một lớp **không trả lời được câu nào** → bỏ lớp đó, tìm lớp khác có nghĩa.

---

## 7. Nghiệm thu: đo mức biến đổi

Với mỗi mục hình trong kế hoạch, phải khai được **lớp biến đổi** đã dùng. Kiểm:

- [ ] **Mọi hình ≥ 2 lớp** — không có ngoại lệ
- [ ] **Không tổ hợp lớp nào lặp quá ~40%** — nếu lặp là đang có công thức
- [ ] **Không hình nào chỉ có "chữ đặt lên ảnh gốc"** — đó là 1 lớp, chưa đủ
- [ ] **Ảnh AI / nguồn công cộng ≥ 4 lớp**
- [ ] Mỗi lớp **trả lời được một câu hỏi ở §6**
- [ ] "Cảnh footage sạch" vẫn có ≥ 2 lớp (thường là 3–4)

`audit_craft.py` đo một phần việc này qua trường `transformLayers` nếu có.

---

## 8. Điểm dễ sai nhất

| Sai | Vì sao sai | Sửa |
|---|---|---|
| "Ảnh tự cung cấp nên khỏi cần xử lý" | nguồn sạch ≠ không trùng | vẫn cần 2–3 lớp |
| "Cảnh để footage tự nói = ảnh gốc" | lẫn "không đồ họa" với "không xử lý" | ít nhất crop + grade |
| Thêm hiệu ứng cho đủ số | không giải quyết bản quyền, làm dở video | mỗi lớp phải có nghĩa |
| Dùng một tổ hợp lớp cho mọi hình | thành công thức, dễ bị nhận ra | luân phiên 5 nhóm |
| Ảnh AI coi như ảnh tự chụp | prompt phổ biến → trùng nhiều kênh | xử lý như nguồn công cộng |
| Chỉ crop mà không grade | 2 lớp nhưng chưa đủ khác về màu | thêm grade hoặc chồng lớp |
| Đổi màu ngẫu nhiên | hình gốc vẫn nhận ra, video xấu | đổi màu theo tông kênh, có chủ đích |

---

## 9. Tóm tắt một câu

> **Với faceless, không có hình nào là "ảnh nền đứng yên". Mỗi hình phải đi qua
> ít nhất hai lớp biến đổi, và mỗi lớp phải phục vụ việc người xem hiểu nội dung —
> vì vừa là yêu cầu bản quyền, vừa là yêu cầu chất lượng.**
