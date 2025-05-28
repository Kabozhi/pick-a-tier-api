from http import HTTPStatus
import requests
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Ensure all INFO level logs show up

def search_decals(query, page_num=1):
    url = 'https://catalog.roblox.com/v1/search/items'
    params = {
        'Category': 8,  # Decals
        'Limit': 30,    # Valid limit value based on Roblox API
        'Keyword': query,
        'Page': page_num,
        'SortType': 3,
        'Subcategory': 1,
        'CreatorType': 'User'
    }

    logger.info(f"Searching for decals with query: {query}, page: {page_num}")
    
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
            for item in raw_results.get('data', [])
        ]

        logger.info(f"Formatted results: {formatted_results}")
        return formatted_results

    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching decals: {e}")
        return None

def main(args):
    logger.info(f"Received args: {args}")

    query = args.get("query")
    page_num = args.get("pageNum")

    if not query or not page_num:
        logger.warning("Missing query or pageNum in request.")
        return {
            "statusCode": HTTPStatus.BAD_REQUEST,
            "body": "Missing query or pageNum"
        }

    logger.info(f"Calling search_decals with query={query}, page_num={page_num}")
    results = search_decals(query, page_num)

    if not results:
        logger.warning("search_decals returned None or empty result.")
        return {
            "statusCode": HTTPStatus.BAD_REQUEST,
            "body": "An error occurred"
        }

    logger.info(f"search_decals returned: {results}")
    return {
        "statusCode": HTTPStatus.ACCEPTED,
        "body": results
    }
