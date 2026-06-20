import os
import pandas as pd
from vector import VectorRepo

dummy_recipes = [
    {
        "name": "Chicken Alfredo Pasta",
        "ingredients": "pasta, chicken breast, heavy cream, parmesan cheese, garlic, butter",
        "cuisine": "Italian",
        "instructions": "1. Cook pasta. 2. Sear chicken in butter with garlic. 3. Add heavy cream and parmesan to make the sauce. 4. Mix pasta and sauce, top with sliced chicken."
    },
    {
        "name": "Tomato Basil Soup",
        "ingredients": "tomatoes, fresh basil, garlic, onion, vegetable broth, olive oil, cream",
        "cuisine": "American",
        "instructions": "1. Sauté onion and garlic in olive oil. 2. Add tomatoes and broth, simmer for 20 minutes. 3. Blend until smooth. 4. Stir in fresh basil and cream."
    },
    {
        "name": "Spicy Tofu Stir Fry",
        "ingredients": "firm tofu, broccoli, bell peppers, soy sauce, sriracha, sesame oil, ginger",
        "cuisine": "Asian",
        "instructions": "1. Press and cube tofu, then pan-fry until golden. 2. Stir-fry broccoli and peppers. 3. Mix soy sauce, sriracha, and ginger. 4. Toss tofu and veggies with the sauce."
    },
    {
        "name": "Chocolate Chip Cookies",
        "ingredients": "flour, butter, brown sugar, white sugar, eggs, vanilla extract, baking soda, chocolate chips",
        "cuisine": "Dessert",
        "instructions": "1. Cream butter and sugars. 2. Beat in eggs and vanilla. 3. Mix in dry ingredients. 4. Fold in chocolate chips and bake at 350°F (175°C) for 10 minutes."
    }
]

def main():
    # Initialize the VectorRepo with collection name 'recipes'
    repo = VectorRepo("recipes")
    
    # Try to locate the recipes.csv file relative to the project root
    # Project root is homeos/backend/data/recipes.csv relative to AGENTRIX26-TEAM39-Neural-Surge
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # homeos/backend
    csv_path = os.path.join(base_dir, "data", "recipes.csv")
    
    if os.path.exists(csv_path) and os.path.getsize(csv_path) > 0:
        print(f"Reading recipes from {csv_path}...")
        df = pd.read_csv(csv_path)
    else:
        print("recipes.csv is not available or is empty. Using dummy recipe data...")
        df = pd.DataFrame(dummy_recipes)
    
    for i, row in df.iterrows():
        text = f"""
        Recipe: {row['name']}
        Ingredients: {row['ingredients']}
        Cuisine: {row['cuisine']}
        Instructions: {row['instructions']}
        """
        doc_id = f"recipe_{i}"
        repo.add_reference(doc_id, text.strip())
        print(f"Added recipe to VDB: {row['name']}")

if __name__ == "__main__":
    main()