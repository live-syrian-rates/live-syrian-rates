#!/usr/bin/env python3
import json, datetime, requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

def get_usd(city: str):
    url  = f"https://sp-today.com/en/currency/us_dollar/city/{city}"
    soup = BeautifulSoup(requests.get(url, headers=HEADERS, timeout=15).text, "lxml")
    buy  = int(soup.select('div.cur-data span.value')[0].get_text(strip=True))
    sell = int(soup.select('div.cur-data span.value')[1].get_text(strip=True))
    return {"buy": buy, "sell": sell, "spread": sell - buy}

def get_euro(city: str):
    soup = BeautifulSoup(requests.get("https://sp-today.com/en/", headers=HEADERS, timeout=15).text, "lxml")
    vals = [s.get_text(strip=True).replace(",", "") for s in soup.select('span.value')]
    # indices 2 & 3 are Euro buy/sell (same for both cities on homepage)
    buy  = int(vals[2])
    sell = int(vals[3])
    return {"buy": buy, "sell": sell, "spread": sell - buy}

def get_gold_oz():
    soup = BeautifulSoup(requests.get("https://sp-today.com/en/", headers=HEADERS, timeout=15).text, "lxml")
    vals = [s.get_text(strip=True).replace(",", "") for s in soup.select('span.value')]
    return float(vals[7].replace("$", ""))

def get_bitcoin_oz():
    soup = BeautifulSoup(requests.get("https://sp-today.com/en/", headers=HEADERS, timeout=15).text, "lxml")
    vals = [s.get_text(strip=True).replace(",", "") for s in soup.select('span.value')]
    return float(vals[8].replace("$", "").replace(",", ""))

def build_snapshot():
    ts = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    return {
        "timestamp": ts,
        "cities": {
            "damascus": {"usd": get_usd("damascus"), "euro": get_euro("damascus")},
            "aleppo":   {"usd": get_usd("aleppo"),   "euro": get_euro("aleppo")}
        },
        "gold_oz":  get_gold_oz(),
        "bitcoin_oz": get_bitcoin_oz()
    }

def main():
    board = build_snapshot()
    print(json.dumps(board, ensure_ascii=False, indent=2))
    with open("live_board.json", "w", encoding="utf-8") as f:
        json.dump(board, f, ensure_ascii=False, indent=2)
    print("Saved to live_board.json")

if __name__ == "__main__":
    main()