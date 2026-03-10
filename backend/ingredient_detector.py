from ultralytics import YOLO
import cv2


class IngredientDetector:

    def __init__(self):
        # load pretrained YOLO model
        self.model = YOLO("yolov8n.pt")

    def detect(self, image_path):

        results = self.model(image_path)

        detected_objects = []

        for result in results:
            for box in result.boxes:

                class_id = int(box.cls[0])
                label = self.model.names[class_id]

                detected_objects.append(label)

        return list(set(detected_objects))