from ultralytics import YOLO


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

                # Accept all detected items
                detected.append(label)

        return list(set(detected))