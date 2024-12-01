# schemas/recipe.py
from pydantic import BaseModel, HttpUrl
from typing import Optional, Dict, List

class WikidataValue(BaseModel):
    type: str
    value: str
    xml_lang: Optional[str] = None

    class Config:
        from_attributes = True

class WikidataInfo(BaseModel):
    item: Optional[WikidataValue] = None
    itemLabel: Optional[WikidataValue] = None
    description: Optional[WikidataValue] = None
    image: Optional[WikidataValue] = None

    class Config:
        from_attributes = True

class RecipeResponse(BaseModel):
    title: str
    description: Optional[str] = None
    cuisine: Optional[str] = None
    url: Optional[str] = None
    wikidata: Optional[str] = None  # Placeholder for WikidataInfo if needed
    ingredients: Optional[str] = None
    totalIngredients: Optional[int] = None
    steps: Optional[str] = None
    totalSteps: Optional[int] = None
    loves: Optional[int] = None
    category: Optional[str] = None
    tags: Optional[str] = None
    author: Optional[str] = None
    diet: Optional[str] = None
    course: Optional[str] = None
    rating: Optional[float] = None
    recordHealth: Optional[str] = None
    cookTime: Optional[str] = None
    prepTime: Optional[str] = None

    class Config:
        from_attributes = True