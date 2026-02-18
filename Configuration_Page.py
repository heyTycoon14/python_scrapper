# Configuration_Page.py - Unified Configuration File

from datetime import datetime, timedelta
import re

def date_range_to_list(range_str=None):
    """
    Converts date ranges into a list of YYYY-MM-DD strings.

    Supported formats:
    - 'YYYY-MM-DD - YYYY-MM-DD'
    - 'YYYY-MM-DD-YYYY-MM-DD'
    - 'YYYY-MM-DD,YYYY-MM-DD'

    Returns [] if input is None or empty.
    """
    if not range_str or not str(range_str).strip():
        return []

    range_str = range_str.strip()

    # Try splitting by known separators
    if "," in range_str:
        start_str, end_str = [s.strip() for s in range_str.split(",", 1)]
    elif " - " in range_str:
        start_str, end_str = [s.strip() for s in range_str.split(" - ", 1)]
    else:
        # Fallback: YYYY-MM-DD-YYYY-MM-DD
        match = re.fullmatch(
            r"(\d{4}-\d{2}-\d{2})-(\d{4}-\d{2}-\d{2})",
            range_str
        )
        if not match:
            raise ValueError(f"Invalid date range format: {range_str}")
        start_str, end_str = match.groups()

    start_date = datetime.strptime(start_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_str, "%Y-%m-%d")

    if end_date < start_date:
        raise ValueError("End date cannot be before start date")

    days = (end_date - start_date).days + 1
    return [
        (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
        for i in range(days)
    ]

# Percentage Variables ######################
scraper_dir = "/home/dzm/public_html/coataa.com/scrapers"
TAX_RATES = 0.065

# ------------------------------------------------------------
# Constants
# ------------------------------------------------------------

# False if we want percentage discount 
SeaWorld_Flat_Discount = True
BuschGardens_Flat_Discount = True
Disney_Flat_Discount = True
Universal_Flat_Discount = True

UNIVERSAL_DAY_LIMIT = 200
SEAWORLD_DAY_LIMIT = 200
BUSCHGARDENS_DAY_LIMIT = 200
DISNEY_DAY_LIMIT = 200

# =============================================================================
# EXCLUDED DAYS
# =============================================================================

# Two Uses

# First - Normal range: date_range_to_list("2026-03-13 - 2026-03-21") 
# Second - Multiple block range: ( date_range_to_list("2026-03-13 - 2026-03-21") + date_range_to_list("2026-03-25 - 2026-03-30") )
# 
# Accepted Formats - 
# 
# date_range_to_list("2026-03-13 - 2026-03-21")
# date_range_to_list("2026-03-13-2026-03-21")
# date_range_to_list("2026-03-13,2026-03-21")

EXCLUDED_DAYS_SEAWORLD_TICKETS = date_range_to_list()
EXCLUDED_DAYS_BUSCH_GARDENS_TICKETS = date_range_to_list()

# THERE ARE NO BLOCKOUT DATES FOR QUICK QUEUE, ALL DATES WILL BE SCRAPED
EXCLUDED_DAYS_SEAWORLD_QUEUES = date_range_to_list()
EXCLUDED_DAYS_BUSCH_GARDENS_QUEUES = date_range_to_list()

EXCLUDED_DAYS_DISNEY_MAGIC_KINGDOM = date_range_to_list("2026-03-13 - 2026-03-21")
EXCLUDED_DAYS_DISNEY_ANIMAL_KINGDOM = date_range_to_list()
EXCLUDED_DAYS_DISNEY_EPCOT = date_range_to_list()
EXCLUDED_DAYS_DISNEY_HOLLYWOOD_STUDIOS = date_range_to_list()
EXCLUDED_DAYS_DISNEY_1DAY_HOPPER = date_range_to_list()

# FOR THIS ONE WE SCRAPE THE PRICE BUT FOR THESE DATES THE DISCOUNT PRICE IS DIFFERENT
EXCLUDED_DAYS_DISNEY_2DAY_TICKET = date_range_to_list()
EXCLUDED_DAYS_DISNEY_3DAY_TICKET = ( date_range_to_list("2026-01-12 - 2026-01-16") + date_range_to_list("2026-01-20 - 2026-02-13") + date_range_to_list("2026-02-17 - 2026-03-13") + date_range_to_list("2026-03-22 - 2026-03-28")+ date_range_to_list("2026-04-10 - 2026-05-14"))
EXCLUDED_DAYS_DISNEY_4DAY_TICKET = ( date_range_to_list("2026-01-12 - 2026-01-16") + date_range_to_list("2026-01-20 - 2026-02-13") + date_range_to_list("2026-02-17 - 2026-03-13") + date_range_to_list("2026-03-22 - 2026-03-28")+ date_range_to_list("2026-04-10 - 2026-05-13"))

EXCLUDED_DAYS_UNIVERSAL_1DAY_PTP = date_range_to_list()
EXCLUDED_DAYS_UNIVERSAL_1DAY_BASE = date_range_to_list()

EXCLUDED_DAYS_UNIVERSAL_2DAY_PTP = date_range_to_list()
EXCLUDED_DAYS_UNIVERSAL_2DAY_BASE = date_range_to_list()

EXCLUDED_DAYS_UNIVERSAL_1DAY_EPIC = date_range_to_list()
EXCLUDED_DAYS_UNIVERSAL_ALL_GROUP_RATE_TICKETS = date_range_to_list("2026-03-30 - 2026-04-05")

# Discount Variables
# For SeaWorld/Busch Gardens/Express To change from % to $ Discounts
# For %: set with a value < 1 (ex: 30%=0.3 or 45%=0.45)
# For $: set with a value > 1 (ex: $40 off=40)

# =============================================================================
# SEAWORLD DISCOUNTS
# =============================================================================
SeaWorld_Orlando_DISCOUNT = 29
SeaWorld_Orlando_QQ_DISCOUNT = 29

# =============================================================================
# BUSCH GARDENS DISCOUNTS
# =============================================================================
Busch_Gardens_DISCOUNT = 41
Busch_Gardens_QQ_DISCOUNT = 31

# =============================================================================
# DISNEY DISCOUNTS
# =============================================================================

# Disney Discount Variables
DISNEY_1DAY_DISCOUNT = 29
DISNEY_2DAY_DISCOUNT = 5
DISNEY_3DAY_DISCOUNT = 50 #64
DISNEY_4DAY_DISCOUNT = 50 #71

#THIS IS SEPARATE DISCOUNT THAT APPLIES TO THE BLOCKOUT DATES
DISNEY_BLOCKOUT_DATES_DISCOUNT_FOR_2DAY_TICKETS = 0
DISNEY_BLOCKOUT_DATES_DISCOUNT_FOR_3DAY_TICKETS = 150 #174
DISNEY_BLOCKOUT_DATES_DISCOUNT_FOR_4DAY_TICKETS = 150 #154

# =============================================================================
# UNIVERSAL DISCOUNTS
# =============================================================================
Universal_1day_base_DISCOUNT = 19
Universal_1day_ptp_DISCOUNT = 34
Universal_2day_base_DISCOUNT = 49
Universal_2day_ptp_DISCOUNT = 71

Universal_1day_base_GROUP_DISCOUNT = 21
Universal_1day_ptp_GROUP_DISCOUNT = 42
Universal_2day_base_GROUP_DISCOUNT = 51
Universal_2day_ptp_GROUP_DISCOUNT = 69

# ---- EPIC ----
Universal_1day_EPIC_DISCOUNT = 0
Universal_2day_base_with_epic_GROUP_DISCOUNT = 29
Universal_2day_ptp_with_epic_GROUP_DISCOUNT = 49


# =============================================================================
# LOWEST PRICE VARIABLES
# =============================================================================
SeaWorld_Orlando_LOWEST_PRICE = 49
SeaWorld_Orlando_QQ_LOWEST_PRICE = 19

Busch_Gardens_LOWEST_PRICE = 49
Busch_Gardens_QQ_LOWEST_PRICE = 19

# ---- UNIVERSAL NON-GROUP ----
Universal_1day_base_LOWEST_PRICE = 136
Universal_1day_ptp_LOWEST_PRICE = 179
Universal_1day_EPIC_LOWEST_PRICE = 171
Universal_2day_base_LOWEST_PRICE = 249
Universal_2day_ptp_LOWEST_PRICE = 281

# ---- UNIVERSAL GROUP ----
Universal_1day_base_GROUP_LOWEST_PRICE = 121 #Cost 101 +tax
Universal_1day_ptp_GROUP_LOWEST_PRICE = 168 #Cost 128 +tax 
Universal_2day_base_GROUP_LOWEST_PRICE = 236 #Cost 156 +tax
Universal_2day_ptp_GROUP_LOWEST_PRICE = 261 #Cost 180 +tax
Universal_2day_base_w_EPIC_GROUP_LOWEST_PRICE = 281 #Cost 240 +tax
Universal_2day_ptp_w_EPIC_GROUP_LOWEST_PRICE = 319 #Cost 260 +tax


# --- Disney ---
DISNEY_1DAY_MAGIC_KINGDOM_MIN_PRICE = 159    
DISNEY_1DAY_EPCOT_MIN_PRICE = 144            
DISNEY_1DAY_HOLLYWOOD_STUDIOS_MIN_PRICE = 157  
DISNEY_1DAY_ANIMAL_KINGDOM_MIN_PRICE = 136    
DISNEY_1DAY_PARK_HOPPER_MIN_PRICE = 201       
DISNEY_2DAY_1PARK_PER_DAY_MIN_PRICE = 251     
DISNEY_3DAY_1PARK_PER_DAY_MIN_PRICE = 335 #change this after discover disney promo ends  
DISNEY_4DAY_1PARK_PER_DAY_MIN_PRICE = 355 #change this after discover disney promo ends
#DISNEY_3DAY_FL_RESIDENT_MIN_PRICE = 211      
#DISNEY_4DAY_FL_RESIDENT_MIN_PRICE = 256    


# =============================================================================
# TICKET ID ASSOCIATIONS
# =============================================================================

# ---- SEAWORLD ----
SeaWorld_Orlando_ticketIDs = [37]
SeaWorld_Orlando_Queue_ticketIDs = [69]

# ---- BUSCH GARDENS ----
Busch_Gardens_ticketIDs = [48]
Busch_Gardens_Queue_ticketIDs = [80]

# ---- UNIVERSAL NON-GROUP ----
Universal_1day_base_ticketIDs = [2, 44]
Universal_1day_EPIC_ticketIDs = [144]
Universal_1day_ptp_ticketIDs = [52]

Universal_2day_base_ticketIDs = [112]
Universal_2day_ptp_ticketIDs = [114]

# ---- UNIVERSAL GROUP ----
Universal_1day_base_GROUP_ticketIDs = [125]
Universal_1day_ptp_GROUP_ticketIDs = [126]
Universal_2day_base_GROUP_ticketIDs = [127]
Universal_2day_ptp_GROUP_ticketIDs = [128]
 
 # ---- EPIC GROUP ----
Universal_2day_base_w_EPIC_GROUP_ticketIDs = [143]
Universal_2day_ptp_w_EPIC_GROUP_ticketIDs = [142]

# Disney Ticket ID Associations (Using existing ticket_prices table)
DISNEY_1DAY_MAGIC_KINGDOM_TICKET_ID = 137   
DISNEY_1DAY_EPCOT_TICKET_ID = 136            
DISNEY_1DAY_HOLLYWOOD_STUDIOS_TICKET_ID = 139 
DISNEY_1DAY_ANIMAL_KINGDOM_TICKET_ID = 138   
DISNEY_1DAY_PARK_HOPPER_TICKET_ID = 140      
DISNEY_2DAY_1PARK_PER_DAY_TICKET_ID = 141  
DISNEY_3DAY_1PARK_PER_DAY_TICKET_ID = 129     
DISNEY_4DAY_1PARK_PER_DAY_TICKET_ID = 130     
DISNEY_3DAY_FL_RESIDENT_TICKET_ID = 90     
DISNEY_4DAY_FL_RESIDENT_TICKET_ID = 91      


# =============================================================================

# Disney Database Tables 
DISNEY_JSON_TABLE = 'disney_json_storage' 
DISNEY_TICKETS_TABLE = 'ticket_prices'     

# =============================================================================
# DATABASE CONFIGURATION
# =============================================================================

################################## FOR SERVER #####################################
import configparser

config = configparser.ConfigParser()
config.read('/home/dzm/public_html/coataa.com/app_controller/Config/config.ini')
db_host = config['database']['host']
db_user = config['database']['user']
db_password = config['database']['password']
db_database = config['database']['database']
####################################################################################

################################## FOR LOCAL #####################################
# db_host = 'localhost'
# db_user = 'root'
# db_password = ''
# db_database = 'dzm_coataa'  # Your database name
####################################################################################