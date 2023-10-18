from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

def setup_database():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Unsafe SQL query (Vulnerable to SQL Injection)
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM users WHERE username='{username}' AND password='{password}'")
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return "Logged in successfully (But beware, this is insecure!)"
        else:
            return "Invalid credentials"
        
    return render_template('index.html')

if __name__ == "__main__":
    setup_database()
    app.run(debug=True)
