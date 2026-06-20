import os
import json
import logging

logger = logging.getLogger(__name__)

def save_meal_plan(report):
    """
    Saves the final meal plan report to homeos/backend/data/meal_plan.json.
    """
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_dir = os.path.join(base_dir, "data")
        os.makedirs(data_dir, exist_ok=True)
        meal_plan_path = os.path.join(data_dir, "meal_plan.json")
        
        with open(meal_plan_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=4)
        print(f"Meal plan successfully saved to {meal_plan_path}")
    except Exception as e:
        logger.error(f"Error saving meal plan: {e}")

def estimate_cost(shopping_list):
    """
    Calculates estimated cost of items in shopping list.
    """
    try:
        return sum(item.get("cost", 0) for item in shopping_list)
    except Exception as e:
        logger.error(f"Error estimating cost: {e}")
        return 0.0
