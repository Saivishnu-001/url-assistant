import json
from rapidfuzz import fuzz

# Load apps data
with open("apps.json", "r") as f:
    apps = json.load(f)

# Build keyword lookup
ALL_KEYWORDS = set()
for app in apps:
    for keyword in app["keywords"]:
        ALL_KEYWORDS.add(keyword.lower())

def find_best_match(user_input):
    user_input = user_input.lower().strip()

    # Allow short forms only if defined
    if len(user_input) < 4 and user_input not in ALL_KEYWORDS:
        return None, 0

    best_match = None
    highest_score = 0

    for app in apps:
        for keyword in app["keywords"]:
            score = fuzz.token_set_ratio(user_input, keyword.lower())

            if score > highest_score:
                highest_score = score
                best_match = app

    return best_match, highest_score

# Agent loop
while True:
    user_input = input("\nAsk something: ")

    match, score = find_best_match(user_input)

    if match and score > 60:
        login_info = match.get("Login", "Not Specified")
        vpn_status = match.get("VPN Required", "NO")

        print("\n═══════════════════════")
        print(f"🔗 {match['name']}")
        print(f"🌐 URL: {match['url']}")
        print(f"🔑 Login: {login_info}")
        print(f"🔐 VPN Required: {vpn_status}")
        print("═══════════════════════")

    else:
        print("\n❌ No matching application found")
