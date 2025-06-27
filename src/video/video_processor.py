import cv2
import numpy as np
from detectors.yolov8n_detector import YOLOv8nDetector
import os

class VideoProcessor:
    def __init__(self):
        self.yolov8n_detector = YOLOv8nDetector()
        
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
            detections = self.yolov8n_detector.object_detection(keyframe['path'], conf_threshold=0.5)
            
            output_path = os.path.join("data", "detections", f"detected_{os.path.basename(keyframe['path'])}")

            img = cv2.imread(keyframe['path'])
            img = self.yolov8n_detector.draw_boxes(img, detections)
            cv2.imwrite(output_path, img)

            processed_frames.append({
                'original' : keyframe,
                'detections' : detections,
                'output_path' : output_path
            })
        return processed_frames
    

                
                


