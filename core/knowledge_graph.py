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

  async def search_by_name(self, name: str) -> List[Dict]:
    print(f"Searching for: {name}")
    query = self.prefixes + """
    SELECT DISTINCT ?title ?description ?cuisine ?url (GROUP_CONCAT(?ingredient; SEPARATOR=";") AS ?ingredients) ?totalIngredients
    ?steps ?totalSteps ?loves ?category (GROUP_CONCAT(?tag; SEPARATOR=";") AS ?tags) ?author ?diet ?course ?rating ?recordHealth
    ?cookTime ?prepTime
    WHERE {
      ?makanan rdfs:label ?title ;
        v:hasRecipe ?recipe .
    OPTIONAL {?recipe v:hasDescription ?description ; }
    OPTIONAL {?recipe v:hasCuisine ?cuisine ; }
	  OPTIONAL {?recipe v:hasUrl ?url ; }
    OPTIONAL {?recipe v:hasIngredients ?ingredient ; }
    OPTIONAL {?recipe v:hasTotalIngredients ?totalIngredients ; }
    OPTIONAL {?recipe v:hasSteps ?steps ; }
    OPTIONAL {?recipe v:hasTotalSteps ?totalSteps ; }
    OPTIONAL {?recipe v:hasLoves ?loves ; }
    OPTIONAL {?recipe v:hasCategory ?category ; }
    OPTIONAL {?recipe v:hasTags ?tag ; }
    OPTIONAL {?recipe v:hasAuthor ?author ; }
    OPTIONAL {?recipe v:hasDiet ?diet ; }
    OPTIONAL {?recipe v:hasCourse ?course ; }
    OPTIONAL {?recipe v:hasRating ?rating ; }
    OPTIONAL {?recipe v:hasRecordHealth ?recordHealth ; }
    OPTIONAL {?recipe v:hasCookTime ?cookTime ; }
    OPTIONAL {?recipe v:hasPrepTime ?prepTime ; }

      FILTER(CONTAINS(LCASE(?title), LCASE("%s")))
    }
    GROUP BY ?title ?description ?cuisine ?url ?totalIngredients ?steps ?totalSteps ?loves ?category ?author
    ?diet ?course ?rating ?recordHealth ?cookTime ?prepTime

    """ % name
    print(f'Query: {query}')
    return await self._execute_query(query)

  async def _execute_query(self, query: str) -> List[Dict]:
    try:
      self.endpoint.setQuery(query)
      results = self.endpoint.queryAndConvert()
      print(results)
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
        item[key] = value.get('value')
      formatted.append(item)
        
    return formatted