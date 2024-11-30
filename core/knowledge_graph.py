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
    query = self.prefixes + """
    SELECT DISTINCT ?title ?description ?cuisine ?url
    WHERE {
      ?makanan rdfs:label ?title ;
        v:recipe ?recipe .
      ?recipe v:description ?description ;
        v:cuisine ?cuisine ;
        v:url ?url ;
      FILTER(CONTAINS(LCASE(?title), LCASE("%s")))
    }
    LIMIT 10
    """ % name
    
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
        item[key] = value.get('value')
      formatted.append(item)
        
    return formatted