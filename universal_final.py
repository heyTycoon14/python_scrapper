import time
import json
import csv
import requests
from pathlib import Path
import base64

# from pricing import apply_pricing
import Configuration_Page as config
from datetime import datetime, timedelta

# =========================
# FILE OUTPUT
# =========================

OUTPUT_CSV = "universal_price_review.csv"

# =========================
# TOKEN CONFIG
# =========================

TOKEN_FILE = Path(__file__).resolve().with_name("tokens.json")

TOKEN_URL = "https://api.universalparks.com/oidc/connect/token"
PRICING_URL = "https://api.universalparks.com/shop/wcs/resources/store/10101/event/priceAndInventory/v2"

UNIVERSAL_USERNAME = "admin@universaladmin.com"
UNIVERSAL_PASSWORD = "password123"
CLIENT_ID = "3d8f26d8-d302-4bfe-8670-8816e7713b90"
CLIENT_SECRET = "AeweCuThiedaowecheighiereizeochiungaesielaechoifie"

INITIAL_ACCESS_TOKEN = "PASTE_ACCESS_TOKEN"
INITIAL_REFRESH_TOKEN = "PASTE_REFRESH_TOKEN"
INITIAL_EXPIRES_AT = 1767374673

# =========================
# TICKET DEFINITIONS (10)
# =========================

TICKETS = [
    # ---------- NON-FL ----------
    {
        "name": "Universal 1D Base",
        "part": "TPA-01D_BSE_2P_AD_GA_ABP",
        "ticket_ids": config.Universal_1day_base_ticketIDs,
        "discount": config.Universal_1day_base_DISCOUNT,
        "min_price": config.Universal_1day_base_LOWEST_PRICE,
        "excluded_dates": config.EXCLUDED_DAYS_UNIVERSAL_1DAY_BASE,
        "group_ticket_ids": config.Universal_1day_base_GROUP_ticketIDs,
        "group_discount": config.Universal_1day_base_GROUP_DISCOUNT,
        "group_min_price": config.Universal_1day_base_GROUP_LOWEST_PRICE,
        "group_excluded_dates": config.EXCLUDED_DAYS_UNIVERSAL_ALL_GROUP_RATE_TICKETS,
        "group_ticket": True,
    },
    {
        "name": "Universal 1D PTP",
        "part": "TPA-01D_PTP_2P_AD_GA_ABP",
        "ticket_ids": config.Universal_1day_ptp_ticketIDs,
        "discount": config.Universal_1day_ptp_DISCOUNT,
        "min_price": config.Universal_1day_ptp_LOWEST_PRICE,
        "excluded_dates": config.EXCLUDED_DAYS_UNIVERSAL_1DAY_PTP,
        "group_ticket_ids": config.Universal_1day_ptp_GROUP_ticketIDs,
        "group_discount": config.Universal_1day_ptp_GROUP_DISCOUNT,
        "group_min_price": config.Universal_1day_ptp_GROUP_LOWEST_PRICE,
        "group_excluded_dates": config.EXCLUDED_DAYS_UNIVERSAL_ALL_GROUP_RATE_TICKETS,
        "group_ticket": True,
    },
    {
        "name": "Universal 1D Epic Universe",
        "part": "TPA-01D_BSE_EPIC_AD_ABP",
        "ticket_ids": config.Universal_1day_EPIC_ticketIDs,
        "discount": config.Universal_1day_EPIC_DISCOUNT,
        "min_price": config.Universal_1day_EPIC_LOWEST_PRICE,
        "excluded_dates": config.EXCLUDED_DAYS_UNIVERSAL_1DAY_EPIC,
        "group_ticket": False,
    },
    {
        "name": "Universal 2D 2Park Base",
        "part": "TPA-02D_BSE_2P_AD_GA_ABP",
        "ticket_ids": config.Universal_2day_base_ticketIDs,
        "discount": config.Universal_2day_base_DISCOUNT,
        "min_price": config.Universal_2day_base_LOWEST_PRICE,
        "excluded_dates": config.EXCLUDED_DAYS_UNIVERSAL_2DAY_BASE,
        "group_ticket_ids": config.Universal_2day_base_GROUP_ticketIDs,
        "group_discount": config.Universal_2day_base_GROUP_DISCOUNT,
        "group_min_price": config.Universal_2day_base_GROUP_LOWEST_PRICE,
        "group_excluded_dates": config.EXCLUDED_DAYS_UNIVERSAL_ALL_GROUP_RATE_TICKETS,
        "group_ticket": True,
    },
    {
        "name": "Universal 2D 2Park PTP",
        "part": "TPA-02D_PTP_2P_AD_GA_ABP",
        "ticket_ids": config.Universal_2day_ptp_ticketIDs,
        "discount": config.Universal_2day_ptp_DISCOUNT,
        "min_price": config.Universal_2day_ptp_LOWEST_PRICE,
        "excluded_dates": config.EXCLUDED_DAYS_UNIVERSAL_2DAY_PTP,
        "group_ticket_ids": config.Universal_2day_ptp_GROUP_ticketIDs,
        "group_discount": config.Universal_2day_ptp_GROUP_DISCOUNT,
        "group_min_price": config.Universal_2day_ptp_GROUP_LOWEST_PRICE,
        "group_excluded_dates": config.EXCLUDED_DAYS_UNIVERSAL_ALL_GROUP_RATE_TICKETS,
        "group_ticket": True,
    },
    {
        "name": "Universal 2D PTP With Epic",
        "part": "TPA-01D_PTP_2P_1DEPIC_AD_ABP",
        "ticket_ids": config.Universal_2day_base_w_EPIC_GROUP_ticketIDs,
        "discount": config.Universal_2day_ptp_with_epic_GROUP_DISCOUNT,
        "min_price": config.Universal_2day_ptp_w_EPIC_GROUP_LOWEST_PRICE,
        "excluded_dates": config.EXCLUDED_DAYS_UNIVERSAL_ALL_GROUP_RATE_TICKETS,
        "group_ticket": False,
    },
    {
        "name": "Universal 2D Base With Epic",
        "part": "TPA-01D_BSE_2P_1DEPIC_AD_ABP",
        "ticket_ids": config.Universal_2day_ptp_w_EPIC_GROUP_ticketIDs,
        "discount": config.Universal_2day_base_with_epic_GROUP_DISCOUNT,
        "min_price": config.Universal_2day_base_w_EPIC_GROUP_LOWEST_PRICE,
        "excluded_dates": config.EXCLUDED_DAYS_UNIVERSAL_ALL_GROUP_RATE_TICKETS,
        "group_ticket": False,
    },
    # ---------- FLORIDA ----------
    # {
    #     "name": "FL 1D 1P Islands/Studios",
    #     "part": "TPA-01D_BSE_2P_AD_FL_ABP",
    #     "ticket_ids": config.Universal_1day1park_group_ticketIDs,
    #     "discount": config.Universal_Group_1d1p_DISCOUNT,
    #     "min_price": config.Universal_fl_1day1park_islands_or_studio_LOWEST_PRICE,
    # },
    # {
    #     "name": "FL 1D 2P Islands/Studios",
    #     "part": "TPA-01D_PTP_2P_AD_FL_ABP",
    #     "ticket_ids": config.Universal_1day2park_group_ticketIDs,
    #     "discount": config.Universal_Group_1d2p_DISCOUNT,
    #     "min_price": config.Universal_fl_1day2park_islands_or_studio_LOWEST_PRICE,
    # },
    # {
    #     "name": "FL 1D 1P Epic",
    #     "part": "TPA-01D_BSE_EPIC_AD_FL_ABP",
    #     "ticket_ids": config.Universal_fl_1day1park_epic_ticketIDs,
    #     "discount": config.Universal_Group_1d1p_DISCOUNT,
    #     "min_price": config.Universal_fl_1day1park_epic_LOWEST_PRICE,
    # },
    # {
    #     "name": "FL 2D 2P 1 Park/Day",
    #     "part": "TPA-02D_PTP_2P_AD_FL_ABP",
    #     "ticket_ids": config.Universal_fl_2day2park_1park_per_day_ticketIDs,
    #     "discount": config.Universal_Group_2d_DISCOUNT,
    #     "min_price": config.Universal_fl_2day2park_1park_per_day_LOWEST_PRICE,
    # },
    # {
    #     "name": "FL 2D 2P Multi Park",
    #     "part": "TPA-01D_PTP_2P_1DEPIC_AD_FL_ABP",
    #     "ticket_ids": config.Universal_fl_2day2park_multipark_ticketIDs,
    #     "discount": config.Universal_Group_2d_DISCOUNT,
    #     "min_price": config.Universal_fl_2day2park_multipark_LOWEST_PRICE,
    # },
]

# =========================
# TOKEN MANAGEMENT
# =========================


def get_expires_at_from_token(access_token, fallback_expires_in=None):
    """
    Returns expires_at (unix timestamp) from JWT exp.
    Falls back to now + expires_in if needed.
    """
    try:
        payload_b64 = access_token.split(".")[1]
        payload_b64 += "=" * (-len(payload_b64) % 4)  # padding
        payload = json.loads(base64.urlsafe_b64decode(payload_b64))
        return int(payload["exp"])
    except Exception:
        if fallback_expires_in is None:
            raise RuntimeError("Cannot determine expires_at from token")
        return int(time.time()) + int(fallback_expires_in)


def save_tokens(tokens):
    # Atomic write to avoid partial/corrupt token files
    tmp_path = TOKEN_FILE.with_suffix(TOKEN_FILE.suffix + ".tmp")
    tmp_path.write_text(json.dumps(tokens, indent=2))
    tmp_path.replace(TOKEN_FILE)


def load_tokens():
    if TOKEN_FILE.exists():
        return json.loads(TOKEN_FILE.read_text())

    tokens = {
        "access_token": INITIAL_ACCESS_TOKEN,
        "refresh_token": INITIAL_REFRESH_TOKEN,
        "expires_at": INITIAL_EXPIRES_AT,
    }
    save_tokens(tokens)
    return tokens


class RefreshTokenInvalid(Exception):
    pass


def login_password_grant() -> dict:
    """
    Gets a brand new token set using the password grant.
    Requires UNIVERSAL_USERNAME / UNIVERSAL_PASSWORD env vars.
    """
    if not UNIVERSAL_USERNAME or not UNIVERSAL_PASSWORD:
        raise RuntimeError(
            "Missing UNIVERSAL_USERNAME / UNIVERSAL_PASSWORD env vars for password login."
        )

    print("Bootstrapping Universal tokens via password grant...")

    r = requests.post(
        TOKEN_URL,
        data={
            "grant_type": "password",
            "username": UNIVERSAL_USERNAME,
            "password": UNIVERSAL_PASSWORD,
            # Use the same scope that worked in Postman:
            "scope": "openid default offline_access",
        },
        auth=(CLIENT_ID, CLIENT_SECRET),
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "User-Agent": "Universal FL/3 CFNetwork/3860.300.31 Darwin/25.2.0",
        },
        timeout=(10, 60),
    )

    if r.status_code != 200:
        print("Password grant login failed:", r.status_code)
        print("Response:", (r.text or "")[:800])
        r.raise_for_status()

    data = r.json()

    tokens = {
        "access_token": data["access_token"],
        "refresh_token": data.get("refresh_token"),
        "expires_at": int(time.time()) + int(data["expires_in"]),
    }

    if not tokens["refresh_token"]:
        raise RuntimeError("Password grant succeeded but no refresh_token returned.")

    save_tokens(tokens)
    return tokens


def refresh_access_token(refresh_token: str) -> dict:
    print("Refreshing Universal token...")

    r = requests.post(
        TOKEN_URL,
        data={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            # Keep it minimal; many providers reject extra fields here
            # If your server requires scope, use:
            # "scope": "openid default offline_access",
        },
        auth=(CLIENT_ID, CLIENT_SECRET),
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "User-Agent": "Universal FL/3 CFNetwork/3860.300.31 Darwin/25.2.0",
        },
        timeout=(10, 60),
    )

    if r.status_code != 200:
        body = (r.text or "")[:800]
        print("Universal refresh failed:", r.status_code)
        print("Response body:", body)

        if '"invalid_grant"' in body:
            raise RefreshTokenInvalid("Refresh token invalid_grant")

        r.raise_for_status()

    data = r.json()

    tokens = {
        "access_token": data["access_token"],
        "refresh_token": data.get("refresh_token", refresh_token),  # handle rotation
        "expires_at": int(time.time()) + int(data["expires_in"]),
    }

    save_tokens(tokens)
    return tokens


def get_tokens():
    tokens = load_tokens()
    if time.time() > tokens["expires_at"] - 60:
        try:
            tokens = refresh_access_token(tokens["refresh_token"])
        except RefreshTokenInvalid:
            # refresh token died -> do password login to get a brand-new refresh token
            tokens = login_password_grant()
    return tokens


# =========================
# API CALL
# =========================


def fetch_prices(part_number, start_date, end_date):
    tokens = get_tokens()

    headers = {
        "Authorization": f"Bearer {tokens['access_token']}",
        "x-ibm-client-id": CLIENT_ID,
        "x-uniwebservice-apikey": "webstore",
        "Content-Type": "application/json",
        "Origin": "https://www.universalorlando.com",
        "Referer": "https://www.universalorlando.com/",
        "User-Agent": "Mozilla/5.0",
    }

    payload = {
        "contractId": "4000000000000000003",
        "currency": "USD",
        "events": [
            {
                "partNumber": part_number,
                "startDate": f"{start_date} 00:00:01",
                "endDate": f"{end_date} 23:59:59",
                "quantity": 1,
            }
        ],
    }

    r = requests.post(PRICING_URL, headers=headers, json=payload, timeout=20)

    if r.status_code == 401:
        tokens = refresh_access_token(tokens["refresh_token"])
        headers["Authorization"] = f"Bearer {tokens['access_token']}"
        r = requests.post(PRICING_URL, headers=headers, json=payload)

    r.raise_for_status()
    return r.json()


# =========================
# NORMALIZER
# =========================


def parse_response(data, ticket_cfg):
    rows = []

    availability = data.get("eventAvailability", {})
    for _, days in availability.items():
        for date, info in days.items():
            pricing = info.get("pricing", [])
            if not pricing:
                continue

            base_price = float(pricing[0]["amount"])
            final_group_price = 0

            # final_price = apply_pricing(
            #     scraped_price=base_price,
            #     discount=ticket_cfg["discount"],
            #     minimum_price=ticket_cfg["min_price"],
            #     flat_discount=config.Universal_Flat_Discount,
            # )
            final_price = base_price  # Placeholder until pricing function is restored

            savings = 0
            group_savings = 0

            if float(base_price) > float(final_price):
                savings = float(base_price) - float(final_price)

            for ticket_id in ticket_cfg["ticket_ids"]:
                if date not in ticket_cfg["excluded_dates"]:
                    rows.append(
                        {
                            "ticket_id": ticket_id,
                            "date": date,
                            "park_price": round(base_price),
                            "our_price": round(final_price),
                            "savings": round(savings),
                        }
                    )

            if ticket_cfg["group_ticket"] == True:
                final_group_price = (
                    base_price  # Placeholder until pricing function is restored
                )
                # final_group_price = apply_pricing(
                #     scraped_price=base_price,
                #     discount=ticket_cfg["group_discount"],
                #     minimum_price=ticket_cfg["group_min_price"],
                #     flat_discount=config.Universal_Flat_Discount,
                # )

                if float(base_price) > float(final_group_price):
                    group_savings = float(base_price) - float(final_group_price)

                for group_ticket_id in ticket_cfg["group_ticket_ids"]:

                    if (
                        ticket_cfg["group_ticket"] == True
                        and date not in ticket_cfg["group_excluded_dates"]
                    ):
                        rows.append(
                            {
                                "ticket_id": group_ticket_id,
                                "date": date,
                                "park_price": round(base_price),
                                "our_price": round(final_group_price),
                                "savings": round(group_savings),
                            }
                        )

    return rows


# =========================
# MAIN
# =========================


def main():
    results = []

    for ticket in TICKETS:
        print(f"\nFetching {ticket['name']}")

        today = datetime.utcnow().date()
        scrape_days = config.UNIVERSAL_DAY_LIMIT

        start_date_str = today.strftime("%Y-%m-%d")
        end_date_str = (today + timedelta(days=scrape_days)).strftime("%Y-%m-%d")

        data = fetch_prices(
            ticket["part"],
            start_date=start_date_str,
            end_date=end_date_str,
        )

        results.extend(parse_response(data, ticket))
        time.sleep(5)

    print(f"\nTotal rows generated: {len(results)}")

    # Sort by start_date (ascending)
    results.sort(key=lambda r: datetime.strptime(r["date"], "%Y-%m-%d"))

    # -----------------------
    # WRITE CSV
    # -----------------------
    with open(OUTPUT_CSV, "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "ticket_id",
                "date",
                "park_price",
                "our_price",
                "savings",
            ],
        )
        writer.writeheader()
        writer.writerows(results)

    print(f"CSV written → {OUTPUT_CSV}")

    return results


def universal_scraper():
    main()


if __name__ == "__main__":
    universal_scraper()
# main()
