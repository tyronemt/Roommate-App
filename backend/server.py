from flask import Flask, render_template, request, redirect, url_for, jsonify
import re
import helper
import db

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
            code = helper.send_verification(current_phone_number)
            if code == None:
                return render_template('home.html', error_message = "Invalid Phone Number")
            else:
                return redirect(url_for('verify'))
        
    return render_template('home.html')


@app.route('/verify', methods = ["POST", "GET"])
def verify():
    if request.method == 'POST':
        verify = request.form.get('verify', None)
        if verify == code:
            if db.check_user(current_phone_number):
                return redirect(url_for('main'))
            else:
                return redirect(url_for('new'))
        else:
            return render_template('verify.html', error_message = "Incorrect Verification Code")
    return render_template('verify.html')


@app.route('/new', methods = ["POST", "GET"])
def new():
    if request.method == 'POST':
        name = request.form.get('name', None)
        birthday = request.form.get('birthday', None)
        if helper.check_birthday(birthday):
            return render_template("new.html", error_message = "Invalid Birthday" )
        else:
            db.create_user(current_phone_number, name, birthday)
            return redirect(url_for("main"))
    return render_template('new.html')

@app.route('/main', methods = ["POST", "GET"])
def main():
    result = db.check_member(current_phone_number)
    if result:
        return redirect(url_for("group"))
    return render_template('main.html')

@app.route('/create', methods = ["POST", "GET"])
def create():
    if request.method == 'POST':
        name = request.form.get('name', None)
        code = helper.random_passcode()
        db.create_group(current_phone_number, name, code)
        return redirect(url_for("group"))
    return render_template('create.html')

@app.route('/join', methods = ["POST", "GET"])
def join():
    if request.method == 'POST':
        code = request.form.get('code', None)
        result = db.add_member(current_phone_number, code)
        if result:
            return redirect(url_for("group"))
        else:
            return render_template('join.html', error_message = "Error Joining")
    return render_template('join.html')

@app.route('/group', methods = ["POST", "GET"])
def group():
    events = db.get_events(current_phone_number)
    birthdays =db.get_birthdays(current_phone_number)
    return render_template('group.html')

if __name__ == "__main__":
    app.run(debug=True)
