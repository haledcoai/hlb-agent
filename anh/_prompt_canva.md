# Thư viện prompt Canva cho ảnh minh họa HLB

Dùng cho ảnh nguồn `canva` (ảnh không gian chung, ảnh thay ảnh công trình khi chưa có ảnh thật). Chọn cảnh gần nhất với ngữ cảnh đoạn văn, rồi sửa phần trong ngoặc vuông cho khớp số liệu và ý của đoạn đó. Prompt viết tiếng Anh.

Mọi prompt luôn kết thúc bằng câu phủ định chuẩn:

```
no people, no text, no logos, no brand names, no watermarks
```

Ảnh tạo ra luôn là ảnh minh họa: `ghi` bằng `--nguon canva --prompt "<prompt đã dùng>"`, ghi chú tự có "Ảnh minh họa, không phải công trình thật", chú thích trên website có "(ảnh minh họa)". Không dùng prompt cho ảnh sản phẩm có model cụ thể.

## Cảnh mẫu

**1. Xưởng cơ khí, trần cao**
```
Wide-angle photo of a clean metalworking factory interior, steel roof truss at about [9] m height, rows of round LED high bay lights (UFO type) hanging evenly, bright uniform light on grey epoxy floor, CNC machines in rows, realistic, natural colors, no people, no text, no logos, no brand names, no watermarks
```

**2. Kho kệ cao, lối đi hẹp**
```
Photo of a warehouse with tall pallet racks about [10] m high, narrow aisles, LED high bay lights hanging above each aisle, light reaching the lower shelves, concrete floor, realistic, no people, no text, no logos, no brand names, no watermarks
```

**3. Xưởng may, xưởng lắp ráp (cần độ rọi cao trên bàn làm việc)**
```
Photo of a garment or assembly workshop, long rows of work tables, ceiling about [6] m, evenly spaced LED high bay lights, bright even light on the work surfaces, no shadows on tables, realistic, no people, no text, no logos, no brand names, no watermarks
```

**4. Xưởng thực phẩm, khu ẩm, có rửa sàn**
```
Photo of a food processing plant interior, stainless steel equipment, wet glossy floor after washing, sealed LED high bay lights mounted on the ceiling, clean hygienic environment, realistic, no people, no text, no logos, no brand names, no watermarks
```

**5. Khu bốc xếp, mái hiên**
```
Photo of a factory loading dock under a steel canopy at dusk, LED lights under the canopy lighting the loading area evenly, trucks parked at the dock doors, realistic, no people, no text, no logos, no brand names, no watermarks
```

**6. Nhà xưởng nhỏ 200-500 m², khung thép mái tôn**
```
Photo of a small single-storey steel frame workshop about [200] m2, corrugated metal roof about [7] m high, a few LED high bay lights in a simple grid, bright clean interior, realistic, no people, no text, no logos, no brand names, no watermarks
```

## Khi ảnh bị trả về (trạng thái `lam_lai`)

Đọc `prompt` cũ trong `anh.json` và ghi chú của người dùng, chỉ sửa phần bị chê (ví dụ "đèn trông như đèn tuýp" thì thêm "round UFO shaped high bay lights, not linear tubes"), giữ phần còn lại. Lỗi hay gặp ở ảnh AI và câu thêm vào prompt:

| Lỗi | Thêm vào prompt |
|---|---|
| Đèn lơ lửng, không có dây treo | each light hanging from the roof truss on a short chain |
| Mái, kèo méo | straight steel roof trusses, symmetrical structure |
| Kiểu đèn khác mô tả | round UFO shaped LED high bay lights |
| Có chữ hoặc biển hiệu | blank walls, no signs |
| Sáng chói, cháy sáng | soft even lighting, no glare, correct exposure |
