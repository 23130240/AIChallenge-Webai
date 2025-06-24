import cv2
import numpy as np
from detectors.yolov8n_detector import YOLOv8nDetector
import os

class VideoProcessor:
    def __init__(self):
        self.yolov8n_detector = YOLOv8nDetector()
        
    def extract_keyframes(self, video_path, interval):
        
        cap = cv2.VideoCapture(video_path)
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        frame_interval = fps*interval
        
        keyframes = []
        frame_count =0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            if frame_count % frame_interval == 0:
                timestamp = frame_count / fps
                keyframe_dir = os.path.join("data", "keyframes")
                os.makedirs(keyframe_dir, exist_ok=True)
                keyframe_path = os.path.join(keyframe_dir, f"frame_{frame_count}.jpg")

                cv2.imwrite(keyframe_path, frame)

                keyframes.append({
                    'frame_number': frame_count,
                    'timestamp': timestamp,
                    'path': keyframe_path
                })
            frame_count += 1
        cap.release()
        return keyframes
    
    def process_video_smart(self, video_path, output_dir):
        os.makedirs(output_dir, exist_ok=True)
        
        keyframes = self.extract_keyframes(video_path, interval = 10)
        
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
    

                
                


