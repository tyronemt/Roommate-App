from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def base():
    return render_template('home.html')


@app.route('/login', methods = ["POST", "GET"])
def login():
    global current_user
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
    return render_template('login.html')






if __name__ == "__main__":
    app.run()
#     a = Event("a", "d" , "01122000")
#     b = Event("a", "d" , "01122000")

#     print(a>b)
