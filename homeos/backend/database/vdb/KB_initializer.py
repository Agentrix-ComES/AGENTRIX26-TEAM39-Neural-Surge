import os
import pandas as pd
from KB import dummy_recipes
from vector import VectorRepo

def initialize_vector_db():
    print("Initializing Vector Database from Knowledge Base...")
    repo = VectorRepo("recipes")
    
    # Locate recipes.csv relative to project root
    vdb_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.dirname(os.path.dirname(vdb_dir))
    csv_path = os.path.join(backend_dir, "data", "recipes.csv")
    
    if os.path.exists(csv_path) and os.path.getsize(csv_path) > 0:
        print(f"Reading recipes from {csv_path}...")
        df = pd.read_csv(csv_path)
    else:
        print("recipes.csv is not available or is empty. Using dummy recipe data from KB...")
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
        
    print(f"Vector Database initialization complete! Persisted in: {repo.persist_directory}")

if __name__ == "__main__":
    initialize_vector_db()
