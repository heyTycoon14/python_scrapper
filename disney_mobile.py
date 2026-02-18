
import Configuration_Page as config
from pricing import apply_pricing
from datetime import datetime, timedelta
import csv
import time
import requests
import json
import uuid

# ------------------------------------------------------------
# Constants
# ------------------------------------------------------------
OUTPUT_CSV = "disney_price_review.csv"

# ------------------------------------------------------------
# 1-Day Park Mapping (PER PARK PRICING)
# ------------------------------------------------------------

ONE_DAY_PARK_SUFFIX_MAP = {
    "_mk": config.DISNEY_1DAY_MAGIC_KINGDOM_TICKET_ID,
    "_ep": config.DISNEY_1DAY_EPCOT_TICKET_ID,
    "_hs": config.DISNEY_1DAY_HOLLYWOOD_STUDIOS_TICKET_ID,
    "_ak": config.DISNEY_1DAY_ANIMAL_KINGDOM_TICKET_ID,
}

# ------------------------------------------------------------
# Multi-Day Ticket Mapping (NO PARK SPLIT)
# ------------------------------------------------------------

MULTI_DAY_TICKETS = {
    2: config.DISNEY_2DAY_1PARK_PER_DAY_TICKET_ID,
    3: config.DISNEY_3DAY_1PARK_PER_DAY_TICKET_ID,
    4: config.DISNEY_4DAY_1PARK_PER_DAY_TICKET_ID,
}

# ------------------------------------------------------------
# Multi-Day Minimum Price Mapping (from config)
# ------------------------------------------------------------

MULTI_DAY_MIN_PRICE_MAP = {
    2: config.DISNEY_2DAY_1PARK_PER_DAY_MIN_PRICE,
    3: config.DISNEY_3DAY_1PARK_PER_DAY_MIN_PRICE,
    4: config.DISNEY_4DAY_1PARK_PER_DAY_MIN_PRICE,
}

# ------------------------------------------------------------
# Multi-Day Discount Mapping (from config)
# ------------------------------------------------------------

MULTI_DAY_DISCOUNT_MAP = {
    1: config.DISNEY_1DAY_DISCOUNT,
    2: config.DISNEY_2DAY_DISCOUNT,
    3: config.DISNEY_3DAY_DISCOUNT,
    4: config.DISNEY_4DAY_DISCOUNT,
}

# ------------------------------------------------------------
# Dates to Skip (from config)
# ------------------------------------------------------------

BLACKOUT_DATES = {
    "_mk": config.EXCLUDED_DAYS_DISNEY_MAGIC_KINGDOM,
    "_ep": config.EXCLUDED_DAYS_DISNEY_EPCOT,
    "_hs": config.EXCLUDED_DAYS_DISNEY_HOLLYWOOD_STUDIOS,
    "_ak": config.EXCLUDED_DAYS_DISNEY_ANIMAL_KINGDOM,
}

MULTI_DAY_BLACKOUT_DATES = {
    2: config.EXCLUDED_DAYS_DISNEY_2DAY_TICKET,
    3: config.EXCLUDED_DAYS_DISNEY_3DAY_TICKET,
    4: config.EXCLUDED_DAYS_DISNEY_4DAY_TICKET,
}

MULTI_DAY_BLACKOUT_DATES_DISCOUNT = {
    1: 0,
    2: config.DISNEY_BLOCKOUT_DATES_DISCOUNT_FOR_2DAY_TICKETS,
    3: config.DISNEY_BLOCKOUT_DATES_DISCOUNT_FOR_3DAY_TICKETS,
    4: config.DISNEY_BLOCKOUT_DATES_DISCOUNT_FOR_4DAY_TICKETS,
}

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------

def is_adult_one_park_price(price_id: str) -> bool:
    """
    Adult + 1 Park Per Day pricing only
    """
    return (
        "_A_" in price_id and
        "_0_0_" in price_id and
        "_P_" not in price_id and
        "_PHP_" not in price_id
    )


def is_adult_multi_day_1park(price_id: str, day: int) -> bool:
    """
    Adult + Multi-day + 1 Park Per Day
    """
    return (
        f"theme-park_{day}_" in price_id and
        "_A_" in price_id and
        "_0_0_" in price_id and
        "_P_" not in price_id and
        "_PHP_" not in price_id
    )

def is_adult_park_hopper(price_id: str, num_days: int) -> bool:
    """
    Adult Park Hopper tickets
    Example: theme-park_3_A_P_0_RF_AF_SOF_progenstr
    """
    return (
        f"theme-park_{num_days}_A_P_" in price_id
        and "_PHP_" not in price_id
    )

# ------------------------------------------------------------
# Disney API Helpers
# ------------------------------------------------------------

DISNEY_TOKENS_FILE = "disney_tokens.json"

PRICING_API = (
    "https://api.wdprapps.disney.com/"
    "lexicon-view-assembler-service/wdw/tickets/"
    "product-types/theme-parks/prices"
)

DISNEY_REFRESH_URL = (
    "https://registerdisney.go.com/"
    "jgc/v8/client/TPR-WDW-LBSDK.IOS-PROD/guest/refresh-auth"
)

def load_disney_token():
    with open(DISNEY_TOKENS_FILE, "r") as f:
        return json.load(f)
    
def save_disney_token(tokens):
    with open(DISNEY_TOKENS_FILE, "w") as f:
        json.dump(tokens, f, indent=2)

def token_expired(expire_time_ms):
    return int(time.time() * 1000) >= expire_time_ms

def refresh_disney_token(tokens):
    """
    Refresh Disney OneID access token using refresh-auth endpoint.
    Updates tokens dict and persists it.
    """

    headers = {
        "Content-Type": "application/json;charset=utf-8",
        "Accept": "*/*",
        "Authorization": f"Bearer {tokens['auth_token']}",
        "User-Agent": "OneID/4.12.3 (iOS)",
        "conversation-id": str(uuid.uuid4()),
        "correlation-id": str(uuid.uuid4()),
    }

    payload = {
        "refreshToken": tokens["refresh_token"]
    }

    r = requests.post(
        DISNEY_REFRESH_URL,
        headers=headers,
        json=payload,
        timeout=20,
    )

    r.raise_for_status()
    data = r.json()["data"]["token"]

    # Update tokens
    tokens["auth_token"] = data["access_token"]
    tokens["refresh_token"] = data["refresh_token"]
    tokens["expire_time"] = data["exp"]  # already in ms

    save_disney_token(tokens)

    return tokens

def get_valid_disney_auth_token():
    tokens = load_disney_token()

    if token_expired(tokens["expire_time"]):
        print("Disney token expired — refreshing")
        tokens = refresh_disney_token(tokens)

    return tokens["auth_token"]

def fetch_pricing(day: int, start_date: str, end_date: str, auth_token: str):
    params = {
        "discountGroup": "std-gst",
        "addOn": "",
        "startDate": start_date,
        "endDate": end_date,
        "numDays": day,
        "storeId": "wdw_mobile",
        "fpAvailability": "false",
    }

    headers = {
        "Authorization": f"Bearer {auth_token}",
        "x-app-id": "WDW-MDX-IOS-8.16.1",
        "Accept": "*/*",
        "Content-Type": "application/json",
        "User-Agent": "WDW/20251204.2 CFNetwork/3860.300.31 Darwin/25.2.0",
    }

    r = requests.get(PRICING_API, headers=headers, params=params, timeout=20)
    r.raise_for_status()
    return r.json()

# ------------------------------------------------------------
# Main Script
# ------------------------------------------------------------

def main():
    results = []

    auth_token = get_valid_disney_auth_token()

    today = datetime.utcnow().date()
    scrape_days = config.DISNEY_DAY_LIMIT

    start_date_str = today.strftime("%Y-%m-%d")
    end_date_str = (today + timedelta(days=scrape_days)).strftime("%Y-%m-%d")

    print(f"Scraping Disney prices from {start_date_str} → {end_date_str}")

    for day in range(1, 5):
        print(f"\nProcessing {day}-day ticket")

        pricing_data = fetch_pricing(
            day=day,
            start_date=start_date_str,
            end_date=end_date_str,
            auth_token=auth_token,
        )

        for calendar in pricing_data["pricingCalendar"]:
            for date_entry in calendar["dates"]:
                start_date = date_entry["date"]

                for price in date_entry["pricing"]:
                    if price["ageGroup"] != "adult":
                        continue

                    price_id = price["id"]
                    scraped_price = float(price["subtotal"])

                    # ------------------------------------------------
                    # 1-DAY PER-PARK
                    # ------------------------------------------------
                    if day == 1 and is_adult_one_park_price(price_id):
                        for suffix, ticket_id in ONE_DAY_PARK_SUFFIX_MAP.items():
                            if price_id.endswith(suffix):
                                # print("SUFFIX: ", suffix)

                                blackout_dates = BLACKOUT_DATES[suffix]

                                final_price = apply_pricing(
                                    scraped_price,
                                    MULTI_DAY_DISCOUNT_MAP[1],
                                    config.DISNEY_1DAY_MAGIC_KINGDOM_MIN_PRICE,
                                    flat_discount=config.Disney_Flat_Discount,
                                )

                                savings = 0 

                                if float(scraped_price) > float(final_price):
                                    savings = float(scraped_price) - float(final_price)

                                if start_date not in blackout_dates:
                                    results.append({
                                        "ticket_id": ticket_id,
                                        "date": start_date,
                                        "park_price": round(scraped_price),
                                        "our_price": round(final_price),
                                        "savings": round(savings),
                                    })
                                break

                    # ------------------------------------------------
                    # PARK HOPPER
                    # ------------------------------------------------
                    elif (
                        day == 1
                        and is_adult_park_hopper(price_id, day)
                    ):
                        hopper_blackout_dates = config.EXCLUDED_DAYS_DISNEY_1DAY_HOPPER

                        final_price = apply_pricing(
                            scraped_price,
                            MULTI_DAY_DISCOUNT_MAP[1],
                            config.DISNEY_1DAY_PARK_HOPPER_MIN_PRICE,
                            flat_discount=config.Disney_Flat_Discount,
                        )

                        savings = 0 

                        if float(scraped_price) > float(final_price):
                            savings = float(scraped_price) - float(final_price)

                        if start_date not in hopper_blackout_dates:
                            results.append({
                                "ticket_id": config.DISNEY_1DAY_PARK_HOPPER_TICKET_ID,
                                "date": start_date,
                                "park_price": round(scraped_price),
                                "our_price": round(final_price),
                                "savings": round(savings),
                            })

                    # ------------------------------------------------
                    # MULTI-DAY 1 PARK PER DAY
                    # ------------------------------------------------
                    elif day in MULTI_DAY_TICKETS and is_adult_multi_day_1park(price_id, day):

                        blackout_dates = MULTI_DAY_BLACKOUT_DATES.get(day, [])

                        if start_date in blackout_dates:
                            ticket_discount = MULTI_DAY_BLACKOUT_DATES_DISCOUNT[day]
                        else:
                            ticket_discount = MULTI_DAY_DISCOUNT_MAP[day]

                        final_price = apply_pricing(
                            scraped_price,
                            ticket_discount,
                            MULTI_DAY_MIN_PRICE_MAP[day],
                            flat_discount=config.Disney_Flat_Discount,
                        )

                        savings = 0 

                        if float(scraped_price) > float(final_price):
                            savings = float(scraped_price) - float(final_price)

                        results.append({
                            "ticket_id": MULTI_DAY_TICKETS[day],
                            "date": start_date,
                            "park_price": round(scraped_price),
                            "our_price": round(final_price),
                            "savings": round(savings),
                        })

        time.sleep(1)

    # --------------------------------------------------------
    # Write CSV
    # --------------------------------------------------------

    with open(OUTPUT_CSV, "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["ticket_id", "date", "park_price", "our_price", "savings"],
        )
        writer.writeheader()
        writer.writerows(results)

    # print("Done. File ready for client review.")


def disney_scraper():
    main()

# main()