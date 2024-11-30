# services/recipe_service.py
from typing import List, Dict
from core.knowledge_graph import KnowledgeGraph
from core.wikidata import WikidataClient

class RecipeService:
  def __init__(self):
    self.kg = KnowledgeGraph()
    self.wikidata = WikidataClient()

  async def search_recipes(self, name: str) -> List[Dict]:
    local_results = await self.kg.search_by_name(name)
    
    enriched_results = []
    for result in local_results:
      recipe = result.copy()
      wikidata_info = await self.wikidata.get_food_info(result.get('title', ''))
      if wikidata_info:
        recipe['wikidata'] = wikidata_info
      enriched_results.append(recipe)
    
    return enriched_results