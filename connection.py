import psycopg2
from dotenv import load_dotenv
import os
    
# Set up the connection parameters
conn_params = {
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'dbname': os.getenv('DB_NAME'),
    'user': 'postgres',
    'password': '123456'
}

# Connect to the database
conn = psycopg2.connect(**conn_params)

# Open a cursor to perform database operations
cur = conn.cursor()
# # drop table if exists seeker , poster
# query = """DROP TABLE IF EXISTS seeker , poster"""
# cur.execute(query)
# conn.commit()
# truncate search table






query = """CREATE TABLE IF NOT EXISTS seeker (
    id SERIAL PRIMARY KEY,
    telegram_id INTEGER,
    user_type VARCHAR(255),
    city VARCHAR(255),
    address VARCHAR(255),
    area VARCHAR(255),
    apartment VARCHAR(255),
    rent VARCHAR(255),
    high_rent VARCHAR(255),
    Anmeldung VARCHAR(255),
    startdate VARCHAR(255),
    end_date VARCHAR(255),
    mobile VARCHAR(255),
    email VARCHAR(255),
    people VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)"""
cur.execute(query)
conn.commit()

# query = """CREATE TABLE IF NOT EXISTS listings (
#     id SERIAL PRIMARY KEY,
#     city VARCHAR(255),
#     url VARCHAR(255),
#     caption VARCHAR(255),
#     pictureurl VARCHAR(255),
#     oftype VARCHAR(255),
#     pincode VARCHAR(255),
#     description VARCHAR(255),
#     address VARCHAR(255),
#     postingdate DATE,
#     vacantfrom DATE,
#     area VARCHAR(255),
#     warmrent VARCHAR(255),
#     rooms VARCHAR(255),
#     web VARCHAR(255),
#     sublocality VARCHAR(255),
#     latitude VARCHAR(255),
#     longitude VARCHAR(255),
#     placeid VARCHAR(255),
#     creationtimestamp TIMESTAMP,
#     spam INTEGER DEFAULT 0,
#     telegram_id VARCHAR(255),
#     user_type VARCHAR(255),
#     rent VARCHAR(255),
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# )"""
# cur.execute(query)
# conn.commit()
import re
import phonenumbers

def email_validation(email):
    try:
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return True
        else:
            return False
    except:
        return False
    
def global_phone_number_validation(phone_number):
    try:
        phone_number = phonenumbers.parse(phone_number, "GB")
        if phonenumbers.is_valid_number(phone_number):
            return True
        else:
            return False
    except:
        return False
