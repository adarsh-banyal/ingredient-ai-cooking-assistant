from ingredient_detector import IngredientDetector

detector = IngredientDetector()

result = detector.detect(r"E:\repo\ingredient-ai-app\bannana.jpg")

print("Detected ingredients:")
print(result)