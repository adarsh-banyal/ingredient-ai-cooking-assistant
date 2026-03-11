from ultralytics import YOLO


class IngredientDetector:

    def __init__(self):
        self.model = YOLO("yolov8n.pt")

    def detect(self, image_path):

        results = self.model(image_path)
        detections_map = {}

        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0])
                label = self.model.names[class_id].lower()
                confidence = float(box.conf[0])

                if label not in detections_map or confidence > detections_map[label]:
                    detections_map[label] = confidence

        # Convert map to list of dicts
        return [{"label": label, "confidence": conf} for label, conf in detections_map.items()]