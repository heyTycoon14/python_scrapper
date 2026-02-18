import Configuration_Page as config
from calander_scraper import scrape_sitecore_calendar
from disney_mobile import disney_scraper
from universal_final import universal_scraper
import time

import csv
import pymysql

connection = pymysql.connect(
    host=config.db_host,
    user=config.db_user,
    password=config.db_password,
    database=config.db_database
)

def insert_csv_to_db(connection, csv_path):
    """
    Reads a CSV file and inserts rows into ticket_prices table
    """
    insert_sql = """
        INSERT INTO ticket_prices (
            ticket_id,
            product_id,
            date,
            park_price,
            florida_resident_price,
            price,
            group_price,
            savings
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)

        with connection.cursor() as cursor:
            for row in reader:

                if len(row) != 5:
                    continue

                ticket_id, date, park_price, our_price, savings = row

                cursor.execute(
                    insert_sql,
                    (
                        ticket_id,
                        None,          # product_id
                        date,
                        park_price,
                        None,          # florida_resident_price
                        our_price,     # price
                        None,          # group_price
                        savings
                    )
                )

        connection.commit()
        print(f"Imported: {csv_path}")

def import_seaworld_orlando(connection):
    insert_csv_to_db(connection, 'seaworld_orlando_queue.csv')
    insert_csv_to_db(connection, 'seaworld_orlando_tickets.csv')

def import_busch_gardens(connection):
    insert_csv_to_db(connection, 'busch_gardens_queue.csv')
    insert_csv_to_db(connection, 'busch_gardens_tickets.csv')

def import_universal(connection):
    insert_csv_to_db(connection, 'universal_price_review.csv')

def import_disney(connection):
    insert_csv_to_db(connection, 'disney_price_review.csv')

scrape_sitecore_calendar(
    landing_url="https://seaworld.com/orlando/tickets/",
    api_url="https://seaworld.com/api/sitecore/Cart/GetCalendarData",
    site_name="seaworld-orlando",
    selling_group_id="769d712e-e0fd-458d-8fda-c62b101e3462",
    item_id="f0903be1-2c3e-4d69-b03f-6d619c519133",
    ticket_name_match="Ticket Only (ages 3+)",
    ticket_ids=config.SeaWorld_Orlando_ticketIDs,
    discount=config.SeaWorld_Orlando_DISCOUNT,
    lowest_price=config.SeaWorld_Orlando_LOWEST_PRICE,
    csv_name="seaworld_orlando_tickets.csv",
    scrap_days=config.SEAWORLD_DAY_LIMIT,
    flat_discount=config.SeaWorld_Flat_Discount,
    blackout_dates=config.EXCLUDED_DAYS_SEAWORLD_TICKETS,
)
        
time.sleep(3)
        
scrape_sitecore_calendar(
    landing_url="https://seaworld.com/orlando/upgrades/rides-and-shows/",
    api_url="https://seaworld.com/api/sitecore/Cart/GetCalendarData",
    site_name="seaworld-orlando",
    selling_group_id="2f74812b-4014-4bab-b17d-28401add16cd",
    item_id="153dfdbc-c33f-4ca0-89bf-c9b8b3710912",
    ticket_name_match="Guest (ages 3+)",
    ticket_ids=config.SeaWorld_Orlando_Queue_ticketIDs,
    discount=config.SeaWorld_Orlando_QQ_DISCOUNT,
    lowest_price=config.SeaWorld_Orlando_QQ_LOWEST_PRICE,
    csv_name="seaworld_orlando_queue.csv",
    scrap_days=config.SEAWORLD_DAY_LIMIT,
    flat_discount=config.SeaWorld_Flat_Discount,
    blackout_dates=config.EXCLUDED_DAYS_SEAWORLD_QUEUES,
)

time.sleep(3)

import_seaworld_orlando(connection)

time.sleep(1)

scrape_sitecore_calendar(
    landing_url="https://buschgardens.com/tampa/",
    api_url="https://buschgardens.com/api/sitecore/Cart/GetCalendarData",
    site_name="busch-gardens-tampa-bay",
    selling_group_id="c544ebf8-7c1c-48db-8ab9-d8721ca8b59d",
    item_id="337639c9-bfe7-4c86-83b8-1695dbfb0005",
    ticket_name_match="Ticket Only",
    ticket_ids=config.Busch_Gardens_ticketIDs,
    discount=config.Busch_Gardens_DISCOUNT,
    lowest_price=config.Busch_Gardens_LOWEST_PRICE,
    csv_name="busch_gardens_tickets.csv",
    scrap_days=config.BUSCHGARDENS_DAY_LIMIT,
    flat_discount=config.BuschGardens_Flat_Discount,
    blackout_dates=config.EXCLUDED_DAYS_BUSCH_GARDENS_TICKETS,
)
        
time.sleep(3)
        
scrape_sitecore_calendar(
    landing_url="https://buschgardens.com/tampa/",
    api_url="https://buschgardens.com/api/sitecore/Cart/GetCalendarData",
    site_name="busch-gardens-tampa-bay",
    selling_group_id="1b1077cf-1e58-4a84-bcf8-ce4250ff32ea",
    item_id="0db6a970-1710-4746-a36f-ba9c048c908a",
    ticket_name_match="Guest",
    ticket_ids=config.Busch_Gardens_Queue_ticketIDs,
    discount=config.Busch_Gardens_QQ_DISCOUNT,
    lowest_price=config.Busch_Gardens_QQ_LOWEST_PRICE,
    csv_name="busch_gardens_queue.csv",
    scrap_days=config.BUSCHGARDENS_DAY_LIMIT,
    flat_discount=config.BuschGardens_Flat_Discount,
    blackout_dates=config.EXCLUDED_DAYS_BUSCH_GARDENS_QUEUES,
)

import_busch_gardens(connection)

time.sleep(3)

universal_scraper()

import_universal(connection)

time.sleep(3)

disney_scraper()

import_disney(connection)

connection.close()