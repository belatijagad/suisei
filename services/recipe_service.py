from typing import List, Dict, Optional
from core.knowledge_graph import KnowledgeGraph
from core.wikidata import WikidataClient

class RecipeService:
  def __init__(self):
    self.kg = KnowledgeGraph()
    self.wikidata = WikidataClient()

  async def search_recipes(self, title: Optional[str], category: Optional[str], ingredients: Optional[List[str]]) -> List[Dict]:
    local_results = await self.kg.search(title, category, ingredients)   
    for i in range(len(local_results)):
      result = local_results[i]
      wikidata_code = result.get('wikicode')
      if wikidata_code:
        wikidata_info = self.wikidata.get_info_from_wikidata(wikidata_code)
        result.update(wikidata_info) 
        local_results[i] = result
        
    return local_results