from fastapi import FastAPI, UploadFile, File, Query
from pydantic import BaseModel
from typing import List, Optional
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
async def detect_recipes(
    files: List[UploadFile] = File(...),
    filters: Optional[List[str]] = Query(None)
):
    all_detections = {}

    for file in files:
        # save uploaded image temporarily
        with open(UPLOAD_PATH, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # detect ingredients for this image
        detections = detector.detect(UPLOAD_PATH)
        
        # Aggregate detections, keeping highest confidence for each label
        for d in detections:
            label = d["label"]
            conf = d["confidence"]
            if label not in all_detections or conf > all_detections[label]["confidence"]:
                all_detections[label] = d

    # Convert aggregated detections back to list
    final_detections = list(all_detections.values())
    ingredient_labels = [d["label"] for d in final_detections]

    # get recipes
    recipes = engine.recommend(ingredient_labels, filters=filters)

    return {
        "detected_ingredients": final_detections,
        "recipes": recipes
    }

class IngredientRequest(BaseModel):
    ingredients: List[str]
    filters: Optional[List[str]] = None

@app.post("/search-recipes")
async def search_recipes(req: IngredientRequest):
    # get recipes directly from the provided ingredient list
    recipes = engine.recommend(req.ingredients, filters=req.filters)
    return {
        "recipes": recipes
    }