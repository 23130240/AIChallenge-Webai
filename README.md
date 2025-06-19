# object-detection-project
Tuyệt vời! Dưới đây là phần **chốt cuối cùng**: bao gồm cả **cấu trúc project chuẩn viết theo OOP/OOD** và **bảng phân công công việc đầy đủ** cho **nhóm 2 người** trong tuần đầu thực hiện dự án nhận diện vật thể trong ảnh bằng YOLOv8.

---

## ✅ **I. CẤU TRÚC PROJECT THEO OOP/OOD**

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

## 📋 **II. BẢNG PHÂN CÔNG CÔNG VIỆC (cho nhóm 2 người)**

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

