# core/wikidata.py
from SPARQLWrapper import SPARQLWrapper, JSON
from typing import Dict, Optional
from config import settings

class WikidataClient:
    def __init__(self):
        self.endpoint = SPARQLWrapper(settings.WIKIDATA_ENDPOINT)
        self.endpoint.setReturnFormat(JSON)
        self.prefixes = """
        PREFIX wd: <http://www.wikidata.org/entity/>
        PREFIX wdt: <http://www.wikidata.org/prop/direct/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX schema: <http://schema.org/>
        """

    async def get_food_info(self, food_name: str) -> Optional[Dict]:
        query = self.prefixes + """
        SELECT DISTINCT ?item ?itemLabel ?description ?image
        WHERE {
            ?item wdt:P279*/wdt:P31* wd:Q746549 .  # instance of food
            ?item rdfs:label ?itemLabel .
            OPTIONAL { 
                ?item schema:description ?description . 
                FILTER(LANG(?description) = "en")
            }
            OPTIONAL { ?item wdt:P18 ?image . }
            FILTER(LANG(?itemLabel) = "en")
            FILTER(CONTAINS(LCASE(?itemLabel), LCASE("%s")))
        }
        LIMIT 1
        """ % food_name

        try:
            self.endpoint.setQuery(query)
            results = self.endpoint.query().convert()
            
            if results['results']['bindings']:
                return results['results']['bindings'][0]
            return None
        except Exception as e:
            print(f"Wikidata query error: {str(e)}")
            return None