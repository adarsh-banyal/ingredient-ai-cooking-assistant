import pandas as pd
import ast
import os
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class VectorRecipeEngine:

    def __init__(self, dataset_path):

        df = pd.read_csv(dataset_path)
        df = df[["name", "ingredients"]]

        df["ingredients"] = df["ingredients"].apply(ast.literal_eval)

        df["ingredients"] = df["ingredients"].apply(
            lambda x: " ".join([i.lower().strip() for i in x])
        )

        self.recipes = df

        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        cache_file = "../embeddings/recipe_vectors.npy"

        if os.path.exists(cache_file):

            print("Loading cached embeddings...")
            self.recipe_vectors = np.load(cache_file)

        else:

            print("Generating recipe embeddings...")

            self.recipe_vectors = self.model.encode(
                self.recipes["ingredients"].tolist(),
                batch_size=256,
                show_progress_bar=True,
                convert_to_numpy=True
            )

            os.makedirs("../embeddings", exist_ok=True)
            np.save(cache_file, self.recipe_vectors)

    def recommend(self, ingredients):

        query = " ".join(ingredients)

        query_vector = self.model.encode([query])

        similarities = cosine_similarity(query_vector, self.recipe_vectors)[0]

        top_indices = similarities.argsort()[-10:][::-1]

        results = []

        for idx in top_indices:
            results.append(
                (self.recipes.iloc[idx]["name"], float(similarities[idx]))
            )

        return results