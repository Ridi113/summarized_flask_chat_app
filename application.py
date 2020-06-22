from flask import Flask, render_template, redirect, url_for
from wtform_fields import *
from models import *

from passlib.hash import pbkdf2_sha256

# Configure app
app = Flask(__name__)
app.secret_key = 'replace later'

#configure database
app.config['SQLALCHEMY_DATABASE_URI']='postgres://jayfgzkhxgprlt:8708ad5ec7c873aa3f587b152b5a9d82dbc1f4c4c041fed1939d431ca3810b30@ec2-34-193-117-204.compute-1.amazonaws.com:5432/d25lfpg5t060v5'

db = SQLAlchemy(app)

@app.route("/", methods=['GET', 'POST'])
def index():

    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data

        #Hashed password
        hashed_pswd = pbkdf2_sha256.hash(password)

        user = User(username=username, password=hashed_pswd)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template("index.html", form=reg_form)


@app.route("/login", methods=['GET', 'POST'])
def login():

    login_form = LoginForm()

    # Allow login if validation success
    if login_form.validate_on_submit():
        return "Logged in, finally!"

    return render_template("login.html", form=login_form)

if __name__ == "__main__":

    app.run(debug = True)