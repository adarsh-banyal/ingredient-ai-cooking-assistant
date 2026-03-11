from vector_recipe_engine import VectorRecipeEngine

engine = VectorRecipeEngine(r"E:\repo\ingredient-ai-app\dataset\RAW_recipes.csv")

ingredients = ["tomato", "onion", "potato"]

recipes = engine.recommend(ingredients)

print(recipes)