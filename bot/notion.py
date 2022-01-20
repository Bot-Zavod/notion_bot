import json
import os
from typing import List

import requests
from dotenv import load_dotenv

load_dotenv()

NOTION_API_KEY = os.getenv("NOTION_API_KEY", "")
DATABASE_ID = os.getenv("DATABASE_ID", "")

url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": "2021-08-16",
    "Content-Type": "application/json",
}


def list_tasks() -> List[str]:
    filter_dict = {
        "filter": {
            "and": [
                {"property": "Когда начать?", "select": {"equals": "Сегодня"}},
                {"property": "Сделано?", "checkbox": {"equals": False}},
            ]
        }
    }
    payload = json.dumps(filter_dict)

    response = requests.request("POST", url, headers=headers, data=payload)
    response.raise_for_status()

    results = response.json()
    tasks = []

    for row in results["results"]:
        title = row["properties"]["Обезьянопонятная задача"]["title"][0]["plain_text"]
        tasks.append(title)

    return tasks
