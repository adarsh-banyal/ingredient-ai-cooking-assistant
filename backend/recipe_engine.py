import pandas as pd
import ast
from collections import defaultdict

SUPPORTED_INGREDIENTS = {
    "tomato",
    "potato",
    "onion",
    "carrot",
    "cabbage",
    "broccoli",
    "spinach",
    "cucumber",
    "pepper",
    "eggplant",
    "apple",
    "banana",
    "orange",
    "mango",
    "grapes",
    "lettuce",
    "garlic",
    "ginger",
    "peas",
    "corn"
}


class RecipeEngine:

    def __init__(self, dataset_path):

        df = pd.read_csv(dataset_path)

        df = df[["name", "ingredients"]]

        # convert ingredient string -> python list
        df["ingredients"] = df["ingredients"].apply(ast.literal_eval)

        # normalize ingredients
        df["ingredients"] = df["ingredients"].apply(
            lambda x: [i.lower().strip() for i in x]
        )

        # filter recipes that contain at least one supported ingredient
        filtered_rows = []

        for _, row in df.iterrows():
            ingredients = set(row["ingredients"])

            if ingredients.intersection(SUPPORTED_INGREDIENTS):
                filtered_rows.append(row)

        self.recipes = pd.DataFrame(filtered_rows).reset_index(drop=True)

        # build ingredient index
        self.index = defaultdict(list)

        for idx, row in self.recipes.iterrows():
            for ingredient in row["ingredients"]:
                if ingredient in SUPPORTED_INGREDIENTS:
                    self.index[ingredient].append(idx)

    def recommend(self, user_ingredients):

        user_set = set([i.lower().strip() for i in user_ingredients])

        candidate_recipes = set()

        # gather candidate recipes from index
        for ingredient in user_set:
            if ingredient in self.index:
                candidate_recipes.update(self.index[ingredient])

        results = []

        for idx in candidate_recipes:

            row = self.recipes.iloc[idx]
            recipe_ingredients = set(row["ingredients"])

            matches = user_set.intersection(recipe_ingredients)
            union = user_set.union(recipe_ingredients)

            score = len(matches) / len(union)

            if score > 0.2:
                results.append((row["name"], score))

        results.sort(key=lambda x: x[1], reverse=True)

        return results[:10]