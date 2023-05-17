
# from poster import email_validation, global_phone_number_validation
from connection import cur
from connection import conn , global_phone_number_validation , email_validation
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackQueryHandler

def update_type(update, context):
    poster_type = str(update.message.text)
    print(poster_type)
    checker_keyword = ['Email', 'Mobile', 'End Date',
                       'Start Date', 'City', 'Address', 'People', 'Area']
    try:
        query = f"select * from seeker where telegram_id = {update.message.from_user.id} "
        cur.execute(query)

        types = cur.fetchone()
    except Exception as e:
        print(e)
        print('error')
        types = None
    if types != '' and types != None and types != 'None' and types != 'none':
        if poster_type in [1,2,3,4,5,6,7,8,'1','2','3','4','5','6','7','8']:
            poster_type = checker_keyword[int(poster_type)-1]
            print(poster_type)
            if poster_type == 'Email':

                # reply email from database based on telegram id
                cur.execute(
                    f"select email from seeker where telegram_id = {update.message.from_user.id} ")
                email = cur.fetchone()
                update.message.reply_text(
                    'Your email is '+str(email[0]),
                )
                update.message.reply_text(
                    'Please enter your new email',
                    reply_markup=ReplyKeyboardRemove()
                )

                return "update_email"
            elif poster_type == 'Mobile':

                # reply mobile from database based on telegram id
                cur.execute(
                    f"select mobile from seeker where telegram_id = {update.message.from_user.id} ")
                mobile = cur.fetchone()
                update.message.reply_text(
                    'Your mobile is '+str(mobile[0]),
                )
                update.message.reply_text(
                    'Please enter your new mobile',
                    reply_markup=ReplyKeyboardRemove()
                )

                return "update_mobile"
            elif poster_type == 'End Date':
                # reply end date from database based on telegram id
                cur.execute(
                    f"select end_date from seeker where telegram_id = {update.message.from_user.id} ")
                end_date = cur.fetchone()
                update.message.reply_text(
                    'Your Available end date is '+str(end_date[0]),
                )
                update.message.reply_text(
                    'Please enter your new aviable end date',
                    reply_markup=ReplyKeyboardRemove()
                )

                return "update_end_date"
            elif poster_type == 'Start Date':
                # reply start date from database based on telegram id
                cur.execute(
                    f"select start_date from seeker where telegram_id = {update.message.from_user.id} ")
                start_date = cur.fetchone()
                update.message.reply_text(
                    'Your aviable start date is '+str(start_date[0]),
                )
                update.message.reply_text(
                    'Please enter your new aviable start date',
                    reply_markup=ReplyKeyboardRemove()
                )

                return "update_start_date"
            elif poster_type == 'City':
                # reply city from database based on telegram id
                cur.execute(
                    f"select city from seeker where telegram_id = {update.message.from_user.id} ")
                city = cur.fetchone()
                update.message.reply_text(
                    'Your city is '+str(city[0]),
                )
                reply_keyboard = [[1, 2], [3, 4], [5]]
                update.message.reply_text(
                    'Please select your city( Type the number or click on the button): \n 1. Munich \n 2. Berlin \n 3. Frankfurt \n 4. Dusseldorf \n 5. Hamburg',
                    reply_markup=(ReplyKeyboardMarkup(
                        reply_keyboard, one_time_keyboard=True)),
                )

                return "update_city"
            elif poster_type == 'Address':
                # reply address from database based on telegram id
                cur.execute(
                    f"select address from seeker where telegram_id = {update.message.from_user.id} ")
                address = cur.fetchone()
                update.message.reply_text(
                    'Your address is '+str(address[0]),
                )
                update.message.reply_text(
                    'Please enter your new address',
                    reply_markup=ReplyKeyboardRemove()
                )

                return "update_address"
            elif poster_type == 'People':
                # reply people from database based on telegram id
                cur.execute(
                    f"select people from seeker where telegram_id = {update.message.from_user.id} ")
                people = cur.fetchone()
                update.message.reply_text(
                    'Previously ,Your are looking for house/flat for '+str(people[0])+' people',
                )
                update.message.reply_text(
                    'Please enter your updated number of people',
                    reply_markup=ReplyKeyboardRemove()
                )

                return "update_people"
            elif poster_type == 'Area':
                # reply area from database based on telegram id
                cur.execute(
                    f"select area from seeker where telegram_id = {update.message.from_user.id} ")
                area = cur.fetchone()
                update.message.reply_text(
                    'Previously,Your are looking for house/flat with '+str(area[0])+' square meters',
                )
                update.message.reply_text(
                    'Please enter your new area',
                    reply_markup=ReplyKeyboardRemove()
                )

                return "update_area"
            else:
                # return invalid input
                update.message.reply_text(
                    'Invalid input',
                )
                return "update_type"
        else:
            # return invalid input
            update.message.reply_text(
                'Invalid input',
            )
            return "update_type"
    else:
        print('No data found')
        update.message.reply_text(
            'No data found',
        )
        update.message.reply_text(
            'Please enter data first', reply_markup=ReplyKeyboardRemove()
        )
        update.message.reply_text(
        'Start a new conversation by typing /start',
        reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END

def update_email(update, context):
    email = str(update.message.text)
    if email_validation(email):
        query = "UPDATE seeker SET email = '"+email + \
            "' WHERE telegram_id ="+str(update.message.from_user.id)
        print(query)
        cur.execute(query)
        conn.commit()
        update.message.reply_text(
            'Your email is updated',
            reply_markup=ReplyKeyboardRemove()
        )
        update.message.reply_text(
            'Start a new conversation by typing /start',
            reply_markup=ReplyKeyboardRemove())
            
        return ConversationHandler.END
    else:

        update.message.reply_text(
            'Incorrect email format',
            reply_markup=ReplyKeyboardRemove()
        )
        update.message.reply_text(
            'Please enter your new email',

            reply_markup=ReplyKeyboardRemove()
        )
        return "update_email"


def update_mobile(update, context):
    mobile = str(update.message.text)
    if global_phone_number_validation(mobile):
        query = "UPDATE seeker SET mobile = '"+mobile + \
            "' WHERE telegram_id ="+str(update.message.from_user.id)
        print(query)
        cur.execute(query)
        conn.commit()
        update.message.reply_text(
            'Your mobile number is updated',
            reply_markup=ReplyKeyboardRemove()
        )
        update.message.reply_text(
            'Start a new conversation by typing /start',
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END
    else:
        update.message.reply_text(
            'Incorrect phone number format, should be +44XXXXXXXXXX',
            reply_markup=ReplyKeyboardRemove()
        )
        update.message.reply_text(
            'Please enter your new mobile number',
            reply_markup=ReplyKeyboardRemove()
        )
        return "update_mobile"


def update_end_date(update, context):
    end_date = str(update.message.text)
    query = "UPDATE seeker SET end_date = '"+end_date + \
        "' WHERE telegram_id ="+str(update.message.from_user.id)
    print(query)
    cur.execute(query)
    conn.commit()
    update.message.reply_text(
        'Your aviable end date is updated',
        reply_markup=ReplyKeyboardRemove()
    )

    update.message.reply_text(
        'Start a new conversation by typing /start',
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


def update_start_date(update, context):
    start_date = str(update.message.text)
    query = "UPDATE seeker SET start_date = '"+start_date + \
        "' WHERE telegram_id ="+str(update.message.from_user.id)
    print(query)
    cur.execute(query)
    conn.commit()
    update.message.reply_text(
        'Your aviable start date is updated',
        reply_markup=ReplyKeyboardRemove()
    )
    update.message.reply_text(
        'Start a new conversation by typing /start',
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


def update_city(update, context):
    city = str(update.message.text)
    query = "UPDATE seeker SET city = '"+city + \
        "' WHERE telegram_id ="+str(update.message.from_user.id)
    print(query)
    cur.execute(query)
    conn.commit()
    update.message.reply_text(
        'Your city is updated',
        reply_markup=ReplyKeyboardRemove()
    )
    update.message.reply_text(
        'Start a new conversation by typing /start',
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


def update_address(update, context):
    address = str(update.message.text)
    query = "UPDATE seeker SET address = '"+address + \
        "' WHERE telegram_id ="+str(update.message.from_user.id)
    print(query)
    cur.execute(query)
    conn.commit()
    update.message.reply_text(
        'Your address is updated',
        reply_markup=ReplyKeyboardRemove()
    )

    update.message.reply_text(
        'Start a new conversation by typing /start',
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


def update_people(update, context):
    people = str(update.message.text)
    query = "UPDATE seeker SET people = '"+people + \
        "' WHERE telegram_id ="+str(update.message.from_user.id)
    print(query)
    cur.execute(query)
    conn.commit()
    update.message.reply_text(
        ' Number of people is updated',
        reply_markup=ReplyKeyboardRemove()
    )
    update.message.reply_text(
        'Start a new conversation by typing /start',
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

def update_area(update, context):
    area = str(update.message.text)
    query = "UPDATE seeker SET area = '"+area + \
        "' WHERE telegram_id ="+str(update.message.from_user.id)
    print(query)
    cur.execute(query)
    conn.commit()
    update.message.reply_text(
        ' Area is updated',
        reply_markup=ReplyKeyboardRemove()
    )
    update.message.reply_text(
        'Start a new conversation by typing /start',
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

