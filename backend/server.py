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
    return render_template('main.html')

if __name__ == "__main__":
    app.run(debug=True)
