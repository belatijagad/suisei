from SPARQLWrapper import SPARQLWrapper, JSON
from typing import List, Dict, Optional
from config import settings

class KnowledgeGraph:
  def __init__(self):
    self.endpoint = SPARQLWrapper(settings.DB_ENDPOINT)
    self.endpoint.setReturnFormat(JSON)
    self.headers = {
      'Accept': 'application/sparql-results+json',
      'Content-Type': 'application/x-www-form-urlencoded'
    }
    self.prefixes = """
    PREFIX v: <http://example.com/vocab#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    """

  async def search(self, title: Optional[str], category: Optional[str], ingredients: Optional[List[str]], limit: int=10) -> List[Dict]:
    conditions = []
    if title: conditions.append(f'CONTAINS(LCASE(?title), LCASE("{title}"))')
    if category: conditions.append(f'CONTAINS(LCASE(?category), LCASE("{category}"))')
    if ingredients:
      ingredient_conditions = ' && '.join([
          f'EXISTS {{ ?recipe v:hasIngredients ?ingredient{i} . FILTER(CONTAINS(LCASE(?ingredient{i}), LCASE("{ingredient}"))) }}'
          for i, ingredient in enumerate(ingredients)
      ])
      conditions.append(f'({ingredient_conditions})')
    final_conditions = ' && '.join(conditions) if conditions else 'true'
    
    query = self.prefixes + """
    SELECT DISTINCT ?title ?description ?cuisine ?url ?totalIngredients
    ?steps ?totalSteps ?loves ?category ?author ?diet ?course ?rating ?recordHealth
    ?cookTime ?prepTime ?ingredients ?tags
    WHERE {
      ?makanan rdfs:label ?title ;
        v:hasRecipe ?recipe .
      ?recipe v:hasUrl ?url ;
        v:hasAuthor ?author ;
        v:hasCuisine ?cuisine ;
        v:hasCategory ?category ;
        v:hasSteps ?steps ;
        v:hasTotalSteps ?totalSteps ;
        v:hasIngredients ?searchIngredient ;
        v:hasTotalIngredients ?totalIngredients .
        
      FILTER(%s)
      
      {
        SELECT ?recipe (GROUP_CONCAT(?ingredient; SEPARATOR=";") AS ?ingredients) 
        WHERE { ?recipe v:hasIngredients ?ingredient } GROUP BY ?recipe
      }
    
      {
        SELECT ?recipe (GROUP_CONCAT(?tag; SEPARATOR=";") AS ?tags) 
        WHERE { ?recipe v:hasTags ?tag } GROUP BY ?recipe
      }
      
      OPTIONAL {?recipe v:hasDescription ?description ; }
      OPTIONAL {?recipe v:hasLoves ?loves ; }
      OPTIONAL {?recipe v:hasTags ?tag ; }
      OPTIONAL {?recipe v:hasDiet ?diet ; }
      OPTIONAL {?recipe v:hasCourse ?course ; }
      OPTIONAL {?recipe v:hasRating ?rating ; }
      OPTIONAL {?recipe v:hasRecordHealth ?recordHealth ; }
      OPTIONAL {?recipe v:hasCookTime ?cookTime ; }
      OPTIONAL {?recipe v:hasPrepTime ?prepTime ; }
    }
    LIMIT %s
    """ % (final_conditions, limit)
    
    return await self._execute_query(query)
    
  async def _execute_query(self, query: str) -> List[Dict]:
    try:
      self.endpoint.setQuery(query)
      results = self.endpoint.queryAndConvert()
      return self._format_results(results)
    except Exception as e:
      print(f"Query execution error: {str(e)}")
      return []

  def _format_results(self, results: Dict) -> List[Dict]:
      formatted = []
      bindings = results.get('results', {}).get('bindings', [])
      
      for binding in bindings:
          item = {}
          for key, value in binding.items():
              val = value.get('value')
              if key == 'ingredients' and val:
                  item[key] = val.split(';')
              elif key == 'steps' and val:
                  item[key] = val.split('|')
              else:
                  item[key] = val
          formatted.append(item)
              
      return formatted