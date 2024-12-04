from typing import List, Dict, Optional
from core.knowledge_graph import KnowledgeGraph
from core.wikidata import WikidataClient

class RecipeService:
  def __init__(self):
    self.kg = KnowledgeGraph()
    self.wikidata = WikidataClient()

  async def search_recipes(self, title: Optional[str], category: Optional[str], ingredients: Optional[List[str]]) -> List[Dict]:
    local_results = await self.kg.search(title, category, ingredients)    
    return local_results