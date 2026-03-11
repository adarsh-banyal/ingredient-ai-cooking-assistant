import pandas as pd
import ast
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

        # load embedding model
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        # create embeddings for recipes
        self.recipe_vectors = self.model.encode(
            self.recipes["ingredients"].tolist(),
            show_progress_bar=True
        )

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