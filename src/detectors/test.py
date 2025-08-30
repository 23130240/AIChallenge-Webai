import cv2
from yolov8n_detector import YOLOv8nDetector

yolo = YOLOv8nDetector()

img_path = "public/image1.jpg"

objects = yolo.object_detection(img_path, 0.5)

img_detected = yolo.draw_boxes(yolo.load_image(img_path), objects)
img_resized = cv2.resize(img_detected, (400, 300))

for obj in objects:
    print(f"Detected {obj['class_name']} with confidence {obj['confidence']:.2f} at {obj['bbox']}")

cv2.imshow('Detected Objects', img_resized)
cv2.waitKey(0)  
cv2.destroyAllWindows()