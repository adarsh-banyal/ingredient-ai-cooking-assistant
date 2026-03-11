from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
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
    detections = detector.detect(UPLOAD_PATH)
    
    # Extract just the labels for the recipe engine
    ingredient_labels = [d["label"] for d in detections]

    # get recipes
    recipes = engine.recommend(ingredient_labels)

    return {
        "detected_ingredients": detections,
        "recipes": recipes
    }

class IngredientRequest(BaseModel):
    ingredients: list[str]

@app.post("/search-recipes")
async def search_recipes(req: IngredientRequest):
    # get recipes directly from the provided ingredient list
    recipes = engine.recommend(req.ingredients)
    return {
        "recipes": recipes
    }