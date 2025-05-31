# 🧩 Sudoku Game – Pygame

Một trò chơi Sudoku đơn giản viết bằng **Python 3** và **Pygame**, sử dụng thuật toán **Backtracking** để giải quyết vấn đề, kèm theo đó là các tính năng chọn độ khó, gợi ý, hiện kết quả và tạo game mới.

---

## 🚀 Tính năng

- ✅ Chơi Sudoku với 3 mức độ: *Easy, Medium, Hard*
- 🧠 Gợi ý (Hint): Tự động điền 1 ô đúng
- ✅ Hiện đáp án đầy đủ
- ♻️ Chơi lại nhanh chóng
- 🎚 Chọn độ khó từ menu

---

## 📦 Cài đặt

1. **Tải project**:
   ```bash
   git clone https://github.com/ten-ban/sudoku-game.git
   cd sudoku-game
2. **Cài đặt thư viện**:
   ```bash
   pip install -r requirements.txt
3. **Chạy project**:
   ```bash
   python main.py
   
## 🎮 Hướng dẫn cách chơi:

   - Click chuột vào ô muốn điền
   
   - Nhập số từ 1–9
   
   - Sai số thì bị trừ "mạng"
   
   - Nút Hint: Gợi ý 1 số đúng
   
   - Nút Result: Hiện toàn bộ kết quả
   
   - Nút New Game: Tạo ván mới
   
   - Nút Difficulty: Chọn lại mức độ dễ / trung bình / khó


## Version

Recommended: **3.12.10**

## Game init

![image](https://github.com/user-attachments/assets/ec6a94ea-f105-454d-b26a-8d5c1bda8104)

## Game complete

![image](https://github.com/user-attachments/assets/4801b566-a2cf-4f15-a84a-db51a8dc5f86)

## Game over

![image](https://github.com/user-attachments/assets/bf00490d-1081-45a6-b429-674c97279961)

## Level easy
**Ô trống là 27**

![image](https://github.com/user-attachments/assets/5dd1addd-8ab6-4215-a435-f655c7956d7f)

## Level medium
**Ô trống là 40**

![image](https://github.com/user-attachments/assets/afdbff58-65a1-4095-bde7-764ca39c4f31)


## Level Hard
**Ô trống là 60**

![image](https://github.com/user-attachments/assets/47008c96-49d5-45ad-9f94-fd1bc0b01859)

## Cải tiến
Sử dụng **Heuristic**:
Thay vì chọn ô trống 1 cách ngẫu nhiên thì **Heuristic** chọn ô trống có ít khả năng điền hợp lệ nhất
-> Làm giảm số lần backtracking
-> Tối ưu hóa lời giải 
-> Nhanh hơn

--> Thuật toán lựa chọn là Minimum Remaining Values

**Minimum Remaining Values**:
- Duyệt qua từng ô trống trong bảng.
- Với mỗi ô, đếm xem có bao nhiêu giá trị hợp lệ (từ 1 đến N) -> options.
- Nếu options < (min_options_present), thì cập nhật min_options_present và lưu ô đó làm best_cell.
- Cuối cùng, trả về ô best_cell có ít lựa chọn nhất — tức là khó nhất — để giải quyết trước.
