import os
import requests
import xml.etree.ElementTree as ET

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY")

RSS_SOURCES = [
    "https://punchng.com/feed/",
    "https://www.vanguardngr.com/feed/",
    "https://www.premiumtimesng.com/feed/",
    "https://dailypost.ng/feed"
]

KEYWORDS = ["tinubu", "apc", "bola", "campaign", "shettima", "government", "election", "presidency", "nigeria"]

def fetch_and_push():
    headers = {
        "apikey": SUPABASE_SERVICE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }

    for url in RSS_SOURCES:
        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            if response.status_code != 200:
                continue

            root = ET.fromstring(response.content)
            for item in root.findall(".//item"):
                title_elem = item.find("title")
                if title_elem is None or not title_elem.text:
                    continue

                title = title_elem.text.strip()
                lower_title = title.lower()

                if not any(kw in lower_title for kw in KEYWORDS):
                    continue

                image_url = ""
                enclosure = item.find("enclosure")
                if enclosure is not None:
                    image_url = enclosure.get("url", "")

                payload = {
                    "title": title,
                    "image_url": image_url,
                    "source": "RSS Aggregator"
                }

                res = requests.post(SUPABASE_URL, json=payload, headers=headers)
                if res.status_code in [200, 201]:
                    print(f"Added: {title[:40]}...")
        except Exception as e:
            print(f"Error parsing {url}: {e}")

if __name__ == "__main__":
    fetch_and_push()

