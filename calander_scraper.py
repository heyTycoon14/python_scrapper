import requests
import Configuration_Page as config
from pricing import apply_pricing
from datetime import date
import csv

def scrape_sitecore_calendar(
    landing_url,
    api_url,
    site_name,
    selling_group_id,
    item_id,
    ticket_name_match,
    ticket_ids,
    discount,
    lowest_price,
    csv_name,
    scrap_days,
    flat_discount,
    blackout_dates
):
    print(f"Establishing session for {site_name}...")

    HEADERS = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Referer": landing_url,
        "X-Requested-With": "XMLHttpRequest",
    }

    session = requests.Session()
    session.headers.update(HEADERS)

    session.get(landing_url, timeout=30).raise_for_status()

    params = {
        "type": "Reservation",
        "sellingGroupSitecoreId": selling_group_id,
        "sc_site": site_name,
        "sc_itemid": item_id,
    }

    r = session.get(api_url, params=params, timeout=30)
    r.raise_for_status()

    data = r.json()

    if not data.get("Dates"):
        raise RuntimeError("No Calendar Data returned")

    results = []
    today = date.today()
    days_collected = 0

    for entry in data["Dates"]:
        if days_collected >= scrap_days:
            break

        visit_date = date.fromisoformat(entry["InventoryDate"][:10])
        if visit_date < today:
            continue

        ticket = next(
            (i for i in entry["OrderItems"] if i.get("Name") == ticket_name_match),
            None,
        )
        if not ticket:
            continue

        park_price = float(ticket["CurrentPrice"])
        savings = 0

        our_price = apply_pricing(
            scraped_price=park_price,
            discount=discount,
            minimum_price=lowest_price,
            flat_discount=flat_discount
        )

        if park_price > float(our_price):
            savings = park_price - float(our_price)

        for ticket_id in ticket_ids:

            start_date = visit_date.isoformat()

            if start_date not in blackout_dates:
                results.append({
                    "ticket_id": ticket_id,
                    "date": start_date,
                    "park_price": round(park_price),
                    "our_price": our_price,
                    "savings": round(savings),
                })

        days_collected += 1

    with open(csv_name, "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["ticket_id", "date", "park_price", "our_price", "savings"],
        )
        writer.writeheader()
        writer.writerows(results)

    print(f"{site_name} pricing saved to {csv_name}")
