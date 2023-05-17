from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler
from main import *
from connection import cur, conn
import phonenumbers
import pandas as pd
import re
from datetime import datetime
postrr_Data_list = ["", "", "", "", "", "", "",
                    "", "", "", "", "", "", "", "", "", "", "", ""]


query = """CREATE TABLE IF NOT EXISTS poster (
    id SERIAL PRIMARY KEY,
    city VARCHAR(255),
    url VARCHAR(255),
    caption VARCHAR(255),
    pictureurl VARCHAR(255),
    oftype VARCHAR(255),
    pincode VARCHAR(255),
    description VARCHAR(255),
    address VARCHAR(255),
    postingdate DATE,
    vacantfrom DATE,
    area VARCHAR(255),
    warmrent VARCHAR(255),
    rooms VARCHAR(255),
    mobile VARCHAR(255),
    email VARCHAR(255),
    web VARCHAR(255),
    sublocality VARCHAR(255),
    latitude VARCHAR(255),
    longitude VARCHAR(255),
    placeid VARCHAR(255),
    creationtimestamp TIMESTAMP,
    spam INTEGER DEFAULT 0,
    telegram_id VARCHAR(255),
    user_type VARCHAR(255),
    rent VARCHAR(255),
    high_rent VARCHAR(255),
    Anmeldung VARCHAR(255),
    start_date VARCHAR(255),
    end_date VARCHAR(255),
    people VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)"""

cur.execute(query)
conn.commit()
import os



def bulk_upload(update, context):

    '''
    this function is used to upload the bulk data using excel file
    '''
    update.message.reply_text(
        'Please send your excel file', reply_markup=ReplyKeyboardRemove())
    path = os.path.join(os.getcwd(), 'Telegram//Poster_Sample.xlsx')
    update.message.reply_document(
        document=open(path, 'rb'))
    return "upload"

def upload(update, context):
    '''
    this function handles the excel file and upload the data into database
    '''
    file = context.bot.getFile(update.message.document.file_id)
    file.download('poster_list.xlsx')
    update.message.reply_text(
        'Please wait while we are uploading your data', reply_markup=ReplyKeyboardRemove())

    df = pd.read_excel(r'poster_list.xlsx')
    path = os.path.join(os.getcwd(), 'Telegram\Sample.xlsx')
    sample_df = pd.read_excel(path)
    if list(df.columns) == list(sample_df.columns):
        for index, row in df.iterrows():
            query = "INSERT INTO poster ( city , description ,Anmeldung , start_date , end_date , rent , mobile , area , rooms ) VALUES ( '" + str(row['City']) + "' , '" + str(row['Description']) + "' , '" + str(row['Anmeldung ']) + "' , '" + str(row['Start Date']) + "' , '" + str(row['End Date']) + "' , '" + str(row['Rent']) + "' , '" + str(row['Mobile Number']) + "' , '" + str(row['Location']) + "' , '" + str(row['No. of Rooms']) + "' )"
            cur.execute(query)
            conn.commit()
        update.message.reply_text(
            'Your data has been uploaded successfully', reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
    else:
        update.message.reply_text(
            'Please upload correct file', reply_markup=ReplyKeyboardRemove())
        update.message.reply_text(
            'To start again please type /start', reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
    


def poster_type(update, context):
    '''
    this function is used to get the type of poster
    '''
    poster_type = str(update.message.text)
    checker_keyword = ['current tenant', 'agent', 'housing co', 'landlord']
    cur.execute("select user_type from listings where telegram_id =" +
                str(update.message.from_user.id)+"::text")

    type = cur.fetchone()
    if poster_type in [ 2,3,4, '2' , '3' , '4' ]:
        poster_type = checker_keyword[int(poster_type)-1]
        update.message.reply_text(
            'Please send your excel file', reply_markup=ReplyKeyboardRemove())
        path = os.path.join(os.getcwd(), 'Telegram\Sample.xlsx')
        update.message.reply_document(
            document=open(path, 'rb'))
        return "upload"
    elif poster_type in [1, '1']:
        poster_type = 'current tenant'
        query = "UPDATE poster SET user_type = '"+poster_type + \
            "' WHERE telegram_id ="+str(update.message.from_user.id)+"::text"
        cur.execute(query)
        conn.commit()
        reply_keyboard = [[1, 2], [
            3, 4], [5]]
        update.message.reply_text(
            'Please select your City (Type the number or click on the button): \n 1.Munich \n 2.Berlin \n 3.Frankfurt \n 4.Dusseldorf \n 5.Hamburg',
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True),

        )
        return "city"

    else:
        return 'Options'


def city_type(update, context):
    city_type = str(update.message.text)
    reply = ['Munich', 'Berlin', 'Frankfurt', 'Dusseldorf', 'Hamburg']
    if city_type in [1, '1',2, '2',3, '3',4, '4',5, '5']:
        city_type = reply[int(city_type)-1]
        query = "UPDATE poster SET city = '"+city_type + \
            "' WHERE telegram_id ="+str(update.message.from_user.id)+"::text"
        cur.execute(query)
        conn.commit()
        postrr_Data_list.insert(2, city_type)
        update.message.reply_text(
            'Please write your area in text field', reply_markup=ReplyKeyboardRemove())
        return "location"
    else:
        poster_type(update, context)


def location(update, context):
    area = str(update.message.text)
    query = "UPDATE poster SET area = '"+area + \
        "' WHERE telegram_id ="+str(update.message.from_user.id)+"::text"
    cur.execute(query)
    conn.commit()

    update.message.reply_text(
        'Please write your address in text field', reply_markup=ReplyKeyboardRemove())
    return "address"


def address(update, context, co=0):
    poster_address = str(update.message.text)
    if co == 1:
        reply_keyboard = [[1,2],[3,4],[5]]
        update.message.reply_text(
            'Please select your home type (Type the number or click on the button): \n 1.Flat \n 2.House \n 3.Studio \n 4.Shared Room \n 5.Shared Apartments)',
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True),

        )

        return "home_type"
    else:
        query = "UPDATE poster SET address = '"+poster_address + \
            "' WHERE telegram_id ="+str(update.message.from_user.id)+"::text"
        cur.execute(query)
        conn.commit()
        reply_keyboard = [[1,2],[3,4],[5]]
        update.message.reply_text(
            'Please select your home type (Type the number or click on the button): \n 1.Flat \n 2.House \n 3.Studio \n 4.Shared Room \n 5.Shared Apartments)',
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True),
        )

        return "home_type"


def home_type(update, context, co=0):
    home_types = str(update.message.text)
    key_Word = ['Flat', 'House', 'Studio', 'Shared Room', 'Shared Apartments']
    cur.execute("select oftype from listings where telegram_id =" +
                str(update.message.from_user.id)+"::text")

    type = cur.fetchone()
    if home_types in [1, '1',2, '2',3, '3',4, '4',5, '5']:
        home_types = key_Word[int(home_types)-1]

        query = "UPDATE poster SET oftype = '"+home_types + \
            "' WHERE telegram_id ="+str(update.message.from_user.id)+"::text"
        cur.execute(query)
        conn.commit()
        global home_typess
        home_typess = home_types
        update.message.reply_text(
            'Enter your lower rent', reply_markup=ReplyKeyboardRemove())
        return "lower_rent"
    else:
        address(update, context, 1)


def lower_rent(update, context):
    lower_rent = str(update.message.text)

    try:
        lower_rent = str(update.message.text)
        # rent
        query = "UPDATE poster SET rent = '"+lower_rent + \
            "' WHERE telegram_id ="+str(update.message.from_user.id)+"::text"
        cur.execute(query)
        conn.commit()

        lower_rent = int(lower_rent)
        update.message.reply_text(
            'Enter your higher rent', reply_markup=ReplyKeyboardRemove())
        postrr_Data_list.insert(5, lower_rent)
        return "higher_rent"
    except:
        update.message.reply_text(
            'Enter your lower rent', reply_markup=ReplyKeyboardRemove())
        return "lower_rent"


def higher_rent(update, context):
    higher_rent = str(update.message.text)

    try:
        higher_rent = str(update.message.text)

        higher_rent = int(higher_rent)
        query = "UPDATE poster SET high_rent = '" + \
            str(higher_rent)+"' WHERE telegram_id =" + \
            str(update.message.from_user.id)+"::text"
        cur.execute(query)
        conn.commit()
        update.message.reply_text(
            'Enter your Flat or house or studio Area in meater', reply_markup=ReplyKeyboardRemove())

        return "flat_area"

    except Exception as e:

        update.message.reply_text(
            'Enter your higher rent', reply_markup=ReplyKeyboardRemove())
        return "higher_rent"


def shared_area(update, context):
    sharedflat_area = str(update.message.text)

    try:
        sharedflat_area = str(update.message.text)
        postrr_Data_list.insert(7, sharedflat_area)
        sharedflat_area = int(sharedflat_area)
        query = "UPDATE poster SET area = '" + \
            str(sharedflat_area)+"' WHERE telegram_id =" + \
            str(update.message.from_user.id)+"::text"
    
        cur.execute(query)
        conn.commit()
        update.message.reply_text(
            'Enter Starting Date You are avilable.(Ex: 09/11/2023)', reply_markup=ReplyKeyboardRemove())
        return "start_date"
    except:
        update.message.reply_text(
            'Enter your shared Flat or shared room Area in meater', reply_markup=ReplyKeyboardRemove())
        return "shared_area"


def flat_area(update, context):
    flat_area = str(update.message.text)

    try:
        flat_area = str(update.message.text)
        query = "UPDATE poster SET area = '" + \
            str(flat_area)+"' WHERE telegram_id =" + \
            str(update.message.from_user.id)+"::text"

        cur.execute(query)
        conn.commit()
        update.message.reply_text(
            'Enter Your Staying Duration(Ex: DD/MM/YYYY - DD/MM/YYYY)', reply_markup=ReplyKeyboardRemove())
 
        return "start_date"
    except:
        update.message.reply_text(
            'Enter your Flat or house or studio Area in meater', reply_markup=ReplyKeyboardRemove())
        return "flat_area"


def date_format_check(date_text):
    try:
        val = date_text.split("-")
        datetime.strptime(val[0].strip(), '%d/%m/%Y')
        datetime.strptime(val[1].strip(), '%d/%m/%Y')
        return True
    except:
        return False


def start_date(update, context):
    start_date = str(update.message.text)
    try:
        if date_format_check(start_date):
            query = "UPDATE poster SET vacantfrom = '" + \
                str(start_date.split(
                    '-')[0].strip())+"' WHERE telegram_id =" + \
                str(update.message.from_user.id)+"::text"

            cur.execute(query)
            conn.commit()
            
            query = ("UPDATE poster SET start_date = '"
                + str(start_date.split("-")[0].strip())
                + "' WHERE telegram_id ="
                + str(update.message.from_user.id)+"::text"
            )
            cur.execute(query)
            conn.commit()
            query = ("UPDATE poster SET end_date = '"
                + str(start_date.split("-")[1].strip())
                + "' WHERE telegram_id ="
                + str(update.message.from_user.id)+"::text"
            )
            cur.execute(query)
            conn.commit()


            postrr_Data_list.insert(9, start_date)
            update.message.reply_text(
                'Enter your phone number', reply_markup=ReplyKeyboardRemove())
            return "phone_number"
        else:
            update.message.reply_text(
                'Incorrect format, should be (DD/MM/YYYY - DD/MM/YYYY)', reply_markup=ReplyKeyboardRemove())
            return "start_date"

    except Exception as e:
        update.message.reply_text(
            'Incorrect format, should be (DD/MM/YYYY - DD/MM/YYYY)', reply_markup=ReplyKeyboardRemove())
        return "start_date"


def global_phone_number_validation(phone_number):
    try:
        phone_number = phonenumbers.parse(phone_number, "GB")
        if phonenumbers.is_valid_number(phone_number):
            return True
        else:
            return False
    except:
        return False


def phone_number(update, context):
    phone_number = str(update.message.text)
    if global_phone_number_validation(phone_number):
        postrr_Data_list.insert(10, phone_number)
        query = "UPDATE poster SET mobile = '" + \
            str(phone_number)+"' WHERE telegram_id =" + \
            str(update.message.from_user.id)+"::text"
        cur.execute(query)
        conn.commit()
        update.message.reply_text(
            'Enter your email', reply_markup=ReplyKeyboardRemove())
        return "email"
    else:
        update.message.reply_text(
            'Incorrect phone number format, should be +44XXXXXXXXXX', reply_markup=ReplyKeyboardRemove())
        return "phone_number"
    
def email_validation(email):
    try:
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return True
        else:
            return False
    except:
        return False

def email(update, context):
    email = str(update.message.text)
    if email_validation(email):
        postrr_Data_list.insert(11, email)
        query = "UPDATE poster SET email = '" + \
            str(email)+"' WHERE telegram_id =" + \
            str(update.message.from_user.id)+"::text"
        cur.execute(query)
        conn.commit()
        update.message.reply_text(
            'Enter number of people required ', reply_markup=ReplyKeyboardRemove())
        return "people"
    else:
        update.message.reply_text(
            'Incorrect email format ', reply_markup=ReplyKeyboardRemove())
        return "email"
    


    


def people(update, context):
    people = str(update.message.text)

    query = "UPDATE poster SET people = '" + \
        str(people)+"' WHERE telegram_id =" + \
        str(update.message.from_user.id)+"::text"
    cur.execute(query)
    conn.commit()

    update.message.reply_text(
        "Your Data Enter Successfully", reply_markup=ReplyKeyboardRemove())
    update.message.reply_text(
        'You can search your room or flat in search option.', reply_markup=ReplyKeyboardRemove())
    update.message.reply_text(
        'Enter /start to go back to main menu', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END



def User_Data(update, context):
    people = str(update.message.text)
    # get data from database based on telegram id and return it to user
    query = 'SELECT * FROM poster WHERE telegram_id =' + \
        str(update.message.from_user.id)+"::text"
    cur.execute(query)
    data = cur.fetchone()

    user_data = '''
    Here is your data
    User Name: '''+update.message.from_user.first_name+'''
    User Email: '''+str(data[2])+'''
    User Phone Number: '''+str(data[3])+'''
    Type of Listing: '''+str(data[4])+'''
    Type of Property: '''+str(data[5])+'''
    Number of Rooms: '''+str(data[6])+'''
    Number of Bathrooms: '''+str(data[7])+'''
    Area: '''+str(data[8])+'''
    Staying Duration: '''+str(data[9])+'''
    Number of People: '''+str(data[10])+'''

    Please wait for our team to contact you
    Thank you for using our service
    '''
    # send data to user
    cur.execute("SELECT * FROM listings LIMIT 0")
    colnames = [desc[0] for desc in cur.description]
    user_id = update.message.from_user.id
    user_name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name
    update.message.reply_text(
        user_data, reply_markup=ReplyKeyboardRemove())
    update.message.reply_text(
        'Start a new conversation by typing /start',
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

