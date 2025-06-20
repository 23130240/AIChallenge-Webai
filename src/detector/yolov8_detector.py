from ultralytics import YOLO
from .base import Detector

class YOLOv8Detector(Detector):
    def __init__(self, model_path):
        self.model = YOLO(model_path)

    def predict(self, image):
        return self.model.predict(source=image, save=False)[0]
