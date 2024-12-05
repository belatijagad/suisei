from SPARQLWrapper import SPARQLWrapper, JSON
from typing import Dict, Optional
from config import settings
from functools import lru_cache

class WikidataClient:
    PROPERTIES_MAP = {
        'http://www.wikidata.org/prop/direct/P18': 'image',
        'http://www.wikidata.org/prop/direct/P495': 'country',
    }

    def __init__(self):
        self.endpoint = SPARQLWrapper(settings.WIKIDATA_ENDPOINT)
        self.endpoint.setReturnFormat(JSON)
        # Removed the invalid addCustomUserAgent line
        self.endpoint.addCustomParameter('User-Agent', 'TasteGraph/1.0')  # This is the correct way to add a user agent

    def _build_query(self, wikidata_code: str) -> str:
        return f"""
        SELECT ?property ?propertyLabel ?value ?valueLabel
        WHERE {{
            wd:{wikidata_code} ?property ?value.
            SERVICE wikibase:label {{ 
                bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". 
            }}
        }}
        """

    @lru_cache(maxsize=100)
    def get_info_from_wikidata(self, wikidata_code: str) -> Dict:
        try:
            self.endpoint.setQuery(self._build_query(wikidata_code))
            data = self.endpoint.query().convert()
            return self._parse_response(data)
            
        except Exception as e:
            print(f"Error fetching Wikidata info: {e}")
            return {}

    def _parse_response(self, data: Dict) -> Dict:
        info = {}
        
        if not data.get("results", {}).get("bindings"):
            return info

        for result in data["results"]["bindings"]:
            property_label = result["propertyLabel"]["value"]
            if property_label in self.PROPERTIES_MAP:
                info[self.PROPERTIES_MAP[property_label]] = result.get("valueLabel", {}).get("value")

        return info 