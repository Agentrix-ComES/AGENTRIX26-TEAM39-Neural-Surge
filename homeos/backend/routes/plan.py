# plan.py
import os
import json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from graph.workflow import compiled_graph

router = APIRouter()

class GenerationRequest(BaseModel):
    budget: float
    family_size: int
    inventory: List[str]

# Global variable fallback memory for trace and plan
_last_plan = None

def get_persisted_plan():
    """
    Helper to read the plan from data/meal_plan.json
    """
    global _last_plan
    plan_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'meal_plan.json')
    if os.path.exists(plan_file):
        try:
            with open(plan_file, 'r', encoding='utf-8') as f:
                _last_plan = json.load(f)
                return _last_plan
        except Exception:
            pass
    return _last_plan

@router.post("/generate")
def generate_plan(req: GenerationRequest):
    """
    Executes the full autonomous LangGraph agent workflow.
    """
    initial_state = {
        "budget": req.budget,
        "family_size": req.family_size,
        "inventory": req.inventory,
        "urgent_foods": [],
        "waste_risk": [],
        "recipes": [],
        "meal_history": [],
        "weekly_plan": {},
        "shopping_list": [],
        "estimated_cost": 0.0,
        "reasoning_summary": "",
        "reflection_result": {},
        "retry_count": 0,
        "agent_trace": []
    }
    
    try:
        # Run LangGraph compilation synchronously
        final_state = compiled_graph.invoke(initial_state)
        
        # Load output report compiled by Reporting Agent
        report_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'meal_plan.json')
        if os.path.exists(report_file):
            with open(report_file, 'r', encoding='utf-8') as f:
                report = json.load(f)
                global _last_plan
                _last_plan = report
                return report
                
        raise HTTPException(status_code=500, detail="Reporting Agent failed to output final meal plan database.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Graph execution failed: {e}")

@router.get("/trace")
def get_trace():
    """
    Retrieves the execution trace logs from the last run.
    """
    plan = get_persisted_plan()
    if plan and "agent_reasoning" in plan:
        return {"trace": plan["agent_reasoning"].get("agent_trace", [])}
    return {"trace": []}

@router.get("/day/{id}")
def get_day_detail(id: int):
    """
    Retrieves details for a specific day of the week (Day 1 through Day 7).
    """
    plan = get_persisted_plan()
    if not plan or "daily_plan" not in plan:
        raise HTTPException(status_code=404, detail="No meal plan exists. Please generate a plan first.")
        
    day_key = f"day_{id}"
    daily_plan = plan["daily_plan"]
    if day_key not in daily_plan:
        raise HTTPException(status_code=404, detail=f"Day {id} does not exist in current weekly plan.")
        
    return {
        "day": id,
        "meals": daily_plan[day_key],
        "household_economics": plan.get("household_economics", {})
    }
