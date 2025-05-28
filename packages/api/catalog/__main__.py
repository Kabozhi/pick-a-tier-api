from http import HTTPStatus
import os
import requests

def search_decals(query, page_num=1):
    url = 'https://catalog.roblox.com/v1/search/items'
    params = {
        'Category': 8,  # Decals
        'Limit': 10,
        'Keyword': query,
        'Page': page_num,
        'SortType': 3,
        'Subcategory': 1,
        'CreatorType': 'User'
    }

    headers = {
        'User-Agent': 'Mozilla/5.0'  # Helps avoid being blocked
    }

    try:
        response = requests.get(url, params=params, headers=headers)
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
    
    print(f"Function called with args: {args}")
    results = search_decals(query, page_num)

    if not results:
        print("search_decals returned None or empty result.")
        return {
            "statusCode" : HTTPStatus.BAD_REQUEST,
            "body" : "An error occured"
        }

    
    return {
        "statusCode" : HTTPStatus.ACCEPTED,
        "body" : results
    }
