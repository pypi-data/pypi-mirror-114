import json
import requests as req
from .utils import format_query_result_as_csv


def list_collections(collections_url):
    return req.get(collections_url).json()


def list_tables(collections_url, collection_name):
    collection_tables_url = f"{collections_url}/{collection_name}/data-connect/tables"
    return req.get(collection_tables_url).json()


def query(collections_url, collection_name, query, format="json"):
    collection_query_url = f"{collections_url}/{collection_name}/data-connect/search"
    results = req.post(collection_query_url, json={"query": query})
    if format == "csv":
        return format_query_result_as_csv(results.json()["data"])
    else:
        # load and redump the json to allow for proper formatting
        return json.dumps(results.json()["data"], indent=4)
