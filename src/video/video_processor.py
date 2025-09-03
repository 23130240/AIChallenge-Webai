import cv2
import numpy as np
from src.detectors.yolov8n_detector import YOLOv8nDetector
import os
from transformers import pipeline


class VideoProcessor:
    def __init__(self):
        self.yolov8n_detector = YOLOv8nDetector()
        # QA pipeline (dùng BERT fine-tuned SQuAD)
        self.qa_pipeline = pipeline(
            "question-answering", 
            model="distilbert-base-uncased-distilled-squad"
        )
        
    def extract_keyframes_scene_change(self, video_path, hist_threshold=0.9):
        cap = cv2.VideoCapture(video_path)
        fps = int(cap.get(cv2.CAP_PROP_FPS))

        keyframes = []
        prev_hist = None
        frame_count = 0

        keyframe_dir = os.path.join("data", "keyframes")
        os.makedirs(keyframe_dir, exist_ok=True)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            hist = cv2.calcHist([hsv], [0, 1], None, [50, 60], [0, 180, 0, 256])
            cv2.normalize(hist, hist)

            is_scene_change = False

            if prev_hist is None:
                is_scene_change = True  # always save first frame
            else:
                similarity = cv2.compareHist(prev_hist, hist, cv2.HISTCMP_CORREL)
                if similarity < hist_threshold:
                    is_scene_change = True

            if is_scene_change:
                keyframe_path = os.path.join(keyframe_dir, f"frame_{frame_count}.jpg")
                cv2.imwrite(keyframe_path, frame)

                keyframes.append({
                    'frame_number': frame_count,
                    'timestamp': frame_count / fps,
                    'path': keyframe_path
                })

                prev_hist = hist

            frame_count += 1

        cap.release()
        return keyframes

    
    def process_video_smart(self, video_path, output_dir):
        os.makedirs(output_dir, exist_ok=True)
        
        keyframes = self.extract_keyframes_scene_change(video_path)
        
        processed_frames = []
        for keyframe in keyframes:
            detections = self.yolov8n_detector.object_detection(
                keyframe['path'], conf_threshold=0.5
            )
            
            output_path = os.path.join(
                "data", "detections", f"detected_{os.path.basename(keyframe['path'])}"
            )

            img = cv2.imread(keyframe['path'])
            img = self.yolov8n_detector.draw_boxes(img, detections)
            cv2.imwrite(output_path, img)

            processed_frames.append({
                'original': keyframe,
                'detections': detections,
                'output_path': output_path
            })
        return processed_frames

    # ---------------------------
    # Tìm keyframe theo query
    # ---------------------------

    def search_keyframes_by_keyword(self, processed_frames, query):
        """Hướng A: Dò theo keyword match (nhanh gọn)"""
        query = query.lower()
        results = []
        for f in processed_frames:
            labels = [d['label'].lower() for d in f['detections'] if 'label' in d]
            if any(q in labels for q in query.split()):
                results.append({
                    "timestamp": f['original']['timestamp'],
                    "frame_path": f['original']['path'],
                    "labels": labels
                })
        return results

    def search_keyframes_by_QA(self, processed_frames, query, score_threshold=0.7):
        """Hướng B: Dùng QA model để match query ↔ context"""
        results = []
        for f in processed_frames:
            context_text = "This scene contains: " + ", ".join([d['label'] for d in f['detections'] if 'label' in d])

            answer = self.qa_pipeline(question=query, context=context_text)

            if answer['score'] > score_threshold and answer['answer'].lower() not in ['unknown', '']:
                results.append({
                    "timestamp": f['original']['timestamp'],
                    "frame_path": f['original']['path'],
                    "context": context_text,
                    "answer": answer['answer'],
                    "score": answer['score']
                })
        return results
    
    def search_keyframes_by_trake(self, processed_frames, events, score_threshold=0.5):
    # """
    # Temporal Retrieval and Alignment of Key Events (TRAKE).
    # Tìm dãy keyframe khớp với chuỗi sự kiện theo đúng thứ tự thời gian.
    # - processed_frames: list các frame đã xử lý
    # - events: list[str], mô tả các sự kiện theo thứ tự
    # """
        results = []
        start_idx = 0  # đảm bảo đúng thứ tự thời gian

        for event in events:
            matched = None
            for i in range(start_idx, len(processed_frames)):
                f = processed_frames[i]

                # Tạo context từ object detection
                context_text = "This scene contains: " + ", ".join(
                    [d['label'] for d in f['detections']]
                )

                # Dùng Q&A pipeline để kiểm tra event có xuất hiện không
                answer = self.qa_pipeline(question=event, context=context_text)

                if answer['score'] > score_threshold and answer['answer'].lower() not in ['unknown', '']:
                    matched = f['original']['frame_number']
                    start_idx = i + 1  # bắt đầu tìm event tiếp theo sau frame này
                    break

            if matched is None:
                return None  # không tìm đủ chuỗi event
            results.append(matched)

        return results
