from recipe_engine import RecipeEngine

engine = RecipeEngine(r"E:\repo\ingredient-ai-app\dataset\RAW_recipes.csv")

ingredients = ["tomato","onion","potato"]

print(engine.recommend(ingredients))