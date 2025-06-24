import cv2
from ultralytics import YOLO


class YOLOv8nDetector():
    def __init__(self, path='weights/yolov8n.pt'):
        self.model = YOLO(path)

    def load_image(self, img_path):
        img = cv2.imread(img_path)
        return img

    def object_detection(self, image_path, conf_threshold):
        results = self.model(image_path, conf_threshold)

        objects = []
        for result in results:
            boxes = result.boxes
            for box in boxes:
                if box is not None:
                    x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().numpy())
                    conf = box.conf[0].cpu().numpy()
                    class_id = int(box.cls[0].cpu().numpy())
                    class_name = self.model.names[class_id]

                    objects.append({
                        'bbox': [x1, y1, x2, y2],
                        'confidence': conf,
                        'class_id': class_id,
                        'class_name': class_name
                    })
        return objects
    
    def draw_boxes(self, image, objects):
        for obj in objects:
            x1, y1, x2, y2 = obj['bbox']
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            label = f"{obj['class_name']} {obj['confidence']:.2f}"
            cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        return image



