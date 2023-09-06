import pickledb 
from functions.getList import *
from functions.utils import *
from telethon.sync import TelegramClient
from telethon.tl.functions.contacts import AddContactRequest

with open('config.json') as f:
   data = json.load(f)

api_id = data["api_id"] #6046922
api_hash = data["api_hash"] #'dfcd845bf7601eb3d7a2efe8da216bbd'
phone_number = data["phone_number"]
session_name = 'session_name'





db_days = pickledb.load('./database/days.db',True) 
db_balance = pickledb.load('./database/balance.db',True) 
db_incorrect = pickledb.load('./database/incorrect.db',True) 


def task():
    print('- Check Task Started')
    check_and_update()
    for day in get_expired_days():
        if(db_days.get(day['user']) == False and db_balance.get(day['user']) == False and db_incorrect.get(day['user']) == False):
            time.sleep(0.5) 
            try:      
                
                send_message(int(day['user']),day['email'])
                db_days.set(day['user'],{'sent':True,'days':day['days']})
                print('New day limit detected : '+ day['user'])
            except:
                db_incorrect.set(day['user'],True)
                print('Error : Can\'t send message to '+day['user']+" | DAYS | "+str(day["days"])+" DAYS TO EXPIRE")
                pass

    for balance in get_expired_balance():
        if(db_balance.get(balance['user']) == False and db_days.get(balance['user']) == False and db_incorrect.get(balance['user']) == False):
            time.sleep(0.5) 
            try:
          
                send_message(int(balance['user']),balance['email'])

                db_balance.set(balance['user'],{'sent':True,'bal':balance['usage']})

                print('New day balance detected : '+ balance['user'])
            except:



                db_incorrect.set(balance['user'],True)
                print('Error : Can\'t send message to '+balance['user']+" | BALANCE | "+str(100 - balance["usage"])+"% TO EXPIRE")
                pass

def send_message(userid,name):
    with TelegramClient(session_name, api_id, api_hash) as client:
        user = client.get_entity(userid)
       
        first_name = user.first_name
        result = client(AddContactRequest(
            id=userid,
            first_name=str(first_name),
            last_name='.',
            phone=str(userid)  
        ))
        if result:
            print(f'User with ID {userid} added to your contacts.')
        else:
            print(f'Failed to add user with ID {userid} to your contacts.')
            

        user_entity = client.get_input_entity(userid)
        message = """
کاربر """+str(name)+""" 

⏳ تایم یا حجم اکانت شما در حال پايان است.
📲جهت تمدید اقدام کنید.

 جهت شماره کارت برای خرید یا تمدید پیام دهید شماره کارت بدیم 🫡

🫡 برای تمدید یا لغو سرویس سریعا پاسخ دهید ،در غیر اینصورت سرویس شما خاموش خواهد‌ شد.


✅مدت زمان تمدید اکانت 24 ساعت میباشد در غیر اینصورت باید اکانت غیرفعال می شود عزیزان 🫡

☆ پشتیبانی v2rayBG☆
"""

        client.send_message(user_entity,message)

def check_and_update():

    for balance in all_balance():
        if(db_balance.exists(balance['user'])):
            if(int(100 - balance['usage']) > int(100 - db_balance.get(balance['user'])['bal'])):
                db_balance.drem(balance['user'])


    for day in all_days():
        if(db_days.exists(day['user'])):
            if(int(day['days']) > int(db_days.get(day['user'])['days'])):
                db_days.drem(day['user'])




setInterval(1*60,task)