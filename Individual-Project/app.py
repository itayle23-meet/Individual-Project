from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {
"apiKey": "AIzaSyApp48RRy8F_j9CrPeVoG0B6P0PwEkebe4",
  "authDomain": "personal-project-97467.firebaseapp.com",
  "databaseURL": "https://personal-project-97467-default-rtdb.europe-west1.firebasedatabase.app",
  "projectId": "personal-project-97467",
  "storageBucket": "personal-project-97467.appspot.com",
  "messagingSenderId": "338614674033",
  "appId": "1:338614674033:web:680a34bc6d3adba629f1d0",
  "measurementId": "G-4HWVZTGESX" }
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database() 
#Code goes below here

@app.route('/', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = {"email": request.form['email'], "password": request.form['password']}
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(request.form['email'], request.form['password'])
        except:
            error = "Authentication failed"
            print(error)
        return redirect(url_for('index'))
    else:
        return render_template("signin.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user = {"email": request.form['email'], "password": request.form['password'], "name" : request.form['name']}
        try:
            login_session['user'] = auth.create_user_with_email_and_password(request.form['email'], request.form['password'])
            db.child("Users").child(login_session['user']['localId']).set(user)
            return redirect(url_for('index'))
        except:
            error = "Authentication failed"
    return render_template("signup.html")

@app.route('/new_review', methods=["POST"])
def new_review():
    print("new review")
    review= {"title" : request.form['title'], "text" : request.form['text'], "name" : request.form['username']}
    db.child("Reviews").push(review)
    print("redirecting")
    return redirect(url_for('index'))

@app.route('/index', methods=['GET', 'POST'])
def index():
    # if request.method == 'POST':
    #     review= {"title" : request.form['title'], "text" : request.form['text'], "name" : request.form['username']}
    #     try:
    #         login_session['reviews'] = reviews
    #         db.child("Reviews").push(reviews)
    #         reviews = db.child("Reviews").get().val()
    #         return render_template("index.html" , reviews = reviews)
    #     except:
    #         print("somthing went wrong")

    reviews = db.child("Reviews").get().val()
    print(reviews)
    return render_template("index.html", reviews = reviews)




@app.route('/logout')
def log_out():
    login_session['user'] = None
    auth.current_user = None
    return render_template('signin.html')




#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)