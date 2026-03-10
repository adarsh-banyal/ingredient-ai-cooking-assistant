from ultralytics import YOLO
from recipe_engine import SUPPORTED_INGREDIENTS


class IngredientDetector:

    def __init__(self):
        self.model = YOLO("yolov8n.pt")

    def detect(self, image_path):

        results = self.model(image_path)

        detected = []

        for result in results:
            for box in result.boxes:

                class_id = int(box.cls[0])
                label = self.model.names[class_id].lower()

                if label in SUPPORTED_INGREDIENTS:
                    detected.append(label)

        return list(set(detected))