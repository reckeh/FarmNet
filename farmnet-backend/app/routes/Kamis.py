import requests
from bs4 import BeautifulSoup
import psycopg2
from datetime import datetime, timedelta
import re
import logging
from time import sleep
import random

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('kamis_scraper.log'),
        logging.StreamHandler()
    ]
)

# Database configuration
DB_CONFIG = {
    'dbname': 'farmnet_db',
    'user': 'postgres',
    'password': '10098',
    'host': 'localhost',
    'port': '5432'
}

# Complete commodity mapping based on KAMIS dropdown
COMMODITY_MAP = {
    '1': 'Dry Maize',
    '2': 'Red Sorghum',
    '3': 'Wheat',
    '4': 'Rice',
    '10': 'Green Grams',
    '12': 'Ground Nuts',
    '29': 'Beans Red Haricot (Wairimu)',
    '30': 'Beans (Yellow-Green)',
    '50': 'Dolichos lablab (Njahi)',
    '51': 'Pearl Rush Millet',
    '54': 'Finger Millet',
    '56': 'White Sorghum',
    '57': 'Red Irish potato',
    '58': 'Cabbages',
    '59': 'Sweet potatoes',
    '60': 'Carrots',
    '61': 'Tomatoes',
    '64': 'Beans Rosecoco',
    '65': 'Beans (Mwitemania)',
    '66': 'Beans (Mwezi Moja)',
    '67': 'Beans (Canadian wonder)',
    '68': 'Tilapia',
    '70': 'Goat Milk (at collection point)',
    '72': 'Eggs',
    '73': 'Meat Beef',
    '74': 'Meat Mutton',
    '75': 'Meat Indiginous Chicken',
    '76': 'Meat Broiler',
    '77': 'Omena',
    '78': 'Cat Fish(Mkizi/Fume)',
    '79': 'Haplochromis',
    '80': 'Trout',
    '81': 'Common Carp',
    '82': 'Protopterus',
    '83': 'Black bass',
    '84': 'Labeo',
    '85': 'Mormyrus',
    '86': 'Eel',
    '87': 'African butter catfish',
    '89': 'Synodontis',
    '90': 'Alestes',
    '91': 'Barbus',
    '92': 'Other Fresh Water',
    '93': 'Snappers(Tazanda)',
    '94': 'Rabbitfish (Tafi/Tasi)',
    '95': 'Mixed Demersal',
    '96': 'Barracuda(Kasumba)',
    '97': 'Tuna',
    '98': 'Mackerel',
    '99': 'Kingfish (Nguru)',
    '100': 'Sharks',
    '101': 'Sardines',
    '102': 'Swordfishes',
    '103': 'Lobster(Kamba Mawe)',
    '104': 'Prawns',
    '107': 'Mud Crabs',
    '108': 'Golden (Deep-Sea) Crabs Kaa',
    '109': 'Fresh Water Shrimp',
    '110': 'Octopus (Pweza)',
    '111': 'Cuttlefish',
    '112': 'Squid(Ngisi)',
    '113': 'Oysters',
    '114': 'Fish Oil',
    '115': 'Fish Maws',
    '117': 'Nile Perch Skins',
    '121': 'Black nightshade (Managu/ Osuga)',
    '122': 'Spider flower (Saga)',
    '123': 'Amaranthus (Terere)',
    '124': 'Jute Plant (Murenda)',
    '125': 'Passion Fruits',
    '127': 'Oranges',
    '128': 'Tree tomato',
    '129': 'Pepino melon',
    '130': 'Thorn melon',
    '131': 'Yam',
    '133': 'Cow Milk(At collection point)',
    '134': 'Camel Milk(At collection point)',
    '138': 'Camel milk(Processed)',
    '139': 'Goat milk (Processed)',
    '140': 'Cattle',
    '141': 'Pork',
    '142': 'Avocado',
    '143': 'Arrow Root',
    '145': 'Lemons',
    '147': 'Mangoes',
    '148': 'Limes',
    '149': 'Green Maize',
    '150': 'Water Melon',
    '151': 'Pineapples',
    '152': 'Pawpaw',
    '153': 'Cow Milk(Processd)',
    '154': 'Kales/Sukuma Wiki',
    '158': 'Dry Onions',
    '159': 'Spring Onions',
    '160': 'Fresh Peas',
    '161': 'Spinach',
    '162': 'Cassava Fresh',
    '163': 'White Irish Potatoes',
    '164': 'Cassava Chips (dry)',
    '165': 'Chillies',
    '166': 'Lettuce',
    '167': 'Sheep',
    '168': 'Goat',
    '169': 'Donkey',
    '170': 'Pumpkin',
    '171': 'Butternuts',
    '172': 'Capsicums',
    '173': 'Cucumber',
    '174': 'Egg plant (Brinjals)',
    '175': 'Cauliflower',
    '177': 'French beans',
    '178': 'Ginger',
    '180': 'Garlic',
    '182': 'Njugu Mawe',
    '183': 'Beans Rosecoco (Nyayo)',
    '184': 'Nile Perch',
    '186': 'Camel',
    '187': 'Rabbit',
    '188': 'Pigeon peas',
    '189': 'Cowpeas',
    '190': 'Scavengers (Changu/Tangu)',
    '191': 'Parrotfishes(Pono)',
    '192': 'Groupers',
    '193': 'Grunt(Taamamba/Kora)',
    '194': 'Mullets(Fumi)',
    '195': 'Surgeonfishes',
    '196': 'Threadfin breams',
    '197': 'Goatfishes',
    '198': 'Rayfish',
    '199': 'Needlefishes',
    '200': 'Jacks/Trevallies(Kolekole)',
    '201': 'Halfbeaks',
    '202': 'Anchovies',
    '203': 'Sailfishes',
    '204': 'Wolf Herrings',
    '205': 'Marlins',
    '206': 'Jobfish',
    '207': 'Mixed Pelagics',
    '208': 'Camel meat',
    '209': 'Meat Chevon',
    '210': 'Rabbit Meat',
    '211': 'Pigs',
    '212': 'Honey',
    '213': 'Cattle Hide',
    '214': 'Camel Hide',
    '215': 'Goat Skin',
    '216': 'Sheep Skin',
    '217': 'Fertilizer',
    '218': 'Tea',
    '219': 'Coffee',
    '220': 'Wheat Bran',
    '221': 'Maize Bran',
    '222': 'Sunflower Cake',
    '223': 'Cotton Seed',
    '224': 'Cotton',
    '226': 'Banana (Ripening)',
    '227': 'Chicken',
    '228': 'Macademia Seed',
    '230': 'Cowpea leaves (Kunde)',
    '231': 'Nderema- Vine Spinach',
    '233': 'Pumpkin Leaves',
    '234': 'Ethiopian Kales -Kanzira',
    '235': 'Indigenous Crotolaria (Mito/Miro)',
    '237': 'Soybean oil',
    '238': 'Coconut Oil',
    '239': 'Sunflower Seeds',
    '240': 'Sunflower Oil',
    '241': 'Walnut Seed',
    '242': 'Coriander (Dhania)',
    '243': 'Grapes',
    '244': 'Apples',
    '245': 'Dry Peas',
    '246': 'Mixed Beans',
    '247': 'Rockcode(Tewa)',
    '248': 'Queenfish (Pandu)',
    '249': 'Maize Flour',
    '251': 'Duck',
    '255': 'Banana (Cooking)',
    '256': 'Banana (Plantain)',
    '257': 'Courgette',
    '258': 'Broccoli',
    '259': 'Lentils',
    '261': 'Fish Scales',
    '262': 'Tangerine (Sandara)',
    '263': 'Pasta',
    '264': 'Spaghetti',
    '265': 'Wheat Flour',
    '267': 'Paddy',
    '269': 'Beans (Yellow)',
    '270': 'Coconut',
    '272': 'Okra',
    '273': 'Cashewnuts (Korosho)'
}

def create_table():
    """Create the market_prices table if it doesn't exist"""
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS market_prices (
        id SERIAL PRIMARY KEY,
        commodity_id VARCHAR(10),
        commodity VARCHAR(100),
        classification VARCHAR(100),
        grade VARCHAR(50),
        sex VARCHAR(50),
        market VARCHAR(100),
        wholesale_price NUMERIC(10,2),
        retail_price NUMERIC(10,2),
        supply_volume NUMERIC(12,2),
        county VARCHAR(100),
        date DATE,
        time_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE (commodity_id, market, date)
    )
    """)
    conn.commit()
    cursor.close()
    conn.close()
    logging.info("Database table ready")

def clean_price(price_str):
    """Extract numeric value from price strings like '31.11/Kg'"""
    if not price_str or price_str.strip() == '-':
        return None
    match = re.search(r'(\d+\.?\d*)', price_str.replace(',', ''))
    return float(match.group(1)) if match else None

def clean_volume(vol_str):
    """Clean supply volume values"""
    if not vol_str:
        return None
    try:
        return float(vol_str.replace(',', ''))
    except ValueError:
        return None

def scrape_kamis_page(commodity_id=None, page=0, per_page=500):
    """Scrape a single page of KAMIS data"""
    url = "https://amis.co.ke/index.php/site/market"
    params = {
        'product': commodity_id,
        'per_page': per_page
    }
    if page > 0:
        params['page'] = page * per_page
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept-Language': 'en-US,en;q=0.9'
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logging.error(f"Request failed for commodity {commodity_id}: {e}")
        return None

def parse_kamis_page(html, commodity_id=None):
    """Parse HTML page and extract market data"""
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', {'class': 'table table-bordered table-condensed'})
    
    if not table:
        logging.warning("Price table not found in HTML")
        return []
    
    records = []
    for row in table.find_all('tr')[1:]:  # Skip header
        cols = row.find_all('td')
        if len(cols) < 10:
            continue

        try:
            record = {
                'commodity_id': commodity_id,
                'commodity': COMMODITY_MAP.get(commodity_id, cols[0].get_text(strip=True)),
                'classification': cols[1].get_text(strip=True),
                'grade': cols[2].get_text(strip=True),
                'sex': cols[3].get_text(strip=True),
                'market': cols[4].get_text(strip=True),
                'wholesale_price': clean_price(cols[5].get_text(strip=True)),
                'retail_price': clean_price(cols[6].get_text(strip=True)),
                'supply_volume': clean_volume(cols[7].get_text(strip=True)),
                'county': cols[8].get_text(strip=True),
                'date': datetime.strptime(cols[9].get_text(strip=True), '%Y-%m-%d').date()
            }
            records.append(record)
        except Exception as e:
            logging.error(f"Error processing row: {e}")
            continue
    
    return records

def save_to_database(records):
    """Save scraped records to database"""
    if not records:
        return 0
    
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    new_records = 0
    
    try:
        for record in records:
            cursor.execute("""
            INSERT INTO market_prices (
                commodity_id, commodity, classification, grade, sex, market,
                wholesale_price, retail_price, supply_volume, county, date
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (commodity_id, market, date) DO NOTHING
            """, (
                record['commodity_id'],
                record['commodity'],
                record['classification'],
                record['grade'],
                record['sex'],
                record['market'],
                record['wholesale_price'],
                record['retail_price'],
                record['supply_volume'],
                record['county'],
                record['date']
            ))
            new_records += cursor.rowcount
        
        conn.commit()
        return new_records
    except Exception as e:
        conn.rollback()
        logging.error(f"Database error: {e}")
        return 0
    finally:
        cursor.close()
        conn.close()

def scrape_all_commodities():
    """Scrape data for all commodities"""
    total_new_records = 0
    
    for commodity_id, commodity_name in COMMODITY_MAP.items():
        logging.info(f"Scraping data for {commodity_name} (ID: {commodity_id})")
        
        # Scrape first page
        html = scrape_kamis_page(commodity_id)
        if not html:
            continue
        
        records = parse_kamis_page(html, commodity_id)
        new_records = save_to_database(records)
        total_new_records += new_records
        logging.info(f"Added {new_records} new records for {commodity_name}")
        
        # Add random delay to avoid being blocked
        sleep(random.uniform(1, 3))
    
    logging.info(f"Total new records added: {total_new_records}")
    return total_new_records

if __name__ == "__main__":
    create_table()
    scrape_all_commodities()