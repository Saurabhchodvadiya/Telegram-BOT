from telegram import (
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import ConversationHandler, CallbackContext
from poster import global_phone_number_validation
from poster import date_format_check

from connection import cur, conn

postrr_Data_list = [
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
]

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
        reply_keyboard = [[1, 2, 3, 4, 5]]
        update.message.reply_text(
            "Please select your City (Type from keyboard button or click on keyboard button): \n 1. Munich \n 2. Berlin \n 3. Frankfurt \n 4. Dusseldorf \n 5. Hamburg",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
        )
        return "seeker_city_type"

    else:
        return 'Options'


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
        postrr_Data_list.insert(2, city_type)
        update.message.reply_text(
            "Please write your area in text field", reply_markup=ReplyKeyboardRemove()
        )
        return "seeker_location"
    else:
        seeker_type(update, context)


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
        reply_keyboard = [[1, 2, 3]]

        update.message.reply_text(
            "Anmeldung Required : \n 1. Yes \n 2. No \n 3. Maybe",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
        )

        return "seeker_anmeldung"
    else:
        seeker_address(update, context, 1)


def seeker_anmeldung(update, context):
    anmeldung = str(update.message.text)
    key_Word = ["Yes", "No", "Not Sure"]
    if anmeldung in [1, 2, 3, "1", "2", "3"]:
        anmeldung = key_Word[int(anmeldung) - 1]
        query = "UPDATE seeker SET anmeldung = '"+anmeldung + \
            "' WHERE telegram_id ="+str(update.message.from_user.id)
        cur.execute(query)
        conn.commit()
        update.message.reply_text(
            "Enter your lower rent", reply_markup=ReplyKeyboardRemove()
        )
        return "seeker_lower_rent"
    else:
        seeker_home_type(update, context, 1)


def seeker_lower_rent(update, context):
    lower_rent = str(update.message.text)

    try:
        lower_rent = str(update.message.text)

        lower_rent = int(lower_rent)
        update.message.reply_text(
            "Enter your higher rent", reply_markup=ReplyKeyboardRemove()
        )
        postrr_Data_list.insert(5, lower_rent)
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
        postrr_Data_list.insert(6, higher_rent)
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
            postrr_Data_list.insert(9, start_date)
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
    if global_email_validation(email):
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
