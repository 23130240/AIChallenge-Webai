import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from detectors.yolov8n_detector import YOLOv8nDetector
from video.video_processor import VideoProcessor

video_path = r'c:\Users\admin\Pictures\vidoe.mp4'  


output_dir = 'data/detections'

processor = VideoProcessor()

# Kiểm tra video có tồn tại không
if not os.path.exists(video_path):
    print(f"Video không tồn tại tại đường dẫn: {video_path}")
else:
    print("Đang xử lý video...")

    # Gọi xử lý thông minh
    results = processor.process_video_smart(video_path, output_dir)

    # Hiển thị kết quả
    print(f"Xử lý hoàn tất. Số keyframe được xử lý: {len(results)}")
    for idx, frame in enumerate(results):
        print(f"[{idx}] Frame: {frame['original']['frame_number']}, Detections: {len(frame['detections'])}")
        print(f"    Đã lưu ảnh: {frame['output_path']}")
