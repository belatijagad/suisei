# core/wikidata.py
from SPARQLWrapper import SPARQLWrapper, JSON
from typing import Dict, Optional
from config import settings
import requests

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

    def get_info_from_wikidata(self, wikidata_code):

        # example: get_info_from_wikidata("Q16836245")

        # Define the REST API endpoint for the Wikidata item
        info = dict()
        # print("wiki:", wikidata_code)


        # Define the SPARQL endpoint and query
        sparql_url = "https://query.wikidata.org/sparql"
        query = f"""
        SELECT ?property ?propertyLabel ?value ?valueLabel
        WHERE {{
        wd:{wikidata_code} ?property ?value.
        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
        }}
        """

        key_to_get = {
            'http://www.wikidata.org/prop/direct/P18': 'image',
            'http://www.wikidata.org/prop/direct/P495': 'country',
        }

        # Send the request to the Wikidata SPARQL endpoint
        response = requests.get(sparql_url, params={'query': query, 'format': 'json'})

        # Parse the response
        data = response.json()
        # print(data)

        # Check and print the results
        if "results" in data and "bindings" in data["results"]:
            for result in data["results"]["bindings"]:
                property_label = result["propertyLabel"]["value"]
                value_label = result.get("valueLabel", {}).get("value", "No label")

                # print(f"{property_label}: {value_label}")
                if(property_label in key_to_get.keys()):
                    info[key_to_get[property_label]] = value_label
        else:
            print("No results found.")

        return info