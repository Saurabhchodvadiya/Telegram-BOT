from telegram import (
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from telegram.ext import ConversationHandler
from poster import global_phone_number_validation , email_validation
from poster import date_format_check
from connection import cur, conn


query = """CREATE TABLE IF NOT EXISTS seeker (
    id SERIAL PRIMARY KEY,
    telegram_id INTEGER,
    user_type VARCHAR(255),
    city VARCHAR(255),
    address VARCHAR(255),
    area VARCHAR(255),
    apartment VARCHAR(255),
    rent VARCHAR(255),
    startdate VARCHAR(255),
    end_date VARCHAR(255),
    mobile VARCHAR(255),
    email VARCHAR(255),
    people VARCHAR(255),
    previous_city VARCHAR(255),
    high_rent VARCHAR(255),
    previous_country VARCHAR(255),
    anmeldung VARCHAR(255),
    flat_share VARCHAR(255),
    kids VARCHAR(255),
    kids_age VARCHAR(255),
    smoke VARCHAR(255),
    gender_preference VARCHAR(255),
    pets VARCHAR(255),
    pets_type VARCHAR(255),
    college_name VARCHAR(255),
    company_name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)"""
cur.execute(query)
conn.commit()


def seeker_type(update, context):
    poster_type = str(update.message.text)
    checker_keyword = ["Students", "Profesional", "Academics"]
    if poster_type in [1, 2, 3, "1", "2", "3"]:
        poster_type = checker_keyword[int(poster_type) - 1]
        query = (
            "UPDATE seeker SET user_type = '"
            + poster_type
            + "' WHERE telegram_id ="
            + str(update.message.from_user.id)
        )
        cur.execute(query)
        conn.commit()

        if poster_type == "Profesional":
            update.message.reply_text(
                "What is your company name?" ,
                reply_markup=ReplyKeyboardRemove())
            
            return "seeker_company_name"
        else:
            update.message.reply_text(
                "What is your college name?" ,
                reply_markup=ReplyKeyboardRemove())
            
            return "seeker_college_name"
    else:
        update.message.reply_text(
            'Invalid Input.')
        return 'seeker_type'
    
def seeker_company_name(update, context):
    company_name = str(update.message.text)
    query = (
        "UPDATE seeker SET company_name = '"
        + company_name
        + "' WHERE telegram_id ="
        + str(update.message.from_user.id)
    )
    cur.execute(query)
    conn.commit()
    reply_keyboard = [[1, 2, 3, 4, 5, 6]]
    update.message.reply_text(
            "Are you currently in which city? (Type from keyboard button or click on keyboard button) : \n 1. Munich \n 2. Berlin \n 3. Frankfurt \n 4. Dusseldorf \n 5. Hamburg \n 6. Other City",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
        )
    return "seeker_previous_city"

def seeker_college_name(update, context):
    college_name = str(update.message.text)
    query = (
        "UPDATE seeker SET college_name = '"
        + college_name
        + "' WHERE telegram_id ="
        + str(update.message.from_user.id)
    )
    cur.execute(query)
    conn.commit()
    reply_keyboard = [[1, 2, 3, 4, 5, 6]]
    update.message.reply_text(
            "Are you currently in which city? (Type from keyboard button or click on keyboard button) : \n 1. Munich \n 2. Berlin \n 3. Frankfurt \n 4. Dusseldorf \n 5. Hamburg \n 6. Other City",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
        )
    return "seeker_previous_city"

def seeker_previous_city(update, context):
    previous_city = str(update.message.text)
    if previous_city in [1, 2, 3, 4, 5, "1", "2", "3", "4", "5",6,'6']:
        reply = ["Munich", "Berlin", "Frankfurt", "Dusseldorf", "Hamburg", "Other City"]
        previous_city = reply[int(previous_city) - 1]
        query = (
            "UPDATE seeker SET previous_city = '"
            + previous_city
            + "' WHERE telegram_id ="
            + str(update.message.from_user.id)
        )
        cur.execute(query)
        conn.commit()
        if previous_city == "Other City":
            update.message.reply_text(
                "Please write your city in text field", reply_markup=ReplyKeyboardRemove()
            )
            return "seeker_previous_city_other"
        else:
            reply_keyboard = [[1, 2, 3, 4, 5]]
            update.message.reply_text(
                "In which city you find place ? (Type from keyboard button or click on keyboard button): \n 1. Munich \n 2. Berlin \n 3. Frankfurt \n 4. Dusseldorf \n 5. Hamburg",
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
            )
            return "seeker_city_type"
    else:
        update.message.reply_text(
            'Invalid Input.')
        
        return 'seeker_previous_city'
    
def seeker_previous_city_other(update, context):
    previous_city_other = str(update.message.text)
    query = (
        "UPDATE seeker SET previous_city = '"
        + previous_city_other
        + "' WHERE telegram_id ="
        + str(update.message.from_user.id)
    )
    cur.execute(query)
    conn.commit()
    update.message.reply_text(
        "Please write your country in text field", reply_markup=ReplyKeyboardRemove()
    )
    return "seeker_previous_country"

def seeker_previous_country(update, context):
    previous_country = str(update.message.text)
    query = (
        "UPDATE seeker SET previous_country = '"
        + previous_country
        + "' WHERE telegram_id ="
        + str(update.message.from_user.id)
    )
    cur.execute(query)
    conn.commit()
    reply_keyboard = [[1, 2, 3, 4, 5]]
    update.message.reply_text(
                "In which city you find place ? (Type from keyboard button or click on keyboard button): \n 1. Munich \n 2. Berlin \n 3. Frankfurt \n 4. Dusseldorf \n 5. Hamburg",
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
            )
    return "seeker_city_type"

def seeker_city_type(update, context):
    city_type = str(update.message.text)
    reply = ["Munich", "Berlin", "Frankfurt", "Dusseldorf", "Hamburg"]

    if city_type in ["1", "2", "3", "4", "5", 1, 2, 3, 4, 5]:
        city_type = reply[int(city_type) - 1]
        query = (
            "UPDATE seeker SET city = '"
            + city_type
            + "' WHERE telegram_id ="
            + str(update.message.from_user.id)
        )
        cur.execute(query)
        conn.commit()
        query =f"select boroughname from boroughs join cities on cities.id = boroughs.cityid where cities.cityname = '{city_type}'"
        cur.execute(query)
        city_id = cur.fetchall()
        if city_id==[]:
            update.message.reply_text(
                "Please write your area in text field", reply_markup=ReplyKeyboardRemove()
            )
        else:
            reply_keyboard = [[i for i in range(len(city_id))]]
            
            update.message.reply_text(
                "Please select your area (Type from keyboard button or click on keyboard button):"+" \n".join([str(i)+"). "+j[0] for i,j in enumerate(city_id)]),
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
            )
        return "seeker_location"
    else:
        update.message.reply_text(
            'Invalid Input.')
        return 'seeker_city_type'


def seeker_location(update, context):
    area = str(update.message.text)
    query = (
        "UPDATE seeker SET area = '"
        + area
        + "' WHERE telegram_id ="
        + str(update.message.from_user.id)
    )
    cur.execute(query)
    conn.commit()

    update.message.reply_text(
        "Please write your address in text field", reply_markup=ReplyKeyboardRemove()
    )
    return "seeker_address"


def seeker_address(update, context, co=0):
    poster_address = str(update.message.text)
    if co == 1:
        reply_keyboard = [[1, 2], [3, 4], [5]]
        update.message.reply_text(
            "Please select your home type (Type from keyboard button or click on keyboard button) :  \n 1. Flat \n 2. House \n 3. Studio \n 4. Shared Room \n 5. Shared Apartments",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
        )
        return "seeker_home_type"
    else:
        query = (
            "UPDATE seeker SET address = '"
            + poster_address
            + "' WHERE telegram_id ="
            + str(update.message.from_user.id)
        )
        cur.execute(query)
        conn.commit()
        reply_keyboard = [[1, 2], [3, 4], [5]]
        update.message.reply_text(
            "Please select your home type (Type from keyboard button or click on keyboard button) :  \n 1. Flat \n 2. House \n 3. Studio \n 4. Shared Room \n 5. Shared Apartments",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
        )

        return "seeker_home_type"


def seeker_home_type(update, context, co=0):
    home_types = str(update.message.text)
    key_Word = ["Flat", "House", "Studio", "Shared Room", "Shared Apartments"]

    if home_types in [1, 2, 3, 4, 5, "1", "2", "3", "4", "5"]:
        home_types = key_Word[int(home_types) - 1]
        query = (
            "UPDATE seeker SET apartment = '"
            + home_types
            + "' WHERE telegram_id ="
            + str(update.message.from_user.id)
        )
        cur.execute(query)
        conn.commit()
        global home_typess
        home_typess = home_types

        if home_types == "Shared Apartments" :
            reply_keyboard = [[1, 2, 3]]
            update.message.reply_text(
                "What kind of flat share would you like? (Type from keyboard button or click on keyboard button) :  \n 1. Very social, love parties \n 2. Social but need my space \n 3. Functional only",
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
            )
            return "seeker_flat_share"
        else:
            reply_keyboard = [[1, 2]]
            update.message.reply_text(
                "Do you have kids? (Type from keyboard button or click on keyboard button) :  \n 1. Yes \n 2. No",
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
            )
            return "seeker_kids"
        

        
    else:
        seeker_address(update, context, 1)


def seeker_flat_share(update, context):
    flat_share = str(update.message.text)
    key_Word = ["Very social, love parties", "Social but need my space", "Functional only"]
    if flat_share in [1, 2, 3, "1", "2", "3"]:
        flat_share = key_Word[int(flat_share) - 1]
        query = "UPDATE seeker SET flat_share = '"+flat_share + \
            "' WHERE telegram_id ="+str(update.message.from_user.id)
        cur.execute(query)
        conn.commit()
        reply_keyboard = [[1, 2, 3, 4]]
        update.message.reply_text(
            'Any gender preference ? \n 1). Male only \n 2). Female only \n 3). Mixed, open to any \n 4). LGBTQ friendly',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
        )

        return 'seeker_gender_preference'



        # reply_keyboard = [[1, 2, 3]]
        # update.message.reply_text(
        #     "Anmeldung Required : \n 1. Yes \n 2. No \n 3. Maybe",
        #     reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
        # )

        # return "seeker_anmeldung"
    else:
        update.message.reply_text(
            'Invalid Input.')
        return 'seeker_flat_share'

def seeker_gender_preference(update, context):
    key_Word = ['Male only' , 'Female only' , 'Mixed, open to any' , 'LGBTQ friendly' ]
    gender_preference = str(update.message.text)
    if gender_preference in [1, 2, 3, 4, '1', '2', '3', '4']:
        gender_preference = key_Word[int(gender_preference) - 1]
        query = "UPDATE seeker SET gender_preference = '"+gender_preference + \
            "' WHERE telegram_id ="+str(update.message.from_user.id)
        cur.execute(query)
        conn.commit()
        reply_keyboard = [[1, 2, 3]]
        update.message.reply_text(
            "Anmeldung Required : \n 1. Yes \n 2. No \n 3. Maybe",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
        )

        return "seeker_anmeldung"
    else:
        update.message.reply_text(
            'Invalid Input.')
        
        return 'seeker_gender_preference'
        



def seeker_kids(update, context):
    kids = str(update.message.text)
    key_Word = ["Yes", "No"]
    if kids in [1, 2, "1", "2"]:
        kids = key_Word[int(kids) - 1]
        query = "UPDATE seeker SET kids = '"+kids + \
            "' WHERE telegram_id ="+str(update.message.from_user.id)
        cur.execute(query)
        conn.commit()
        if kids == "Yes":
            update.message.reply_text(
                "How many kids, and what are their ages?...(free text)"
            )
            return "seeker_kids_age"
        else:
            reply_keyboard = [[1, 2, 3]]
            update.message.reply_text(
                "Anmeldung Required : \n 1. Yes \n 2. No \n 3. Maybe",
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
            )

            return "seeker_anmeldung"
    else:
        update.message.reply_text(
            'Invalid Input.')
        return 'seeker_kids'
    
def seeker_kids_age(update, context):
    kids_age = str(update.message.text)
    query = "UPDATE seeker SET kids_age = '"+kids_age + \
        "' WHERE telegram_id ="+str(update.message.from_user.id)
    cur.execute(query)
    conn.commit()
    reply_keyboard = [[1, 2, 3]]
    update.message.reply_text(
        "Anmeldung Required : \n 1. Yes \n 2. No \n 3. Maybe",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return "seeker_anmeldung"

def seeker_anmeldung(update, context):
    anmeldung = str(update.message.text)
    key_Word = ["Yes", "No", "Not Sure"]
    if anmeldung in [1, 2, 3, "1", "2", "3"]:
        anmeldung = key_Word[int(anmeldung) - 1]
        query = "UPDATE seeker SET anmeldung = '"+anmeldung + \
            "' WHERE telegram_id ="+str(update.message.from_user.id)
        cur.execute(query)
        conn.commit()
#         Do you have pets?
# 1. Yes
# 2. No
# If No continue...if yes,...

# How many pets, what pets?...(free text)

        reply_keyboard = [[1, 2]]
        update.message.reply_text(
            "Do you have pets? \n 1. Yes \n 2. No",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
        )

        return "seeker_pets"

        
    else:
        seeker_home_type(update, context, 1)

def seeker_pets(update, context):
    pets = str(update.message.text)
    key_Word = ["Yes", "No"]
    if pets in [1, 2, "1", "2"]:
        pets = key_Word[int(pets) - 1]
        query = "UPDATE seeker SET pets = '"+pets + \
            "' WHERE telegram_id ="+str(update.message.from_user.id)
        cur.execute(query)
        conn.commit()
        if pets == "Yes":
            update.message.reply_text(
                "How many pets, what pets?...(free text)"
            )
            return "seeker_pets_type"
        else:
            reply_keyboard = [[1, 2]]
            update.message.reply_text(
                "Do you smoke? \n 1. Yes \n 2. No",
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
            )

            return "seeker_smoke"
    else:
        update.message.reply_text(
            'Invalid Input.')
        return 'seeker_pets'
    
def seeker_pets_type(update, context):
    pets_type = str(update.message.text)
    query = "UPDATE seeker SET pets_type = '"+pets_type + \
        "' WHERE telegram_id ="+str(update.message.from_user.id)
    cur.execute(query)
    conn.commit()
    reply_keyboard = [[1, 2]]
    update.message.reply_text(
        "Do you smoke? \n 1. Yes \n 2. No",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return "seeker_smoke"
def seeker_smoke(update, context):
    smoke = str(update.message.text)
    key_Word = ["Yes", "No"]
    if smoke in [1, 2, "1", "2"]:
        smoke = key_Word[int(smoke) - 1]
        query = "UPDATE seeker SET smoke = '"+smoke + \
            "' WHERE telegram_id ="+str(update.message.from_user.id)
        cur.execute(query)
        conn.commit()
        
        update.message.reply_text(
            "Enter your lower rent", reply_markup=ReplyKeyboardRemove()
        )
        return "seeker_lower_rent"
    else:
        update.message.reply_text(
            'Invalid Input.')
        return 'seeker_smoke'

def seeker_lower_rent(update, context):
    lower_rent = str(update.message.text)

    try:
        lower_rent = str(update.message.text)

        lower_rent = int(lower_rent)
        update.message.reply_text(
            "Enter your higher rent", reply_markup=ReplyKeyboardRemove()
        )
        return "seeker_higher_rent"
    except:
        update.message.reply_text(
            "Enter your lower rent", reply_markup=ReplyKeyboardRemove()
        )
        return "seeker_lower_rent"


def seeker_higher_rent(update, context):
    higher_rent = str(update.message.text)

    try:
        higher_rent = str(update.message.text)

        higher_rent = int(higher_rent)
        query = (
            "UPDATE seeker SET high_rent = '"
            + str(higher_rent)
            + "' WHERE telegram_id ="
            + str(update.message.from_user.id)
        )
        cur.execute(query)
        conn.commit()

        update.message.reply_text(
            "Enter Your Staying Duration(Ex: DD/MM/YYYY - DD/MM/YYYY)",
            reply_markup=ReplyKeyboardRemove(),
        )

        return "seeker_start_date"

    except:
        update.message.reply_text(
            "Enter your higher rent", reply_markup=ReplyKeyboardRemove()
        )
        return "seeker_higher_rent"


def seeker_start_date(update, context):
    start_date = str(update.message.text)
    try:
        if date_format_check(start_date):
            query = (
                "UPDATE seeker SET startdate = '"
                + str(start_date.split("-")[0].strip())
                + "' WHERE telegram_id ="
                + str(update.message.from_user.id)
            )

            cur.execute(query)
            conn.commit()
            query = (
                "UPDATE seeker SET end_date = '"
                + str(start_date.split("-")[1].strip())
                + "' WHERE telegram_id ="
                + str(update.message.from_user.id)
            )

            cur.execute(query)
            conn.commit()
            update.message.reply_text(
                "Enter your phone number", reply_markup=ReplyKeyboardRemove()
            )
            return "phone_number"
        else:
            update.message.reply_text(
                "Incorrect format, should be (DD/MM/YYYY - DD/MM/YYYY)",
                reply_markup=ReplyKeyboardRemove(),
            )
            return "seeker_start_date"

    except:
        update.message.reply_text(
            "Incorrect format, should be (DD/MM/YYYY - DD/MM/YYYY)",
            reply_markup=ReplyKeyboardRemove(),
        )
        return "seeker_start_date"


def seeker_end_date(update, context):
    end_date = str(update.message.text)
    try:
        if date_format_check(end_date):
            query = (
                "UPDATE seeker SET end_date = '"
                + str(end_date)
                + "' WHERE telegram_id ="
                + str(update.message.from_user.id)
            )

            cur.execute(query)
            conn.commit()
            update.message.reply_text(
                "Enter your phone number", reply_markup=ReplyKeyboardRemove()
            )
            return "seeker_phone_number"
        else:
            update.message.reply_text(
                "Incorrect data format, should be DD/MM/YYYY",
                reply_markup=ReplyKeyboardRemove(),
            )
            return "seeker_end_date"
    except:
        update.message.reply_text(
            "Incorrect data format, should be DD/MM/YYYY",
            reply_markup=ReplyKeyboardRemove(),
        )
        return "seeker_end_date"



def seeker_phone_number(update, context):
    phone_number = str(update.message.text)
    if global_phone_number_validation(phone_number):
        query = (
            "UPDATE seeker SET mobile = '"
            + str(phone_number)
            + "' WHERE telegram_id ="
            + str(update.message.from_user.id)
        )

        cur.execute(query)
        conn.commit()
        update.message.reply_text(
            "Enter your email", reply_markup=ReplyKeyboardRemove()
        )
        return "seeker_email"
    else:
        update.message.reply_text(
            'Incorrect phone number format, should be +44XXXXXXXXXX', reply_markup=ReplyKeyboardRemove()
        )
        return "seeker_phone_number"
    
def seeker_email(update, context):
    email = str(update.message.text)
    if email_validation(email):
        query = (
            "UPDATE seeker SET email = '"
            + str(email)
            + "' WHERE telegram_id ="
            + str(update.message.from_user.id)
        )

        cur.execute(query)
        conn.commit()
        update.message.reply_text(
            "Enter number of people required ", reply_markup=ReplyKeyboardRemove()
        )
        return "seeker_people"
    else:
        update.message.reply_text(
            "Incorrect email format"
        )
        return "seeker_email"


def seeker_people(update, context):
    people = str(update.message.text)
    query = (
        "UPDATE seeker SET people = '"
        + str(people)
        + "' WHERE telegram_id ="
        + str(update.message.from_user.id)
    )

    cur.execute(query)
    conn.commit()
    update.message.reply_text(
        "Your Data Enter Successfully", reply_markup=ReplyKeyboardRemove())
    update.message.reply_text(
        'Enter /start to go back to main menu', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END
