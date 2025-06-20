# object-detection-project
---
## ✅ **I. CẤU TRÚC PROJECT**

```
object_detection_project/
├── images/                         # Ảnh đầu vào để test
├── results/                        # Ảnh đầu ra sau khi vẽ bounding box
├── weights/                        # File model YOLOv8 (.pt)
│   └── yolov8n.pt
├── src/                            # Mã nguồn chính
│   ├── __init__.py
│   ├── main.py                     # Điểm bắt đầu chương trình
│   ├── config.py                   # Chứa cấu hình (đường dẫn model, threshold...)
│
│   ├── detector/
│   │   ├── __init__.py
│   │   ├── base.py                 # Lớp trừu tượng Detector (interface)
│   │   └── yolov8_detector.py     # Cài đặt Detector bằng YOLOv8
│
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── image_loader.py        # Hàm load và resize ảnh
│   │   └── visualizer.py          # Hàm vẽ bounding box và label lên ảnh
│
│   └── cli.py                      # Nhận ảnh từ dòng lệnh (tùy chọn nâng cao)
├── requirements.txt               # Các thư viện cần cài đặt
├── README.md                      # Hướng dẫn sử dụng
```

---

## 📋 **II. BẢNG PHÂN CÔNG CÔNG VIỆC**

| STT | Công việc cụ thể                                      | Người thực hiện   | Deadline | Ghi chú                              |
| --- | ----------------------------------------------------- | ----------------- | -------- | ------------------------------------ |
| 1   | Cài đặt thư viện: `ultralytics`, `opencv-python`      | **Bạn B**         | 20/6     | Test import OK                       |
| 2   | Tải và đặt model YOLOv8 (`yolov8n.pt`) vào `weights/` | **Bạn B**         | 20/6     | Dùng YOLOv8n (nhẹ)                   |
| 3   | Thu thập ảnh đầu vào và lưu vào `images/`             | **Bạn A**         | 21/6     | \~10–20 ảnh (người, xe, vật dụng...) |
| 4   | Viết `image_loader.py`: load + resize ảnh             | **Bạn A**         | 22/6     | Dùng OpenCV                          |
| 5   | Viết `base.py`: abstract class Detector               | **Bạn B**         | 22/6     | Dùng `abc.ABC`                       |
| 6   | Viết `yolov8_detector.py`: cài YOLOv8Detector         | **Bạn B**         | 22/6     | Kế thừa từ `Detector`                |
| 7   | Viết `visualizer.py`: vẽ bounding box, label          | **Bạn A**         | 23/6     | Dùng `cv2.rectangle`, `cv2.putText`  |
| 8   | Viết `main.py`: kết hợp pipeline detect               | **Cả 2 cùng làm** | 23/6     | Load ảnh → detect → vẽ → lưu kết quả |
| 9   | Chạy thử nhiều ảnh, lưu kết quả vào `results/`        | **Bạn B**         | 24/6     | Lưu kết quả với hậu tố `_out.jpg`    |
| 10  | Viết `README.md` mô tả cách chạy, kết quả mẫu         | **Bạn A**         | 25/6     | Markdown hoặc Word                   |
| 11  | Ghi lại lỗi / limit của model YOLO (ảnh sai/sót)      | **Bạn B**         | 25/6     | Ghi rõ class sai, ảnh mờ...          |
| 12  | Tạo slide demo trình bày (nếu cần)                    | **Cả 2**          | 26/6     | Gộp input + output ảnh demo          |

---

## 🎁 Tệp tin đi kèm bạn nên chuẩn bị

| Tên tệp                      | Mô tả                                          |
| ---------------------------- | ---------------------------------------------- |
| `requirements.txt`           | `ultralytics\nopencv-python`                   |
| `README.md`                  | Mục tiêu, cách cài đặt, cách chạy, ảnh kết quả |
| `detect.py` (hoặc `main.py`) | Tích hợp pipeline detect ảnh                   |

---
## ✅ **III. CHÚ Ý**

### 📌 Có 3 loại nhánh chính:

| Nhánh                | Mục đích                                   | Ai làm gì                         |
| -------------------- | ------------------------------------------ | --------------------------------- |
| `main` hoặc `master` | Nhánh chính, chứa code ổn định, đã test kỹ | Chỉ merge khi đã hoàn thiện       |
| `dev`                | Nhánh phát triển chung                     | Mỗi người tạo nhánh con từ đây    |
| `feature/...`        | Nhánh con để phát triển từng chức năng     | Mỗi người code 1 nhánh riêng biệt |

---

## 📌 **2. Cách đặt tên nhánh (chuẩn và dễ hiểu)**

| Tên nhánh                 | Dùng cho                       |
| ------------------------- | ------------------------------ |
| `feature/detect-yolo`     | Phát triển phần nhận diện YOLO |
| `feature/gui-basic`       | Giao diện ban đầu              |
| `feature/image-utils`     | Viết hàm đọc ảnh, vẽ ảnh       |
| `fix/yolo-output-error`   | Sửa lỗi liên quan output YOLO  |
| `refactor/class-detector` | Tái cấu trúc class `Detector`  |
| `docs/readme-update`      | Chỉnh sửa README, hướng dẫn    |

---

## 🧑‍💻 **3. Quy trình làm việc nhóm (chuẩn Git flow nhẹ)**

```bash
# Bước 1: clone project về
git clone https://github.com/your-team/project.git
cd project

# Bước 2: tạo nhánh phát triển (nếu chưa có)
git checkout -b dev
git push -u origin dev

# Bước 3: mỗi người tạo nhánh riêng từ dev
git checkout dev
git checkout -b feature/image-utils
```

Sau đó mỗi người **code trên nhánh của mình** → **push lên GitHub** → **tạo pull request về `dev`** để review & test.

---

## 🔁 **4. Ví dụ quy trình merge**

1. Thành viên A hoàn thành `feature/image-utils`
2. Push lên GitHub
3. Tạo Pull Request từ `feature/image-utils` → `dev`
4. Review OK → merge
5. Khi `dev` ổn định → merge vào `main`

---

## 🧠 **5. Tips cho teamwork dễ hiểu, dễ merge**

| Quy tắc                                | Giải thích                         |
| -------------------------------------- | ---------------------------------- |
| Mỗi chức năng → 1 nhánh riêng          | Tránh code chồng chéo              |
| Không commit trực tiếp vào `main`      | Giữ code ổn định                   |
| Thường xuyên `pull` nhánh `dev` mới về | Để tránh xung đột                  |
| Tên nhánh nên ngắn gọn, rõ ràng        | VD: `feature/train`, `fix/gui-bug` |

---

## ✅ Cấu trúc nhánh bạn nên dùng

```
main        ← ổn định, release
│
└─ dev      ← nhánh phát triển chung
   ├─ feature/detect-yolo
   ├─ feature/gui-basic
   └─ fix/image-load-error
```


