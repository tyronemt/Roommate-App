import datetime
import keys
from twilio.rest import Client
import random
import math

def check_date(date):
    m = int(date[0:2])
    d = int(date[2:4])
    y = int(date[4:8])

    correctDate = None
    try:
        newDate = datetime.datetime(y,m,d)
        print("valid date")
        correctDate = False
    except ValueError:
        correctDate = True
    
    if len(date) > 8:
        correctDate = True
    return correctDate

def send_verification(phone_number):
    client = Client(keys.account_sid, keys.auth_token)
    code = random_passcode()
    print(phone_number)
    try:
        message = client.messages.create(
            body = code,
            from_ = keys.twilio_number,
            to = phone_number
        )
        return code
    except:
        return None


def random_passcode():
    digits = [i for i in range(0, 10)]
    random_str = ""
    for i in range(6):
        index = math.floor(random.random() * 10)
        random_str += str(digits[index])

    print(random_str)
    return random_str