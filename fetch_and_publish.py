#!/usr/bin/env python3
import json, datetime, subprocess, sys
import requests
from bs4 import BeautifulSoup

URL_CITY = {
    "damascus": "https://sp-today.com/en/currency/us_dollar/city/damascus",
    "aleppo":   "https://sp-today.com/en/currency/us_dollar/city/aleppo"
}
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
GITHUB_FILE = "live_board.json"   # in same repo

def get_city_rate(city_url):
    """Return (buy, sell) tuple or (None, None) on error."""
    try:
        r = requests.get(city_url, headers=HEADERS, timeout=15)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "lxml")
        buy  = soup.select('div.cur-data span.value')[0].get_text(strip=True)
        sell = soup.select('div.cur-data span.value')[1].get_text(strip=True)
        return int(buy), int(sell)
    except Exception as e:
        print(f"Error fetching {city_url}: {e}", file=sys.stderr)
        return None, None

def build_snapshot():
    ts = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    board = {"timestamp": ts, "cities": {}}
    for city, url in URL_CITY.items():
        buy, sell = get_city_rate(url)
        if buy and sell:
            board["cities"][city] = {"buy": buy, "sell": sell, "spread": sell - buy}
        else:
            board["cities"][city] = None
    return board

def publish_to_repo(data_dict):
    """Write JSON & git-commit-push."""
    with open(GITHUB_FILE, "w", encoding="utf-8") as f:
        json.dump(data_dict, f, ensure_ascii=False, indent=2)
    # git add / commit / push
    subprocess.run(["git", "add", GITHUB_FILE], check=True)
    subprocess.run(["git", "commit", "-m", f"rates {data_dict['timestamp']}"], check=True)
    subprocess.run(["git", "push"], check=True)
    print("Pushed to GitHub Pages.")

def main():
    board = build_snapshot()
    print(json.dumps(board, ensure_ascii=False, indent=2))
    publish_to_repo(board)

if __name__ == "__main__":
    main()