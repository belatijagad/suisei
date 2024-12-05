from fastapi import APIRouter, HTTPException, Query
from services.recipe_service import RecipeService
from typing import List, Optional
from schemas.recipe import RecipeResponse

router = APIRouter()
recipe_service = RecipeService()

@router.get("/search/", response_model=List[RecipeResponse])
async def search_recipes(
  title: Optional[str] = Query(None, description='Search recipes by title'),
  ingredients: Optional[str] = Query(None, description='Search recipes by ingredients (comma separated)'),
  category: Optional[str] = Query(None, description='Srach recipes by category'),
):
  try:
    ingredient_list = None
    if ingredients:
      ingredient_list = [
        i.strip().replace('_', ' ') 
        for i in ingredients.split()
      ]
    results = await recipe_service.search_recipes(title, category, ingredient_list)
    return results
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))