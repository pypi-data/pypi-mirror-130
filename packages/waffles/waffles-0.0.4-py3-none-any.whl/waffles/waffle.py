import random
import typing as t
import webbrowser

import httpx

from waffles import sprinkles
from waffles.baker import waffle_baker

URL = "https://gw.hellofresh.com/api/recipes/search"


headers = {
    "accept": "applicaton/json",
    "Authorization": f"Bearer {sprinkles.TOKEN}",
    "user-agent": sprinkles.USER_AGENT,
}


def get_receipts_list(payload: t.Dict) -> t.Dict:
    response = httpx.get(URL, params=payload, headers=headers)
    return response.json()


def get_random_receipt(json_response: t.Dict) -> t.Dict:

    receipts = [
        {
            "name": receipt["name"],
            "link": receipt["cardLink"],
            "ingredients": receipt["ingredients"],
            "serving": receipt["yields"][0]["ingredients"],
        }
        for receipt in json_response["items"]
    ]

    ingredients_ids = {
        ingredient["id"]: ingredient["name"]
        for receipt in receipts
        for ingredient in receipt["ingredients"]
    }
    random_receipt = random.choice(receipts)
    return {
        "dish": random_receipt["name"],
        "link": random_receipt["link"],
        "shopping list": {
            ingredients_ids[serving["id"]]: f'{serving["amount"]} {serving["unit"]}'
            for serving in random_receipt["serving"]
        },
    }


params = {
    "limit": sprinkles.LIMIT,
    "locale": sprinkles.LANGUAGE,
    "country": sprinkles.COUNTRY,
    "max-prep-time": sprinkles.MAX_PREP_TIME,
    "sort": "-favorites",
}

response_json = get_receipts_list(payload=params)
cook = get_random_receipt(response_json)
webbrowser.open_new_tab(cook["link"])
waffle_baker(cook)
