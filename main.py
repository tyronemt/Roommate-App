from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import false
import calend
import roommate

app = Flask(__name__)

current_user = None
groups = []

@app.route('/')
def base():
    return render_template('home.html')


@app.route('/login', methods = ["POST", "GET"])
def login():
    global current_user
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        result = roommate.login(username,password)
        if result[0] == True:
            current_user = roommate.login(username, password)[1]
            return redirect(url_for('calendar'))
        else:
            return render_template('login.html', error_message = result[1])
    return render_template('login.html')

@app.route('/register', methods = ["POST", "GET"])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        birthday = request.form['birthday']
        result = roommate.register(name, username, password, birthday)
        if result == True: 
            return render_template('success.html', message = "Event Created")
        else:
            return render_template('register.html', error_message = result)
    return render_template('register.html')

@app.route('/calendar', methods = ["POST", "GET"])
def calendar():
    return render_template("calendar.html", calendar = current_user.calendar.calendar)

@app.route('/create', methods = ["POST", "GET"])
def create():
    if request.method == 'POST':
        name = request.form['name']
        date = request.form['date']
        description = request.form['description']
        result = current_user.calendar.create_event(name,date,description)
        if result == True:
            return render_template('success.html', message = "Event Created")
        else:
            return render_template('create.html', error_message = result)
    return render_template("create.html")

@app.route('/group', methods = ["POST", "GET"])
def group():
    return render_template("group.html")











if __name__ == "__main__":
    roommate.register("Tyrone", "a@email.com", "a2", "01132000")

    app.run()
#     a = Event("a", "d" , "01122000")
#     b = Event("a", "d" , "01122000")

#     print(a>b)
