import json
from fastapi import FastAPI
from rapidfuzz import fuzz

app = FastAPI()

with open("apps.json", "r") as f:
    apps = json.load(f)

ALL_KEYWORDS = set()

for app_data in apps:
    for keyword in app_data["keywords"]:
        ALL_KEYWORDS.add(keyword.lower())

def find_best_match(user_input):
    user_input = user_input.lower().strip()

    if len(user_input) < 4 and user_input not in ALL_KEYWORDS:
        return None, 0

    best_match = None
    highest_score = 0

    for app_data in apps:
        for keyword in app_data["keywords"]:
            score = fuzz.token_set_ratio(user_input, keyword.lower())

            if score > highest_score:
                highest_score = score
                best_match = app_data

    return best_match, highest_score

@app.get("/search")
def search_app(query: str):
    match, score = find_best_match(query)

    if match and score > 60:
        return {
            "status": "success",
            "name": match["name"],
            "url": match["url"]
        }

    return {
        "status": "not_found"
    }
