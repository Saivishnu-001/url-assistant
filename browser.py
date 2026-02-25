import json
import subprocess
from rapidfuzz import fuzz

with open("apps.json", "r") as f:
    apps = json.load(f)

def find_best_match(user_input):
    user_input = user_input.lower().strip()

    best_match = None
    highest_score = 0

    for app in apps:
        for keyword in app["keywords"]:
            score = fuzz.token_set_ratio(user_input, keyword.lower())

            if score > highest_score:
                highest_score = score
                best_match = app

    return best_match, highest_score

while True:
    user_input = input("\nAsk something: ")

    match, score = find_best_match(user_input)

    if match and score > 60:
        login_info = match.get("Login", "Not Specified")
        vpn_status = match.get("VPN Required", "NO")

        print("\n═══════════════════════")
        print(f"🔗 {match['name']}")
        print(f"🔑 Login: {login_info}")
        print(f"🔐 VPN Required: {vpn_status}")
        print("🌐 Opening browser...")
        print("═══════════════════════")

        # ✅ FULL URL SAFE (handles & properly)
        subprocess.run(f'cmd.exe /c start "" "{match["url"]}"', shell=True)

    else:
        print("\n❌ No matching application found")
