import pandas as pd
import ast


class RecipeEngine:

    def __init__(self, dataset_path):

        df = pd.read_csv(dataset_path)

        df = df[["name", "ingredients"]]

        # convert string list → python list
        df["ingredients"] = df["ingredients"].apply(ast.literal_eval)

        self.recipes = df

    def recommend(self, user_ingredients):

        user_set = set(user_ingredients)
        results = []

        for _, row in self.recipes.iterrows():

            recipe_ingredients = set(row["ingredients"])

            matches = user_set.intersection(recipe_ingredients)

            score = len(matches) / len(recipe_ingredients)

            if score > 0.3:   # threshold
                results.append((row["name"], score))

        results.sort(key=lambda x: x[1], reverse=True)

        return results[:10]