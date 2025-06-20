# object-detection-project
---
## **I. CẤU TRÚC PROJECT**

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

## **II. BẢNG PHÂN CÔNG CÔNG VIỆC**

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
## **III. CHÚ Ý**

---

### ✅ **1. Cấu trúc nhánh Git**

| Nhánh                | Mục đích                              | Ai làm gì                       |
| -------------------- | ------------------------------------- | ------------------------------- |
| `main` hoặc `master` | Chứa code **ổn định**, đã test kỹ     | Chỉ merge khi đã hoàn thiện     |
| `dev`                | Nhánh phát triển **chính**            | Mỗi người tạo nhánh con từ đây  |
| `feature/...`        | Nhánh phát triển **chức năng cụ thể** | Mỗi người code trên nhánh riêng |
| `fix/...`            | Dùng để **sửa lỗi**                   |                                 |
| `refactor/...`       | Dùng để **tái cấu trúc**              |                                 |
| `docs/...`           | Dùng để **cập nhật tài liệu, README** |                                 |

---

### 🏷️ **2. Quy tắc đặt tên nhánh**

| Tên nhánh                 | Dùng cho                         |
| ------------------------- | -------------------------------- |
| `feature/gui-basic`       | Tạo giao diện ban đầu            |
| `feature/detect-yolo`     | Viết module nhận diện YOLO       |
| `fix/yolo-output-error`   | Sửa lỗi liên quan đến YOLO       |
| `refactor/class-detector` | Tối ưu lại code class `Detector` |
| `docs/readme-update`      | Chỉnh sửa tài liệu hướng dẫn     |

---

### 🔁 **3. Quy trình làm việc Git (Chuẩn nhóm)**

#### 🔹 **Lần đầu setup**

```bash
git clone <repo-url>
cd <project>
git checkout -b dev      # Nếu chưa có nhánh dev
git push -u origin dev
```

---

#### 🔹 **Tạo nhánh khi bắt đầu task**

```bash
git checkout dev
git pull origin dev                  # Luôn cập nhật code mới
git checkout -b feature/<task-name> # VD: feature/image-utils
```

---

#### 🔹 **Khi hoàn thành task**

```bash
git add .
git commit -m "Mô tả ngắn gọn"
git push origin feature/<task-name>
```

→ Tạo **Pull Request về `dev`** trên GitHub
→ Người khác **review** → Merge!

---

#### 🔹 **Mỗi sáng bắt đầu làm việc**

```bash
git checkout dev
git pull origin dev
```

→ Luôn cập nhật code mới nhất từ nhóm để tránh xung đột.

---

### 📌 **4. Quy tắc teamwork**

| Quy tắc                           | Lý do                              |
| --------------------------------- | ---------------------------------- |
| Mỗi tính năng → 1 nhánh riêng     | Dễ kiểm soát, tránh đụng code nhau |
| Không commit trực tiếp vào `main` | Tránh làm hỏng code ổn định        |
| Tên nhánh rõ ràng, ngắn gọn       | Dễ hiểu, dễ quản lý                |
| Luôn pull dev trước khi code      | Tránh merge conflict               |

---

### 🔄 **5. Vòng đời 1 Task (tóm gọn)**

```bash
git checkout dev
git pull origin dev
git checkout -b feature/x

## → Viết code

git add .
git commit -m "Xong phần X"
git push origin feature/x

## → Lên GitHub: tạo Pull Request về dev
```

---

### 🗂️ **6. Sơ đồ nhánh (minh họa)**

```
main        ← ổn định, release
│
└─ dev      ← nhánh phát triển chung
   ├─ feature/detect-yolo
   ├─ feature/gui-basic
   └─ fix/image-load-error
```

---
