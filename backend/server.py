from flask import Flask, render_template, request, redirect, url_for, jsonify
from twilio.rest import Client
import keys
import re
import random
import math
import mysql.connector
import db


def random_passcode():
    digits = [i for i in range(0, 10)]
    random_str = ""
    for i in range(6):
        index = math.floor(random.random() * 10)
        random_str += str(digits[index])

    print(random_str)
    return random_str

def send_verification(phone_number):
    client = Client(keys.account_sid, keys.auth_token)
    code = random_passcode()
    print(phone_number)
    message = client.messages.create(
        body = code,
        from_ = keys.twilio_number,
        to = phone_number
    )
    return code
    

app = Flask(__name__)

@app.route('/', methods = ["POST", "GET"])
def base():
    if request.method == 'POST':
        phone_number = request.form.get('phone_number', None)
        if re.match("^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$", phone_number) == None:
            return render_template('home.html', error_message = "Invalid Phone Number")
        else:
            global current_phone_number, code
            current_phone_number =  "+1" + phone_number
            code = send_verification(current_phone_number)
            return redirect(url_for('verify'))
        
    return render_template('home.html')


@app.route('/verify', methods = ["POST", "GET"])
def verify():
    if request.method == 'POST':
        verify = request.form.get('verify', None)
        if verify == code:
            if db.check_user(current_phone_number):
                return redirect(url_for('returning'))
            else:
                return redirect(url_for('new'))
    return render_template('verify.html')

@app.route('/returning', methods = ["POST", "GET"])
def returning():
   
    return render_template('returning.html')

@app.route('/new', methods = ["POST", "GET"])
def new():
    
    return render_template('new.html')

if __name__ == "__main__":
    app.run(debug=True)
