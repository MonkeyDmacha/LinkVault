from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('landing.html')

@app.route('/register', methods=['POST'])
def register():
    fullname = request.form.get('fullname')
    email = request.form.get('email')
    password = request.form.get('password')

    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO users (fullname, email, password) VALUES (?, ?, ?)',
                     (fullname, email, password))
        conn.commit()
    except sqlite3.IntegrityError:
        return "⚠️ Email already registered!", 400
    finally:
        conn.close()

    return redirect(url_for('dashboard'))

@app.route('/login', methods=['POST'])
def login():
    email_or_username = request.form.get('username_or_email')
    password = request.form.get('password')

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE email = ?', (email_or_username,)).fetchone()
    conn.close()

    if user and user['password'] == password:
        return redirect(url_for('dashboard'))
    return "❌ Invalid credentials", 401

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
