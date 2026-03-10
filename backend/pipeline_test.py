from ingredient_detector import IngredientDetector
from recipe_engine import RecipeEngine


detector = IngredientDetector()
engine = RecipeEngine(r"E:\repo\ingredient-ai-app\dataset\RAW_recipes.csv")


image_path = r"E:\repo\ingredient-ai-app\fruits.jpg"

ingredients = detector.detect(image_path)

print("Detected ingredients:")
print(ingredients)

recipes = engine.recommend(ingredients)

print("\nSuggested recipes:")
for recipe in recipes:
    print(recipe)