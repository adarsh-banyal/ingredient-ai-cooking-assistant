import pandas as pd
import ast
import os
import numpy as np
import faiss

from sentence_transformers import SentenceTransformer


class VectorRecipeEngine:

    def __init__(self, dataset_path):

        df = pd.read_csv(dataset_path)
        df = df[["name", "ingredients"]]

        df["ingredients"] = df["ingredients"].apply(ast.literal_eval)

        df["ingredients"] = df["ingredients"].apply(
            lambda x: " ".join([i.lower().strip() for i in x])
        )

        # reduce dataset size for faster experimentation
        df = df.sample(30000, random_state=42)

        self.recipes = df.reset_index(drop=True)

        self.model = SentenceTransformer("paraphrase-MiniLM-L3-v2")

        vector_cache = "../embeddings/recipe_vectors.npy"
        index_cache = "../embeddings/faiss_index.bin"

        os.makedirs("../embeddings", exist_ok=True)

        # load or generate embeddings
        if os.path.exists(vector_cache):

            print("Loading cached embeddings...")
            self.recipe_vectors = np.load(vector_cache)

        else:

            print("Generating embeddings...")

            self.recipe_vectors = self.model.encode(
                self.recipes["ingredients"].tolist(),
                batch_size=256,
                show_progress_bar=True,
                convert_to_numpy=True
            )

            np.save(vector_cache, self.recipe_vectors)

        dimension = self.recipe_vectors.shape[1]

        # load or build FAISS index
        if os.path.exists(index_cache):

            print("Loading FAISS index...")
            self.index = faiss.read_index(index_cache)

        else:

            print("Building FAISS index...")

            self.index = faiss.IndexFlatL2(dimension)
            self.index.add(self.recipe_vectors)

            faiss.write_index(self.index, index_cache)

    def recommend(self, ingredients, top_k=10):

        query = " ".join(ingredients)

        query_vector = self.model.encode([query])

        distances, indices = self.index.search(query_vector, top_k)

        results = []

        for idx, score in zip(indices[0], distances[0]):

            recipe_name = self.recipes.iloc[idx]["name"]

            results.append((recipe_name, float(score)))

        return results