# https://docs.python-telegram-bot.org/en/stable/telegram.message.html
from connection import *
from datetime import datetime
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater, ConversationHandler
import pandas as pd
from seeker import *
from poster import *
from update import *
from search import *
import os
from dotenv import load_dotenv
load_dotenv()

home_typess = ""
postrr_Data_list = ["", "", "", "", "", "", "",
                    "", "", "", "", "", "", "", "", "", "", "", ""]


def start_command(update, context):
    update.message.reply_text('Type something to get started!')


def help_command(update, context):
    update.message.reply_text(
        'If you need help, you should ask for it on Google!')


def custom_command(update, context):
    update.message.reply_text(
        'This is a custom command, you can add whatever text here')


def handle_response(text: str):

    if "hello" in text:
        return 'Hello there!'

    if 'how are you' in text:
        return 'I am fine, thank you. How are you?'

    return 'Sorry, I dont understand you. Could you please rephrase?'


def handle_message(update, context):
    '''
    This function is used to handle the message from the user

    args: update, context

    '''
    message_type = update.message.chat.type
    text = str(update.message.text).lower()
    response = ''
    if message_type == 'group' and 'bot19292bot' in text:
        new_text = text.replace('@bot19292bot', '').strip()
        response = handle_response(new_text)

    if message_type == 'private':
        reply_keyboard = [['1', '2', '3', '4',]]
        update.message.reply_text(
            '''Please select your option(Type the number or click the button):\n1. Poster\n2. Seeker\n3. Update\n4. Search
            ''',
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True),

        )
        return "Options"

    update.message.reply_text(response)


def Options(update, context):
    '''
    this function is used to handle the options from the user

    args: update, context
    '''

    text = str(update.message.text)
    if '1' in text:
        update.message.reply_text('You selected Poster')
        reply_keyboard = [[1, 2],
                          [3, 4]]
        update.message.reply_text(
            'Please select your type from keyboard button\n1. current tenant\n2. agent\n3. housing co\n4. landlord',
            reply_markup=(ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True)),

        )

        cur.execute("select * from poster where telegram_id =" +
                    str(update.message.from_user.id)+"::text")

        count = cur.fetchall()
        if (len(count) < 1):

            query = "INSERT INTO poster (telegram_id) VALUES (" + \
                str(update.message.from_user.id)+")"
    
            cur.execute(query)
            conn.commit()
        return "poster_type"
    elif '2' in text:
        update.message.reply_text('You selected Seeker')
        reply_keyboard = [[1, 2], [3]]
        update.message.reply_text(
            'Please select your type from keyboard button (Type the number or click the button) : \n1. Students\n2. Profesional\n3. Academics',
            reply_markup=(ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True)),

        )
        cur.execute("select * from seeker where telegram_id =" +
                    str(update.message.from_user.id))
        count = cur.fetchall()
        if (len(count) < 1):

            query = "INSERT INTO seeker (telegram_id) VALUES (" + \
                str(update.message.from_user.id)+")"
            cur.execute(query)
            conn.commit()
        return "seeker_type"
    elif '3' in text or 'update_type' in text:
        update.message.reply_text('You selected Update')
        reply_keyboard = [[1, 2, 3, 4, 5, 6, 7, 8]]
        update.message.reply_text(
            'Please select your type from keyboard button (Type the number or click the button) : \n1. Email\n2. Mobile\n3. End Date\n4. Start Date\n5. City\n6. Address\n7. People\n8. Area',
            reply_markup=(ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True)),

        )
        return "update_type"
    elif '4' in text:
        update.message.reply_text('You selected Search')
        reply_keyboard = [[1, 2]]
        update.message.reply_text(
            'Please select your type from keyboard button (Type the number or click the button) : \n1. Based on your Data\n2. Manual',
            reply_markup=(ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True)),

        )
        return "search_type"

    else:
        return 'handle_message'







def stop(update, context):
    '''
    this function is used to stop the bot

    '''
    update.message.reply_text(
        'Bye', reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

token = os.getenv('BOT_KEY')
if __name__ == '__main__':
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher
 
    dp.add_handler(CommandHandler('stop', stop))
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', handle_message)],
        states={
            'handle_message': [MessageHandler(Filters.text, handle_message)],
            "Options": [MessageHandler(Filters.text, Options)],
            "poster_type": [MessageHandler(Filters.text, poster_type)],
            "city": [MessageHandler(Filters.text, city_type)],
            "address": [MessageHandler(Filters.text, address)],
            "location": [MessageHandler(Filters.text, location)],
            "home_type": [MessageHandler(Filters.text, home_type)],
            "lower_rent": [MessageHandler(Filters.text, lower_rent)],
            "higher_rent": [MessageHandler(Filters.text, higher_rent)],
            "flat_area": [MessageHandler(Filters.text, flat_area)],
            "shared_area": [MessageHandler(Filters.text, shared_area)],
            "start_date": [MessageHandler(Filters.text, start_date)],
            "phone_number": [MessageHandler(Filters.text, phone_number)],
            "email": [MessageHandler(Filters.text, email)],
            "people": [MessageHandler(Filters.text, people)],
            "seeker_type": [MessageHandler(Filters.text, seeker_type)],
            "seeker_home_type": [MessageHandler(Filters.text, seeker_home_type)],
            "seeker_address": [MessageHandler(Filters.text, seeker_address)],
            "seeker_location": [MessageHandler(Filters.text, seeker_location)],
            "seeker_city_type": [MessageHandler(Filters.text, seeker_city_type)],
            "seeker_lower_rent": [MessageHandler(Filters.text, seeker_lower_rent)],
            "seeker_higher_rent": [MessageHandler(Filters.text, seeker_higher_rent)],
            "seeker_start_date": [MessageHandler(Filters.text, seeker_start_date)],
            "seeker_end_date": [MessageHandler(Filters.text, seeker_end_date)],
            "seeker_phone_number": [MessageHandler(Filters.text, seeker_phone_number)],
            "seeker_email": [MessageHandler(Filters.text, seeker_email)],
            "seeker_people": [MessageHandler(Filters.text, seeker_people)],
            'User_Data': [MessageHandler(Filters.text, User_Data)],
            'update_email': [MessageHandler(Filters.text, update_email)],
            'update_people': [MessageHandler(Filters.text, update_people)],
            'update_address': [MessageHandler(Filters.text, update_address)],
            'update_city': [MessageHandler(Filters.text, update_city)],
            'update_start_date': [MessageHandler(Filters.text, update_start_date)],
            'update_end_date': [MessageHandler(Filters.text, update_end_date)],
            'update_type': [MessageHandler(Filters.text, update_type)],
            'update_mobile': [MessageHandler(Filters.text, update_mobile)],
            'search_type': [MessageHandler(Filters.text, search_type)],
            'manual_search': [MessageHandler(Filters.text, manual_search)],
            'next_option': [MessageHandler(Filters.text, next_option)],
            'next_option_area': [MessageHandler(Filters.text, next_option_area)],
            'next_option_rent': [MessageHandler(Filters.text, next_option_rent)],
            'next_option_start_date': [MessageHandler(Filters.text, next_option_start_date)],
            'next_option_end_date': [MessageHandler(Filters.text, next_option_end_date)],
            'next_option_people': [MessageHandler(Filters.text, next_option_people)],
            'manual_search_city': [MessageHandler(Filters.text, manual_search_city)],
            'upload': [MessageHandler(Filters.document, upload)],
            'seeker_anmeldung': [MessageHandler(Filters.text, seeker_anmeldung)],
            'stop': [MessageHandler(Filters.text, stop)],
            'update_area' : [MessageHandler(Filters.text, update_area)],
        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    dp.add_handler(conv_handler)
    dp.add_error_handler(error)
    updater.start_polling(1.0)
    updater.idle()
