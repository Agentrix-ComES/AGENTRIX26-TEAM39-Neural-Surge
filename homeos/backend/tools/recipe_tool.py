import logging
from vector_db.qdrant import search_recipes_vector

logger = logging.getLogger(__name__)

def search_recipes(query: str):
    """
    Search recipes from Qdrant vector DB using the query terms.
    Returns:
        dict: A dictionary containing a list of matching recipes under the "recipes" key.
    """
    try:
        results = search_recipes_vector(query)
        return {"recipes": results}
    except Exception as e:
        logger.error(f"Error in search_recipes: {e}")
        return {"recipes": []}
