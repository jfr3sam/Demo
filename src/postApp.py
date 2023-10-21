from flask import Flask, request, render_template
import sqlite3
import hashlib

app = Flask(__name__)


def setup_database():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)')

    sample_users = [
        ('Ali', 'password1'),
        ('Ahammed', 'password2'),
        ('Mohammed', 'password3'),
        ('esam', 'password4')
    ]

    hashed_sample_users = [(name, hashlib.sha256(
        password.encode()).hexdigest()) for name, password in sample_users]
    cursor.executemany(
        'INSERT INTO users (username, password) VALUES (?, ?)', hashed_sample_users)
    conn.commit()
    conn.close()


setup_database()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?", (username, hashed_password))
        user = cursor.fetchone()
        conn.close()

        if user:
            return "Logged in successfully"
        else:
            return "Invalid credentials"

    return render_template('index.html')


if __name__ == "__main__":
    setup_database()
    app.run(debug=True, port=5001)
