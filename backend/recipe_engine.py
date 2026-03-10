import pandas as pd
import ast
from collections import defaultdict


class RecipeEngine:

    def __init__(self, dataset_path):

        df = pd.read_csv(dataset_path)

        df = df[["name", "ingredients"]]

        df["ingredients"] = df["ingredients"].apply(ast.literal_eval)

        df["ingredients"] = df["ingredients"].apply(
            lambda x: [i.lower().strip() for i in x]
        )

        self.recipes = df

        # Build ingredient index
        self.index = defaultdict(list)

        for idx, row in df.iterrows():
            for ingredient in row["ingredients"]:
                self.index[ingredient].append(idx)

    def recommend(self, user_ingredients):

        candidate_recipes = set()

        # gather recipes containing user ingredients
        for ingredient in user_ingredients:
            if ingredient in self.index:
                candidate_recipes.update(self.index[ingredient])

        results = []

        for idx in candidate_recipes:

            row = self.recipes.iloc[idx]

            recipe_ingredients = set(row["ingredients"])
            user_set = set(user_ingredients)

            matches = user_set.intersection(recipe_ingredients)

            union = user_set.union(recipe_ingredients)

            score = len(matches) / len(union)

            if score > 0.2:
                results.append((row["name"], score))

        results.sort(key=lambda x: x[1], reverse=True)

        return results[:10]