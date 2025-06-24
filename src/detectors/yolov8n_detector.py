import cv2
from ultralytics import YOLO


class YOLOv8nDetector():
    def __init__(self, path='weights/yolov8n.weights'):
        self.model = YOLO(path)

    def load_image(self, img_path):
        img = cv2.imread(img_path)
        return img

    def object_detection(self, image_path, conf_threshold):
        results = self.model(image_path, conf_threshold)

        detections = []
        for result in results:
            boxes = result.boxes
            

