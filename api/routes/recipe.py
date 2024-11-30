from fastapi import APIRouter, HTTPException
from services.recipe_service import RecipeService
from typing import List
from schemas.recipe import RecipeResponse

router = APIRouter()
recipe_service = RecipeService()

@router.get("/search/{name}", response_model=List[RecipeResponse])
async def search_recipes(name: str):
  try:
    results = await recipe_service.search_recipes(name)
    return results
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))