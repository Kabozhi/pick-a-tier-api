from http import HTTPStatus
import os
import requests

def search_decals(query, page_num=1):
    url = 'https://search.roblox.com/catalog/json'
    params = {
        'Category': 8,  # Decal Category
        'Subcategory': 1,  # Subcategory look for all
        'Keyword': query,
        'ResultsPerPage': 20,
        'PageNumber': page_num,
        'SortAggregation': 3
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raises an error for bad status codes

        raw_results = response.json()  # Assuming the response is in JSON format

        # Format the results
        formatted_results = [
            {
                'AssetId': item.get('AssetId'),
                'Name': item.get('Name'),
                'Description': item.get('Description', 'No description available'),
                'Creator': item.get('Creator', 'Unknown creator')
            }
            for item in raw_results
        ]

        return formatted_results

    except requests.exceptions.RequestException as e:
        return None



def main(args):
    query = args.get("query")
    page_num = args.get("pageNum")

    results = search_decals(query, page_num)

    if not results:
        return {
            "statusCode" : HTTPStatus.BAD_REQUEST,
            "body" : "An error occured"
        }

    
    return {
        "statusCode" : HTTPStatus.ACCEPTED,
        "body" : results
    }