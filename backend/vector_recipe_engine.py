import pandas as pd
import ast
import os
import numpy as np
import faiss

from sentence_transformers import SentenceTransformer


class VectorRecipeEngine:

    def __init__(self, dataset_path):

        df = pd.read_csv(dataset_path)
        # Include steps in the dataframe
        df = df[["name", "ingredients", "steps"]]

        # Parse string lists into actual Python lists
        df["ingredients"] = df["ingredients"].apply(ast.literal_eval)
        df["steps"] = df["steps"].apply(ast.literal_eval)

        # Create the searchable string for the vector model
        df["searchable_ingredients"] = df["ingredients"].apply(
            lambda x: " ".join([i.lower().strip() for i in x])
        )

        # Sampling dataset to 30,000 for fast RAM loading and embedding generation
        df = df.sample(30000, random_state=42)

        self.recipes = df.reset_index(drop=True)

        self.model = SentenceTransformer("paraphrase-MiniLM-L3-v2")

        # Use absolute paths so the cache is consistently saved/loaded regardless of cwd
        base_dir = os.path.dirname(os.path.abspath(__file__))
        embeddings_dir = os.path.join(base_dir, "embeddings")
        
        vector_cache = os.path.join(embeddings_dir, "recipe_vectors_v2.npy")
        index_cache = os.path.join(embeddings_dir, "faiss_index_v2.bin")

        os.makedirs(embeddings_dir, exist_ok=True)

        # load or generate embeddings
        if os.path.exists(vector_cache):

            print("Loading full cached embeddings...")
            self.recipe_vectors = np.load(vector_cache)

        else:

            print("Generating full embeddings... This might take a moment!")

            self.recipe_vectors = self.model.encode(
                self.recipes["searchable_ingredients"].tolist(),
                batch_size=256,
                show_progress_bar=True,
                convert_to_numpy=True
            )

            np.save(vector_cache, self.recipe_vectors)

        dimension = self.recipe_vectors.shape[1]

        # load or build FAISS index
        if os.path.exists(index_cache):

            print("Loading full FAISS index...")
            self.index = faiss.read_index(index_cache)

        else:

            print("Building full FAISS index...")

            self.index = faiss.IndexFlatL2(dimension)
            self.index.add(self.recipe_vectors)

            faiss.write_index(self.index, index_cache)

    def recommend(self, ingredients, top_k=10):

        query = " ".join(ingredients)

        query_vector = self.model.encode([query])

        distances, indices = self.index.search(query_vector, top_k)

        results = []

        for idx, score in zip(indices[0], distances[0]):
            
            row = self.recipes.iloc[idx]
            
            # Return rich dict with all details
            results.append({
                "name": row["name"],
                "score": float(score),
                "ingredients": row["ingredients"],
                "steps": row["steps"]
            })

        return results