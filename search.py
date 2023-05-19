from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler
from connection import cur , conn
from datetime import datetime, timedelta
# create a table for search filter
cur.execute('''CREATE TABLE IF NOT EXISTS search(
    id serial PRIMARY KEY,
    telegram_id INTEGER,
    city VARCHAR(255),
    address VARCHAR(255),
    area VARCHAR(255),
    apartment VARCHAR(255),
    rent VARCHAR(255),
    startdate VARCHAR(255),
    end_date VARCHAR(255),
    people VARCHAR(255),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)''')
conn.commit()



def search_type(update, context):
    data = str(update.message.text)
    if '1' in data:
        cur.execute(
            f"select * from seeker where telegram_id = {update.message.from_user.id} ")
        data = cur.fetchone()
        if data:
           
            update.message.reply_text(
                'You are '+ str(data[2]) + ' and looking for a place  in '+str(data[3])
                # +' for '+str(data[12])+' people'+ ' with rent '+str(data[7])+' and start date '+str(data[8])+' and end date '+str(data[9])
                , 
                reply_markup=ReplyKeyboardRemove()
            )

            update.message.reply_text(
                'Here are some options for you',
            )
            cur.execute(f"select * from poster where city = '{data[3]}'")
            data = cur.fetchall()
            if data:
                for i in data:
                    update.message.reply_text('''
                    ############ Aviable Option ##############
                        City : '''+str(i[1])+'''
                        Address : '''+str(i[8])+'''
                        Rent : '''+str(i[11])+'''
                        Posting Date : '''+str(i[9])+'''
                        Vacant From : '''+str(i[10])+'''
                    
                        ''')
                update.message.reply_text(
                    'Start a new conversation by typing /start',
                    reply_markup=ReplyKeyboardRemove()
                )
                return ConversationHandler.END
            else:
                update.message.reply_text(
                    'No data found',
                )
     
                update.message.reply_text(
                    'Update your profile to get better result or search manually', reply_markup=ReplyKeyboardRemove()
                )
                update.message.reply_text(
                    'Start a new conversation by typing /start',
                    reply_markup=ReplyKeyboardRemove()
                )
                return ConversationHandler.END
        else:
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
    elif "2" in data:
       
        update.message.reply_text('For Manual Serach Please entry data as per fileds, if you want to skip any field please type "Skip" or choose from keyboard button',reply_markup=ReplyKeyboardRemove())
        
        reply_keyboard = [[1, 2, 3, 4, 5]]
        update.message.reply_text(
            'Please select your City (Type or Choose from keyboard): \n 1. Munich \n 2. Berlin \n 3. Frankfurt \n 4. Dusseldorf \n 5. Hamburg',
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True)
        )
        query = f"insert into search (telegram_id) values ({update.message.from_user.id})"
        cur.execute(query)
        conn.commit()

        return "next_option"
    else:
        update.message.reply_text(
            'Invalid input',
        )
        return "search_type"

def next_option(update, context):
    data = str(update.message.text)
    data_list = ['Munich', 'Berlin', 'Frankfurt', 'Dusseldorf', 'Hamburg','Skip']
    if data in [1, 2, 3, 4, 5,'1','2','3','4','5']:
        data = data_list[int(data)-1]
        query = f"update search set city = '{data}' where telegram_id = {update.message.from_user.id}"
        cur.execute(query)
        conn.commit()
        update.message.reply_text(
            'Please enter Area(ex:  Street Name or Skip)',
            reply_markup=ReplyKeyboardRemove()
        )
        return "next_option_area"
    elif data == "Skip" or data == "skip":
        update.message.reply_text(
            'You can not skip this field',
        )
        return "next_option"
    else:
        update.message.reply_text(
            'Invalid input,Select from options.',
        )
        return "next_option"
        


def next_option_area(update, context):
    data = str(update.message.text)
    data = data.capitalize()
    query = f"update search set area = '{data}' where telegram_id = {update.message.from_user.id}"
    cur.execute(query)
    conn.commit()


    update.message.reply_text(
        'Please enter rent(ex: 1000  or Skip)',
        reply_markup=ReplyKeyboardRemove()
    )
    return "next_option_rent"

def next_option_rent(update, context):
    data = str(update.message.text)
    data = data.capitalize()
    query = f"update search set rent = '{data}' where telegram_id = {update.message.from_user.id}"
    cur.execute(query)
    conn.commit()
    update.message.reply_text(
        'Please enter number of people(ex: 2  or Skip)',
        reply_markup=ReplyKeyboardRemove()
    )
    return "next_option_people"

def next_option_people(update, context):
    data = str(update.message.text)
    data = data.capitalize()
    query = f"update search set people = '{data}' where telegram_id = {update.message.from_user.id}"
    cur.execute(query)
    conn.commit()
    
    update.message.reply_text(
        'Please enter start date(ex: mm/dd/yyyy  or Skip)',
        reply_markup=ReplyKeyboardRemove()
    )
    return "next_option_start_date"



def date_format_check(date_text):
    try:
        datetime.strptime(date_text, '%m/%d/%Y')
    except ValueError:
        return False
    else:
        return True
    
def next_option_start_date(update, context):
    data = str(update.message.text)
    data = data.capitalize()
    if data != "Skip":
        if date_format_check(data):
            query = f"update search set startdate = '{data}' where telegram_id = {update.message.from_user.id}"
            cur.execute(query)
            conn.commit()
        else:
            update.message.reply_text(
                'Please enter valid date format(ex: mm/dd/yyyy  or Skip)',
                reply_markup=ReplyKeyboardRemove()
            )
            return "next_option_start_date"
    else:
        query = f"update search set startdate = '{data}' where telegram_id = {update.message.from_user.id}"
        cur.execute(query)
        conn.commit()
    update.message.reply_text(
        'Please enter end date(ex: mm/dd/yyyy  or Skip)',
        reply_markup=ReplyKeyboardRemove()
    )
    return "next_option_end_date"

def next_option_end_date(update, context):
    data = str(update.message.text)
    data = data.capitalize()
    if data != "Skip":
        if date_format_check(data):
            query = f"update search set end_date = '{data}' where telegram_id = {update.message.from_user.id}"
            cur.execute(query)
            conn.commit()
        else:
            update.message.reply_text(
                'Please enter valid date format(ex: mm/dd/yyyy  or Skip)',
                reply_markup=ReplyKeyboardRemove()
            )
            return "next_option_end_date"
    else:
        query = f"update search set end_date = '{data}' where telegram_id = {update.message.from_user.id}"
        cur.execute(query)
        conn.commit()
    update.message.reply_text(
        'Please wait for the result',
        reply_markup=ReplyKeyboardRemove()
    )
    query = f"select * from search where telegram_id = {update.message.from_user.id}"
    cur.execute(query)
    result = cur.fetchone()
    rent = result[5] if result[5] != "Skip" else ""
    start_date = result[6] if result[6] != "Skip" else ""
    end_date = result[7] if result[7] != "Skip" else ""
    city = result[2] if result[2] != "Skip" else ""
    address = result[3] if result[3] != "Skip" else ""
    area = result[4] if result[4] != "Skip" else ""
    query = f"select * from poster where "
    if city !="" and city != None and city !="None" and city != "none" and city != "Skip":
        query=query+"city ='"+city+"'"
    if rent !="" and rent != None and rent !="None" and rent != "none"and rent != "Skip":
        query=query+"and (rent<='"+rent+"'"
    if area !="" and area != None and area !="None" and area != "none"and area != "Skip":
        query=query+" or area='"+area+"'"
    if start_date !="" and start_date != None and start_date !="None" and start_date != "none"and start_date != "Skip":
        query=query+" or start_date='"+start_date+"'"
    if end_date !="" and end_date != None and end_date !="None" and end_date != "none"and end_date != "Skip":
        query=query+" or end_date='"+end_date+"' )"
    query = query + " and created_at >='" + str((datetime.now() - timedelta(days=30))) + "'"
    cur.execute(query)
    result = cur.fetchall()
    if len(result) == 0:
        update.message.reply_text(
            'No result found',
            reply_markup=ReplyKeyboardRemove()
        )
        update.message.reply_text(
            'Please enter /start to start again',
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END
    else:
        for i in result:
            
            update.message.reply_text(
                f'City: {i[1]}\n Type: {i[5]}\n Description: {i[7]}\n Address: {i[8]}\n Area: {i[11]}\n Warmrent: {i[12]}\n Mobile: {i[14]}\n Email: {i[15]}\n User_type: {i[24]}\n Rent: {i[25]}\n High_rent: {i[26]}\n Anmeldung: {i[27]}\n Start_date: {i[28]}\n End_date: {i[29]}\n People: {i[30]}\n Created_at: {i[31]}'
            )

        update.message.reply_text(
            'For more result or other query please contact admin',
            reply_markup=ReplyKeyboardRemove()
        )

        update.message.reply_text(
            'Please enter /start to start again',
            reply_markup=ReplyKeyboardRemove()
        )

        return ConversationHandler.END
    

def manual_search(update, context):
    data = str(update.message.text)
    if "City" in data:
        reply_keyboard = [['Munich', 'Berlin'], [
            'Frankfurt', 'Dusseldorf'], ['Hamburg','Skip']]
        update.message.reply_text(
            'Please select your City from keyboard button',
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True)
        )
        return "manual_search_city"
    elif "Type" in data:
        reply_keyboard = [['Students', 'Profesional', 'Academics']]
        update.message.reply_text(
            'Please select your Type from keyboard button',
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True)
        )
        return "manual_search_type"
    elif "Rent" in data:
        # give option to select city
        reply_keyboard = [['100', '200', '300'], [
            '400', '500', '600'], ['700', '800', '900']]
        update.message.reply_text(
            'Please select your Rent from keyboard button',
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True)
        )
        return "manual_search_rent"
    else:
        # return invalid input
        update.message.reply_text(
            'Invalid input',
        )
        return "manual_search"


def manual_search_city(update, context):
    city = str(update.message.text)
    cur.execute(f"select * from poster where city = '{city}'")
    data = cur.fetchall()
    if data:
        for i in data:
            update.message.reply_text('''
            ############ Aviable Option ##############
                City : '''+str(i[1])+'''
                Address : '''+str(i[8])+'''
                Rent : '''+str(i[11])+'''
                Posting Date : '''+str(i[9])+'''
                Vacant From : '''+str(i[10])+'''
            
                ''')
        update.message.reply_text(
        'Thank you for using our service \n\n',
        reply_markup=ReplyKeyboardRemove()
        )
        update.message.reply_text(
            'Start a new conversation by typing /start',
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END
    else:
        # return no data found
        update.message.reply_text(
            'No data found',
        )
        # if no data found ask for manual search
        update.message.reply_text(
            'Do you want to search manually?',
            reply_markup=ReplyKeyboardMarkup([['Manual']])
        )
        return "search_type"
    # clear keyboard

    update.message.reply_text(
        'Thank you for using our service \n\n',
        reply_markup=ReplyKeyboardRemove()
    )
    update.message.reply_text(
        'Start a new conversation by typing /start',
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END