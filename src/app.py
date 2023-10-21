'''
Esam Jaafar
201751810
2023/10/18

'''


from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)


def setup_database():
    # Connects to an SQLite database named database.db. If the file doesn't exist, it will be created.
    conn = sqlite3.connect('database.db')
    #  Creates a cursor object. You use this object to execute SQL commands.
    cursor = conn.cursor()

    # Executes an SQL command to create a table called users. The table has three columns: id, username, and password.
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)')
    # id: Auto-incrementing primary key.
    sample_users = [
        ('Ali', 'password1'),
        ('Ahammed', 'password2'),
        ('Mohammed', 'password3'),
        ('esam', 'password4'),
        ('empty', '')  # User with an empty password
    ]

    # Inserts these sample users into the users table
    cursor.executemany(
        'INSERT INTO users (username, password) VALUES (?, ?)', sample_users)

    # Making sure that all changes are saved
    conn.commit()

    #  Closes the database connection
    conn.close()


# Call setup_database function before running the app
setup_database()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # # Debugging lines to print the SQL query
        # sql_query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        # print("Executing SQL query:", sql_query)

        # Unsafe SQL query (Vulnerable to SQL Injection)
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT * FROM users WHERE username='{username}' AND password='{password}'")

        # fetches one record that matches the criteria (Username & Password).
        result = cursor.fetchone()

        # # Debugging line to print the result
        # print("Query result:", result)
        conn.close()

        if result:
            return "Logged in successfully"
        else:
            return "Invalid credentials"

    return render_template('index.html')


if __name__ == "__main__":
    setup_database()
    app.run(debug=True)
