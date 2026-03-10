from fastapi import FastAPI, UploadFile, File
import shutil
import os

from backend.ingredient_detector import IngredientDetector
from backend.recipe_engine import RecipeEngine


app = FastAPI()

detector = IngredientDetector()
engine = RecipeEngine(r"E:\repo\ingredient-ai-app\dataset\RAW_recipes.csv")


UPLOAD_PATH = r"E:\repo\ingredient-ai-app\fruits.jpg"


@app.post("/detect-recipes")
async def detect_recipes(file: UploadFile = File(...)):

    # save uploaded image temporarily
    with open(UPLOAD_PATH, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # detect ingredients
    ingredients = detector.detect(UPLOAD_PATH)

    # get recipes
    recipes = engine.recommend(ingredients)

    return {
        "detected_ingredients": ingredients,
        "recipes": recipes
    }