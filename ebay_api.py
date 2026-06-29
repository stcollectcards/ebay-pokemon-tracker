import requests
import time
from config import EBAY_CLIENT_ID, EBAY_CLIENT_SECRET

EBAY_TOKEN_URL = "https://api.ebay.com/identity/v1/oauth2/token"
EBAY_SEARCH_URL = "https://api.ebay.com/buy/browse/v1/item_summary/search"

_access_token = None
_token_expiry = 0


def get_access_token():
    global _access_token, _token_expiry

    if _access_token and time.time() < _token_expiry:
        return _access_token

    response = requests.post(
        EBAY_TOKEN_URL,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={
            "grant_type": "client_credentials",
            "scope": "https://api.ebay.com/oauth/api_scope",
        },
        auth=(EBAY_CLIENT_ID, EBAY_CLIENT_SECRET),
    )

    response.raise_for_status()
    data = response.json()

    _access_token = data["access_token"]
    _token_expiry = time.time() + int(data["expires_in"]) - 60

    return _access_token


def search_ebay(query, limit=25):
    token = get_access_token()

    headers = {
        "Authorization": f"Bearer {token}",
        "X-EBAY-C-MARKETPLACE-ID": "EBAY_US",
    }

    params = {
        "q": query,
        "limit": limit,
        "sort": "newlyListed"
    }

    response = requests.get(
        EBAY_SEARCH_URL,
        headers=headers,
        params=params
    )

    response.raise_for_status()
    data = response.json()

    results = []

    for item in data.get("itemSummaries", []):
        results.append({
            "item_id": item.get("itemId"),
            "title": item.get("title"),
            "price": float(item.get("price", {}).get("value", 0)),
            "url": item.get("itemWebUrl"),
            "seller": item.get("seller", {}).get("username"),
            "timestamp": item.get("itemCreationDate")
        })

    return results
