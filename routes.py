from flask import Flask, render_template, request, session, flash, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = "super secret key"

'''home page'''
@app.route('/')
def home():
    username = session.get('username')
    if username:
        flash('Hi {}, welcome to Toast Website!'.format(session.get('username')))
        flash('haha, flash again')
    return render_template('home.html', username = username)

@app.route('/signup')
def signup_get():
    return render_template('signup.html')

'''sign up'''
@app.route('/signup', methods = ['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']
    connection = sqlite3.connect('toast.db')
    cursor = connection.cursor()
    #Mike Rhodes - Stack overflow :skull:
    cursor.execute("SELECT username FROM users WHERE username = '{}'".format(username))
    key = cursor.fetchone()
    if key is not None:
        error = 'this username is taken!'
        return render_template('signup.html', error = error)
    else:
        cursor.execute("INSERT INTO users(username, password) VALUES('{}', '{}')".format(username, password))
        connection.commit()
        session['username'] = username
        return(redirect(url_for('home')))

@app.route('/login')
def test():
    return render_template('login.html')

@app.route('/login', methods = ['POST'])
def login():
        password = request.form['password'] 
        username = request.form['username']
        connection = sqlite3.connect('toast.db')
        cursor = connection.cursor()
        cursor.execute("SELECT password FROM users WHERE username = '{}'".format(username))
        key = cursor.fetchone()
        connection.close()

        if key is None:
            error = 'User not found!'
            return render_template('login.html', error = error)
        if key[0] == password:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            error = 'Wrong password!'
            return render_template('login.html', error = error)

@app.route('/logout')
def logout():
    session.clear()
    return(redirect(url_for('home')))

'''shows user reviews'''
@app.route('/myreviews')
def myreviews():
    username = session.get('username')
    if not username:
        return(redirect(url_for('login')))
    else:
            connection = sqlite3.connect('toast.db')
            cursor = connection.cursor()
            cursor.execute("SELECT review FROM reviews as r JOIN users as u on r.user_id = u.id WHERE u.username = '{}'".format(username))
            reviews = cursor.fetchall()
            if len(reviews) == 0:
                return render_template('myreviews.html', error = 'No review found!')
            else:
                return render_template('myreviews.html', reviews = reviews)

'''shows all reviews'''
@app.route('/reviews')
def show_all_reviews():
    connection = sqlite3.connect('toast.db')
    cursor = connection.cursor()
    cursor.execute('SELECT toast.description, review, username FROM Reviews JOIN Toast ON reviews.toast_id = toast.id JOIN Users ON reviews.user_id = users.id')
    reviews = cursor.fetchall()
    connection.close()
    return render_template("reviews.html", reviews = reviews)

@app.route('/create-review')
def im_so_stressed():
    return "please help me"



if __name__ == "__main__":
    app.run(debug = True)