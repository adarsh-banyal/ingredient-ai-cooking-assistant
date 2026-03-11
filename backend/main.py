from fastapi import FastAPI, UploadFile, File
import shutil
import os

from fastapi.middleware.cors import CORSMiddleware
from backend.ingredient_detector import IngredientDetector
from backend.vector_recipe_engine import VectorRecipeEngine


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

detector = IngredientDetector()
engine = VectorRecipeEngine(r"E:\repo\ingredient-ai-app\dataset\RAW_recipes.csv")


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