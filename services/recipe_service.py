from typing import List, Dict, Optional
from core.knowledge_graph import KnowledgeGraph
from core.wikidata import WikidataClient
from dataclasses import dataclass

@dataclass
class SearchParameters:
    title: Optional[str] = None
    category: Optional[str] = None
    ingredients: Optional[List[str]] = None

class RecipeService:
    def __init__(self):
        self.kg = KnowledgeGraph()
        self.wikidata = WikidataClient()

    async def search_recipes(self, 
        title: Optional[str] = None, 
        category: Optional[str] = None, 
        ingredients: Optional[List[str]] = None) -> List[Dict]:
        """
        Search for recipes with optional enrichment from Wikidata.
        """
        try:
            # Get local results
            search_params = SearchParameters(title, category, ingredients)
            local_results = await self.kg.search(
                search_params.title,
                search_params.category,
                search_params.ingredients
            )

            # Enrich with Wikidata information
            enriched_results = await self._enrich_with_wikidata(local_results)
            return enriched_results

        except Exception as e:
            print(f"Error in search_recipes: {e}")
            return []

    async def _enrich_with_wikidata(self, recipes: List[Dict]) -> List[Dict]:
        """
        Enrich recipe data with Wikidata information.
        """
        enriched_recipes = []
        
        for recipe in recipes:
            try:
                wikidata_code = recipe.get('wikicode')
                if wikidata_code:
                    wikidata_info = self.wikidata.get_info_from_wikidata(wikidata_code)
                    if wikidata_info:
                        print(wikidata_info)
                        recipe.update(wikidata_info)
                enriched_recipes.append(recipe)
            except Exception as e:
                print(f"Error enriching recipe {recipe.get('title', 'Unknown')}: {e}")
                enriched_recipes.append(recipe)
        return enriched_recipes