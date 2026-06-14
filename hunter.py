send_telegram("🧪 TEST: el bot está funcionando")

import requests
import json
import time
from bs4 import BeautifulSoup
import os

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

KEYWORDS = [
    "new 3ds xl lcd",
    "new 3ds ll upper screen",
    "new 3ds xl pulled",
    "new 3ds ll parts",
]

COUNTRIES = {
    "ES": "https://www.ebay.es/sch/i.html",
    "DE": "https://www.ebay.de/sch/i.html",
    "UK": "https://www.ebay.co.uk/sch/i.html",
    "US": "https://www.ebay.com/sch/i.html",
}

def load_seen():
    try:
        with open("seen.json", "r") as f:
            return set(json.load(f))
    except:
        return set()

def save_seen(seen):
    with open("seen.json", "w") as f:
        json.dump(list(seen), f)

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def is_good(text):
    bad = ["replacement", "aftermarket", "shell", "copy"]
    good = ["original", "pulled", "oem", "genuine", "from console"]

    text = text.lower()

    if any(b in text for b in bad):
        return False

    return any(g in text for g in good)

def search_ebay(query, url):
    r = requests.get(url, params={"_nkw": query}, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(r.text, "html.parser")

    items = soup.select(".s-item")

    results = []

    for item in items[:10]:
        title = item.select_one(".s-item__title")
        link = item.select_one(".s-item__link")

        if not title or not link:
            continue

        title_text = title.text
        link_url = link["href"]

        if title_text == "Shop on eBay":
            continue

        results.append((title_text, link_url))

    return results


def main():
    seen = load_seen()

    for country, url in COUNTRIES.items():
        for kw in KEYWORDS:
            results = search_ebay(kw, url)

            for title, link in results:

                uid = link.split("?")[0]

                if uid in seen:
                    continue

                if not is_good(title):
                    continue

                msg = f"""🎮 NUEVO ITEM eBay ({country})

📝 {title}

🔗 {link}
"""
                send_telegram(msg)

                seen.add(uid)
                time.sleep(1)

    save_seen(seen)

if __name__ == "__main__":
    main()
