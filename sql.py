from flask import Flask, request
import sqlite3

app = Flask(__name__)

# Connect to an in-memory SQLite database
conn = sqlite3.connect(':memory:', check_same_thread=False)
cursor = conn.cursor()

# Create a simple users table
cursor.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')

# Insert some dummy data
cursor.execute("INSERT INTO users (username, password) VALUES ('alice', 'password123')")
cursor.execute("INSERT INTO users (username, password) VALUES ('bob', 'qwerty')")

conn.commit()

# Vulnerable login route
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    # Vulnerable SQL query (concatenates user input)
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)
    user = cursor.fetchone()
    
    if user:
        return f"Welcome {username}!"
    else:
        return "Login failed!"

if __name__ == '__main__':
    app.run(debug=True)