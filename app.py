from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

app = Flask(__name__)

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'zubur1'
app.config['MYSQL_DB'] = 'bjflaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Init MySQL
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    username = StringField('Username', [validators.Length(min=5, max=25)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
        ])
    confirm = PasswordField('Confirm Password')

class LoginForm(Form):
    username = StringField('Username', [
        validators.DataRequired(),
        ])
    password = PasswordField('Password', [
        validators.DataRequired(),
        ])

@app.route('/logout')
def logout():
    session["logged_in"] = False
    session["username"] = None
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)

    if request.method == 'POST' and login_form.validate():
        username = login_form.username.data
        
         # Create the cursor
        with mysql.connection.cursor() as cur:

            # Insert data to DB
            cur.execute("SELECT * FROM users WHERE username = '%s'" % username)
            res = cur.fetchone()

            if res is not None:
                if sha256_crypt.verify(str(login_form.password.data), res['password']):
                    session['logged_in'] = True
                    session['username'] = username
                    flash('Welcome, %s.' % res['name'], 'success')
                else:
                    flash('Username or password are wrong', 'danger')
                    return render_template('login.html', form=login_form)
                
            else:
                flash('You are not registered. Please, register.', 'danger')

        return redirect(url_for('index'))
    else:
        return render_template('login.html', form=login_form)
        


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        # Encrypt the password
        
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create the cursor
        cur = mysql.connection.cursor()

        # Insert data to DB
        cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))

        # Commit to DB
        mysql.connection.commit()

        #Close the connection
        cur.close()

        flash('You are now registered. Please, log in.', 'success')

        return redirect(url_for('login'))
     
    else:
        return render_template('register.html', form=form)

if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True, host= '0.0.0.0')
    #app.run()
