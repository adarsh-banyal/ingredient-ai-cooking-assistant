from recipe_engine import RecipeEngine

engine = RecipeEngine(r"E:\repo\ingredient-ai-app\dataset\recipes.csv")

ingredients = ["potato", "tomato", "onion"]

recipes = engine.recommend(ingredients)

print(recipes)