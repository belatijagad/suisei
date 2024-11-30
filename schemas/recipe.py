# schemas/recipe.py
from pydantic import BaseModel, HttpUrl
from typing import Optional, Dict

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
    wikidata: Optional[WikidataInfo] = None

    class Config:
        from_attributes = True