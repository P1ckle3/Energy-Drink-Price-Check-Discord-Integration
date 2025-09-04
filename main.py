from dhooks import Webhook
from dhooks import Embed
from dotenv import load_dotenv
import os
import json
import requests
from requests.exceptions import (
    RequestException,
)  # FIX: JSONDecodeError isn’t from requests.exceptions
import re
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def main():
    load_dotenv()
    link = os.getenv("WEBHOOK_URL")

    hook = Webhook(link)

    hook.send("Webhook Initialised...")
    print("[/] Webhook Initialised...")

    # Function that checks Woolworths for 4-pack energy drink specials
    def wooliesCheck():
        # Send startup message to discord webhook
        hook.send("Checking Woolworths for 4-pack energy drink specials...")
        # --- Woolies setup ---
        Wlink = "https://www.woolworths.com.au/apis/ui/Search/products"

        # Get fresh cookies from Woolworths using Selenium
        import time

        def get_fresh_cookies():
            print("[/] Retrieving fresh cookies from Woolworths...")
            options = Options()
            options.add_argument("--headless")
            driver = None
            cookies = []
            try:
                driver = webdriver.Chrome(options=options)
                driver.get(
                    "https://www.woolworths.com.au/shop/search/products?searchTerm=energy%20drinks"
                )
                time.sleep(5)  # Wait for cookies to be set
                cookies = driver.get_cookies()
                print(f"[/] Retrieved {len(cookies)} cookies")
            except Exception as e:
                print(f"X Failed to get cookies: {e}")
            finally:
                if driver:
                    driver.quit()
            # Convert cookies to "name=value; ..." string
            if not cookies:
                raise RuntimeError("No cookies retrieved from Woolworths")
            cookie_str = "; ".join([f"{c['name']}={c['value']}" for c in cookies])
            return cookie_str

        fresh_cookie = get_fresh_cookies()

        # Headers
        WHeader = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "Origin": "https://www.woolworths.com.au",
            "Referer": "https://www.woolworths.com.au/shop/search/products?searchTerm=energy%20drinks",
            "Cookie": fresh_cookie,
        }

        # Pay load data
        Wpayload = {
            "Filters": [],
            "IsSpecial": False,
            "Location": "/shop/search/products?searchTerm=energy%20drinks",
            "PageNumber": 1,
            "PageSize": 36,
            "SearchTerm": "energy drinks",
            "SortType": "TraderRelevance",
            "ExcludeSearchTypes": ["UntraceableVendors"],
        }

        # --- get data ---
        resp = None  # FIX: ensure resp exists even if request fails
        try:
            print(f"[/] Sending request to {Wlink}")
            resp = requests.post(Wlink, headers=WHeader, json=Wpayload, timeout=60)
            print(f"[/] Succesful connecton...HTTP {resp.status_code}")
            if resp.status_code != 200:
                print(f"Body (truncated): {resp.text[:500]}")
                resp = None  # FIX: mark as failed so we don't use it below
        except RequestException as e:
            print(f"X Request failed: {e}")
            resp = None  # FIX: keep resp defined

        if not resp:
            print("!X! No response, skipping processing.")
            raise SystemExit(1)  # FIX: stop here so we don’t hit resp.json() below

        # FIX: only call .json() once, after the guard above
        data = resp.json()

        out_path = os.path.abspath("woolies_products.json")
        try:
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print(f"[/] Saved results to {out_path}")
        except OSError as e:
            print(f"X Failed to write file: {e}")

        # Your JSON shape is nested: data["Products"] -> list of groups, each with ["Products"] list
        groups = data.get("Products", [])
        products = [p for g in groups for p in g.get("Products", [])]

        discounted = []

        print("Itterating through products...")
        for p in products:
            # FIX: guard DisplayName so .lower() never crashes
            name = (p.get("DisplayName") or "").strip()
            price = p.get("Price")
            was = p.get("WasPrice")
            savingsamount = p.get("SavingsAmount")

            if (
                "x 4 pack" in name.lower()
                and price is not None
                and was is not None
                and price < was
            ):
                # FIX: store structured data (tuple), not a formatted string
                discounted.append((name, price, was, savingsamount))

        print("Generatig embed for Discord...")
        embed = Embed(
            title="Woolies 4-Pack Specials",
            description="4-Pack energy drinks that are on sale",
            color=0xD20F39,
        )

        # Uses the structured tuples we appended above
        for i, (name, price, was, savingsamount) in enumerate(discounted[:10], 1):
            value = (
                f"${price:.2f} (was ${was:.2f})"
                if (price is not None and was is not None)
                else (f"${price:.2f}" if price is not None else "—")
            )
            embed.add_field(name=f"{i}. {name}", value=value, inline=False)

        # FIX: correct argument name is embed= (lowercase)
        print("Sending Embed to Discord...")
        hook.send(embed=embed)

    # Call the function to perform the check
    wooliesCheck()


# Call the main function if the script is run directly from the file (not imported)
if __name__ == "__main__":
    main()
