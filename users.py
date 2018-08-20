from flask import Flask, render_template,

class User():
    def is_authenticated(self):
        username = login_form.username.data
        
         # Create the cursor
        with mysql.connection.cursor() as cur:

            # Insert data to DB
            cur.execute("SELECT * FROM users WHERE username = '%s'" % username)
            res = cur.fetchone()

            if res is not None:
                if sha256_crypt.verify(str(login_form.password.data), res['password']):
                    flash('Welcome, %s.' % res['name'], 'success')
                else:
                    flash('Username or password are wrong', 'danger')
                    return render_template('login.html', form=login_form)
                
            else:
                flash('You are not registered. Please, register.', 'danger')
    def is_active(self):
        pass
    def is_anonymous(self):
        pass
    def get_id(self, user_id):
        pass
