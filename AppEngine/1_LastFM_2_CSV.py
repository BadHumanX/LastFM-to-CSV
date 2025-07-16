import os
import csv
import requests
from datetime import datetime

# Hardcoded public API key
API_KEY = "1b667b3b606ae6768567d23c811ad373"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "..", "Output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def extract_username(input_str):
    input_str = input_str.strip()
    if input_str.startswith("https://www.last.fm/user/"):
        return input_str.split("/")[-1]
    return input_str

def parse_date_or_datetime(dt_str, is_start=True):
    dt_str = dt_str.strip()
    try:
        dt = datetime.strptime(dt_str, "%d %B %Y %H:%M:%S")
    except ValueError:
        dt = datetime.strptime(dt_str, "%d %B %Y")
        dt = dt.replace(hour=0, minute=1, second=0) if is_start else dt.replace(hour=23, minute=59, second=59)
    return int(dt.timestamp())

def get_time_range_from_user():
    print("Choose time range option:")
    print("1. All time\n2. Specific time range")
    choice = input("Enter 1 or 2: ").strip()

    if choice == "1":
        return None, None
    elif choice == "2":
        start = input("Enter start date (e.g. '01 July 2025'): ")
        end = input("Enter end date (e.g. '07 July 2025'): ")
        return parse_date_or_datetime(start, True), parse_date_or_datetime(end, False)
    return None, None

def fetch_loved_tracks(username):
    loved = set()
    page = 1
    while True:
        params = {
            "method": "user.getlovedtracks",
            "user": username,
            "api_key": API_KEY,
            "format": "json",
            "limit": 200,
            "page": page
        }
        try:
            resp = requests.get("https://ws.audioscrobbler.com/2.0/", params=params)
            resp.raise_for_status()
            data = resp.json()
            tracks = data.get("lovedtracks", {}).get("track", [])
            for t in tracks:
                loved.add((t["artist"]["name"], t["name"]))
            print(f"[♥] Page {page} - Fetched {len(tracks)} loved tracks")
            if len(tracks) < 200:
                break
            page += 1
        except Exception as e:
            print(f"[⚠️] Failed to fetch loved tracks on page {page}: {e}")
            break
    return loved

def fetch_all_scrobbles(username, time_from=None, time_to=None):
    all_tracks = []
    page = 1
    while True:
        params = {
            "method": "user.getrecenttracks",
            "user": username,
            "api_key": API_KEY,
            "format": "json",
            "limit": 200,
            "page": page
        }
        if time_from: params["from"] = time_from
        if time_to: params["to"] = time_to

        resp = requests.get("https://ws.audioscrobbler.com/2.0/", params=params)
        resp.raise_for_status()
        data = resp.json()
        tracks_data = data.get("recenttracks", {}).get("track", [])
        if not tracks_data:
            break
        print(f"[⏳] Fetched page {page}, {len(tracks_data)} tracks")
        all_tracks.extend(tracks_data)
        if len(tracks_data) < 200:
            break
        page += 1
    return all_tracks

def process_scrobbles(raw_scrobbles, loved_set):
    combined = {}
    for track in raw_scrobbles:
        if not isinstance(track, dict) or "date" not in track or "#text" not in track["date"]:
            continue
        artist = track["artist"]["#text"]
        title = track["name"]
        timestamp = int(track["date"]["uts"])
        played_time = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
        loved = 1 if (artist, title) in loved_set else 0
        key = (artist, title)
        if key not in combined:
            combined[key] = {
                "Played Time": played_time,
                "Artist": artist,
                "Track Title": title,
                "Loved": loved,
                "Playcount": 1
            }
        else:
            combined[key]["Playcount"] += 1
            combined[key]["Played Time"] = max(combined[key]["Played Time"], played_time)
            combined[key]["Loved"] = max(combined[key]["Loved"], loved)
    return list(combined.values())

def save_csv(scrobbles, csv_path):
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Played Time", "Artist", "Track Title", "Loved", "Playcount"])
        writer.writeheader()
        writer.writerows(scrobbles)

def main():
    user_input = input("\nEnter Last.fm username or profile URL: ")
    username = extract_username(user_input)
    time_from, time_to = get_time_range_from_user()

    if time_from and time_to:
        start_str = datetime.fromtimestamp(time_from).strftime("%d %B %Y")
        end_str = datetime.fromtimestamp(time_to).strftime("%d %B %Y")
        csv_filename = f"scrobbles ({start_str} to {end_str}).csv"
    else:
        csv_filename = "scrobbles_all_time.csv"
    csv_path = os.path.join(OUTPUT_DIR, csv_filename)

    print(f"\n[🎧] Fetching loved tracks for {username}...")
    loved_set = fetch_loved_tracks(username)

    print(f"[📥] Fetching recent tracks...")
    raw_scrobbles = fetch_all_scrobbles(username, time_from, time_to)
    final_scrobbles = process_scrobbles(raw_scrobbles, loved_set)

    if not final_scrobbles:
        print("[✗] No scrobbles found.")
        return

    save_csv(final_scrobbles, csv_path)
    print(f"[✓] Saved {len(final_scrobbles)} scrobbles to {csv_path}")

if __name__ == "__main__":
    main()
