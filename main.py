from dhooks import Webhook
from dhooks import Embed
from dotenv import load_dotenv
import os
import json
import requests
from requests.exceptions import RequestException  # FIX: JSONDecodeError isn’t from requests.exceptions
import re
from pathlib import Path

def main():
    load_dotenv()
    link = os.getenv("WEBHOOK_URL")

    hook = Webhook(link)

    hook.send("Initialised")

    def wooliesCheck():
        # --- Woolies setup ---
        Wlink = "https://www.woolworths.com.au/apis/ui/Search/products"
        WHeader = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "Origin": "https://www.woolworths.com.au",
            "Referer": "https://www.woolworths.com.au/shop/search/products?searchTerm=energy%20drinks",
            "Cookie": "_abck=694F6B1DB3691A52A896C5E04C2D106E~-1~YAAQRVbbF4SlmeWYAQAArHBMDw78mOwl8JG5BZbr/pjar0o4tM+wrpeR6sqbQsK4pNMeTfpQsAqd7LbghdHBexY2t//suZqiL2OJzmYw3SE8HbZA9HK8HeNU8/jCmbi4WzSIcWr4aJ3HcUWPTVjSgrwDLU01w4MLCJsuOeB0GYJbWl8b5uyH9TzZ96UFq1aO1LkxhtG/T1raXpvtv6ZGl1/w5XwMNS/gR2b9DwrxsrNQZ7aXDo8fovbYlz+bONQ3K/sy+1yH2GAn4Nt6/8+/V4jgnuN8zR7tcvsF3m+yV/ss+fX3Pm/kUKwCFgZj59DOEDW3bw4fh0NWF3z7FRXCNRGelNeme5ryp3uP7YzrSuprQQM/Eynjy7LxlPqLIrZYRRP1bgTRNd5Hf0BQ/K9y1hUarOmTltQlo5sHQ0KrfL5/hV/Rg9JRBvW6IbIVyTASHKRpO4RQSI1MMQv8HxmYP+/e1+8aFMu6/+VkSaExnvgaoNLSPZUOqq1BwqIDCH5D2oYixo/bV1EDRizvw1bPGONCQ9AvbY9icecOLfm9aPm92+AwDrSenx1hmb68PDncJKQwna1s3f7dzP7xJx+RpYo71Fue5DcnclztHkmjyF/K3P19Nwuzq66yNM5FxhN2Bk+SVNDBwo9qHqqTksdyTN3aDpY7WLJZihH/j+QJNnZoRuGMDliQZMomdEQ0shOd4iqLgkDzPKAplOA3pken8oqNh+oWaw86Czr/iJ4iWXTXxE0K6ON5N0rw2Skbj6aPPQwHUl/zH4PNz7W5YF08IkXQ1KUGLOzeQ6ITPNh2PAmRaX+5E3NQd4uWDf5bj7Zl4hxbbJ0MjrUCMZG86hvxB4YAlSJlecv6UsMHXQ7ZCFf3UkjUMOs510j/ZecRJdAltN99/TbL3sQH8JH0WSJKmXXS9ZRRX+MhAo4C7gSCbGNztyOCpXVYgVlwMP+hhhRosRpq~-1~-1~1756901417~~; ai_user=tFFfL8Zwi658XCJF8fF9Gf^|2025-08-08T08:52:47.093Z; AMCV_4353388057AC8D357F000101^%^40AdobeOrg=179643557^%^7CMCIDTS^%^7C20335^%^7CMCMID^%^7C30086187825909179478232758668271313851^%^7CMCOPTOUT-1756905491s^%^7CNONE^%^7CvVersion^%^7C5.5.0; mbox=PC^#b233dbcc9d034aa59a6bd00f2aa8580b.36_0^#1820143074^|session^#dc5b7de3a9374c37864560dd614feb62^#1756900153; bff_region=syd2; akaalb_woolworths.com.au=~op=www_woolworths_com_au_ZoneA:PROD-ZoneA^|www_woolworths_com_au_BFF_SYD_Launch:WOW-BFF-SYD2^|~rv=81~m=PROD-ZoneA:0^|WOW-BFF-SYD2:0^|~os=43eb3391333cc20efbd7f812851447e6~id=4897a7ab52a0816a85951a850761f94a; bm_sz=7AA4C7DEE1610F7DBC35B324DE30087D~YAAQRVbbF8aEmeWYAQAApmdMDxzRp/l4wEMb3okit0SXHmSFnP3ZPvKUEs8PG5jPnOpc9Q5rDaJK3NW/KWKPhzWat3HrWF4psTj/hd96mOtdG9W7ppHJfZ+vXlG8GcSDwVuOhgUpIwvIPPZ01FDTwUwkCCp6j++e7QkVdCb69JPlJnJ7on3wkAvzL2Id02Ld5MoFYQuZdEl9dZKnph6aiVi0VHoj9F4ByJSy7atwGQG+09HuKl/NMSg37LqLVpvoIJkuwHb9pYoyZ3D3/qexZ3skGeCkGBCugrSC/0qzYjsdWF/TJu0VjoVFVC94JoEr78MhR0OlhMmWapCcFLiiFdjxpI1/pxS52oF42n5CimEsPrj5z3HRYOYHep+VeSIOHtfE0QBknov26HVAAv6mYf4xU3vo26VuBAtg24+uZft7o7U6ue3lkDrYwqLAHt00H3XlNge/XVLqdcNxl261D5kDolLvAIx5Lxn0ldoLvcant4RNCC5o/PCPUCIHFD2CBQziRjSCzxw8SKR7SdsIUWPmrr1T18vW2DJhkjEyxAPReFihAQ==~4469314~3487283; at_check=true; ai_session=yxSe/+f3GEn0mIEVQlsuld^|1756896063564^|1756898291162; AMCVS_4353388057AC8D357F000101^%^40AdobeOrg=1; INGRESSCOOKIE=1756890617.78.68.415870^|37206e05370eb151ee9f1b6a1c80a538; dtCookie=v_4_srv_4_sn_02944CF6DCABEE1CB71A5FF4E94BAD72_perc_100000_ol_0_mul_1_app-3Af908d76079915f06_0_rcs-3Acss_0; utag_main_v_id=019888e20cb4009162e1516ae31805050004500d00bd0; utag_main__sn=5; utag_main_vapi_domain=woolworths.com.au; utag_main_dc_visit=4; fullstoryEnabled=false; s_cc=true; w-rctx=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE3NTY4OTc4NjQsImV4cCI6MTc1NjkwMTQ2NCwiaWF0IjoxNzU2ODk3ODY0LCJpc3MiOiJXb29sd29ydGhzIiwiYXVkIjoid3d3Lndvb2x3b3J0aHMuY29tLmF1Iiwic2lkIjoiMCIsInVpZCI6IjMzOGNkM2Y1LWIyYmUtNDc5My04NjgxLTJlYzMwYzdmY2YzZSIsIm1haWQiOiIwIiwiYXV0IjoiU2hvcHBlciIsImF1YiI6IjAiLCJhdWJhIjoiMCIsIm1mYSI6IjEifQ.C0tFGQEYpv2lUgcIPUnXJf0v9OqEYkr3UPvGRiok-m8BTGQmMawLTL3Joxg7IFmfd_zbSmbtpl45qpC02wKfIZOxhNmyfH4e18VNBbpuuAR-1tz6r3plzkF5Q46qAZ9oFbCnNiZD4_l5EIKAKdLDRxs2i69FUIGYHq-HyP1mjWr98w3ELPk2ymROSbiTqRDW_hZXa2NtL0rwkxVGC-vKTQ8Lq5wYI1qei_kU-ggV6KSKcmzWJT-udtdXUULC12P1_6GOroDxx7SdFRO5M4Cr9WCAU_1R1GX9MgQwKORqhDOLhVqbwDaniK4VYEwiJDx-lKIhcNGacVK6z5EJh3BEvg; wow-auth-token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE3NTY4OTc4NjQsImV4cCI6MTc1NjkwMTQ2NCwiaWF0IjoxNzU2ODk3ODY0LCJpc3MiOiJXb29sd29ydGhzIiwiYXVkIjoid3d3Lndvb2x3b3J0aHMuY29tLmF1Iiwic2lkIjoiMCIsInVpZCI6IjMzOGNkM2Y1LWIyYmUtNDc5My04NjgxLTJlYzMwYzdmY2YzZSIsIm1haWQiOiIwIiwiYXV0IjoiU2hvcHBlciIsImF1YiI6IjAiLCJhdWJhIjoiMCIsIm1mYSI6IjEifQ.C0tFGQEYpv2lUgcIPUnXJf0v9OqEYkr3UPvGRiok-m8BTGQmMawLTL3Joxg7IFmfd_zbSmbtpl45qpC02wKfIZOxhNmyfH4e18VNBbpuuAR-1tz6r3plzkF5Q46qAZ9oFbCnNiZD4_l5EIKAKdLDRxs2i69FUIGYHq-HyP1mjWr98w3ELPk2ymROSbiTqRDW_hZXa2NtL0rwkxVGC-vKTQ8Lq5wYI1qei_kU-ggV6KSKcmzWJT-udtdXUULC12P1_6GOroDxx7SdFRO5M4Cr9WCAU_1R1GX9MgQwKORqhDOLhVqbwDaniK4VYEwiJDx-lKIhcNGacVK6z5EJh3BEvg; prodwow-auth-token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE3NTY4OTc4NjQsImV4cCI6MTc1NjkwMTQ2NCwiaWF0IjoxNzU2ODk3ODY0LCJpc3MiOiJXb29sd29ydGhzIiwiYXVkIjoid3d3Lndvb2x3b3J0aHMuY29tLmF1Iiwic2lkIjoiMCIsInVpZCI6IjMzOGNkM2Y1LWIyYmUtNDc5My04NjgxLTJlYzMwYzdmY2YzZSIsIm1haWQiOiIwIiwiYXV0IjoiU2hvcHBlciIsImF1YiI6IjAiLCJhdWJhIjoiMCIsIm1mYSI6IjEifQ.C0tFGQEYpv2lUgcIPUnXJf0v9OqEYkr3UPvGRiok-m8BTGQmMawLTL3Joxg7IFmfd_zbSmbtpl45qpC02wKfIZOxhNmyfH4e18VNBbpuuAR-1tz6r3plzkF5Q46qAZ9oFbCnNiZD4_l5EIKAKdLDRxs2i69FUIGYHq-HyP1mjWr98w3ELPk2ymROSbiTqRDW_hZXa2NtL0rwkxVGC-vKTQ8Lq5wYI1qei_kU-ggV6KSKcmzWJT-udtdXUULC12P1_6GOroDxx7SdFRO5M4Cr9WCAU_1R1GX9MgQwKORqhDOLhVqbwDaniK4VYEwiJDx-lKIhcNGacVK6z5EJh3BEvg; AKA_A2=A; ak_bmsc=31810B08A9110513D9AE7452189CD0A4~000000000000000000000000000000~YAAQRVbbF6LjlOWYAQAAZepFDxxDaHDSrEH3JIydOvX5q2Wk9DO+lzwSfpzXIcHYdXCQh7RNHFR+SekEfa4sKcgrYdazDFLOZ15x1Zxd+/rj8LgDJZ7UDbWiHqQ4p0oA2QkwVYCjRGQUfRd9zCRtWR6K/TJEY7f1QEyQcgjn/pmXnPUDp3z5vfKRfDqhiyIvSpWbKVzpKDV06ZP4hkwJ/0gxlvyWPDQOhBTvumNTWWNErgBxvgHaUM8YjUUOY+uZiwAHGPMZDaHeoQliPoRnYM6plPQk6KC8Wn8wqYXYPvIp37vD9hhsaSNDh86T4VEH3DMxBeloxLQjM3Qd9aHhAaNxU6P5DSfh3M7nMLdUuXffBda0IakPc81xhzAcbrrRCg5IEewhzxPbLquQxztVZrCnXg==; bm_mi=EF241D72DBFED76BFA7B1E2DEE7B3CA1~YAAQRVbbF8SEmeWYAQAApmdMDxwPkwiV6IuIDOvN8Mff+bveIFtsahhsryP0mxUtY0laOmfOIAiQL+eGQwTP1LRRNqAPY2zLgHMv2BNbRzOYfHy6zni0M2V6oELwdjzDBcsje+XTqLWAPVyIDx5HkE7sf4kZPHxWhYvPFWBIgMVfaNesN3HJHwUTL1V980h5pEUwM0LajztvIgFACtqYLl2vVUoMjWhXbbzvbhA9qnVOGBjt4ckeqcPHYaI3oJKAqVnNn5aORMXvZl2xFEb/xuYqVBQQyR3DoC2VZyopgvrua4rz+JxhsoH+nXil0jxJV2/+EeGSqBo4+77rxK1S983SM7oVxA==~1; bm_sv=9E97D21B6D6F3A49BFEF6E0B9C4AC99F~YAAQRVbbF4ylmeWYAQAAr3BMDxyMrOvmD2N44N1LKkF2aZlOOzTlfQwLsHPF6PiD3Kd8NYhn0Dp9Wat6JquqQEZCjcit1WWf18aI6U+7KpKHPRMuwBUUUuxyEnFI2Zdhh+m9Ba+56uiKFXN3L21a1vPtTOeOyvn5A5JJLqKkTtkAWowO21DU7O1VKN0PKOWkAfok0GDb2Sbftyku4yZ1asDN+x7mCp8cnnNZ69WqRNBkh/eA0LmtKRmavL7phLdiHZsjpx3n82c=~1; utag_main__se=3^%^3Bexp-session; utag_main__ss=0^%^3Bexp-session; utag_main__st=1756900091727^%^3Bexp-session; utag_main_ses_id=1756898275979^%^3Bexp-session; utag_main__pn=2^%^3Bexp-session; utag_main_dc_event=1^%^3Bexp-session"
        }
        Wpayload = {
            "Filters": [],
            "IsSpecial": False,
            "Location": "/shop/search/products?searchTerm=energy%20drinks",
            "PageNumber": 1,
            "PageSize": 36,
            "SearchTerm": "energy drinks",
            "SortType": "TraderRelevance",
            "ExcludeSearchTypes": ["UntraceableVendors"]
        }

        # --- get data ---
        resp = None  # FIX: ensure resp exists even if request fails
        try:
            resp = requests.post(Wlink, headers=WHeader, json=Wpayload, timeout=20)
            print(f"HTTP {resp.status_code}")
            if resp.status_code != 200:
                print(f"Body (truncated): {resp.text[:500]}")
                resp = None  # FIX: mark as failed so we don't use it below
        except RequestException as e:
            print(f"❌ Request failed: {e}")
            resp = None  # FIX: keep resp defined

        if not resp:
            print("⚠️ No response, skipping processing.")
            raise SystemExit(1)  # FIX: stop here so we don’t hit resp.json() below

        # FIX: only call .json() once, after the guard above
        data = resp.json()

        out_path = os.path.abspath("woolies_products2.json")
        try:
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print(f"✅ Saved results to {out_path}")
        except OSError as e:
            print(f"❌ Failed to write file: {e}")

        # Your JSON shape is nested: data["Products"] -> list of groups, each with ["Products"] list
        groups = data.get("Products", [])
        products = [p for g in groups for p in g.get("Products", [])]

        discounted = []

        for p in products:
            # FIX: guard DisplayName so .lower() never crashes
            name = (p.get("DisplayName") or "").strip()
            price = p.get("Price")
            was = p.get("WasPrice")
            savingsamount = p.get("SavingsAmount")

            if "x 4 pack" in name.lower() and price is not None and was is not None and price < was:
                # FIX: store structured data (tuple), not a formatted string
                discounted.append((name, price, was, savingsamount))

        embed = Embed(
            title="Woolies 4-Pack Specials",
            description="4-Pack energy drinks that are on sale",
            color=0xd20f39
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
        hook.send(embed=embed)

    wooliesCheck()




if __name__ == "__main__":
    main()



