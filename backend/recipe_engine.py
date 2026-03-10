import pandas as pd

class RecipeEngine:

    def __init__(self, dataset_path):
        self.recipes = pd.read_csv(dataset_path)

        # convert ingredients to list
        self.recipes["ingredients"] = self.recipes["ingredients"].apply(
            lambda x: [i.strip() for i in x.split(",")]
        )

    def recommend(self, user_ingredients):
        user_set = set(user_ingredients)
        matches = []

        for _, row in self.recipes.iterrows():

            recipe_ingredients = set(row["ingredients"])

            if recipe_ingredients.issubset(user_set):
                matches.append(row["recipe"])

        return matches