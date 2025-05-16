from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import sqlite3
import os
from werkzeug.utils import secure_filename
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

users = {}  # Simple in-memory user store for demo purposes
ngos = {'AP000/2045': True, '271107': True}  # Example valid NGO code numbers including test code 271107

def get_db_connection():
    conn = sqlite3.connect('stray_animals.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    conn = get_db_connection()
    reports = conn.execute('SELECT * FROM reports').fetchall()
    return render_template('index.html', reports=reports)

@app.route('/reports', methods=['GET'])
def reports():
    conn = get_db_connection()
    reports = conn.execute('SELECT * FROM reports').fetchall()
    reports_list = [dict(report) for report in reports]  # Convert to list of dicts
    return jsonify(reports_list)  # Return JSON response with images

@app.route('/view_reports')
def view_reports():
    if not session.get('username'):
        return redirect(url_for('login_page'))
    if session.get('user_type') != 'ngo':
        return "Access denied: Only NGO users can access this page.", 403
    conn = get_db_connection()
    reports = conn.execute('SELECT * FROM reports').fetchall()
    return render_template('reports.html', reports=reports)

@app.route('/submit', methods=['GET', 'POST'])
def submit_report():
    if request.method == 'GET':
        return render_template('submit_report.html')
    description = request.form.get('description')
    location = request.form.get('location')
    image = request.files.get('image')

    if not description or not location:
        return jsonify({"error": "Description and location are required."}), 400

    if image and not allowed_file(image.filename):
        return jsonify({"error": "Invalid image file type."}), 400

    conn = get_db_connection()
    app.logger.debug(f"Submitting report: {description}, {location}, {image.filename if image else 'No image'}")  # Log the submission details

    try:
        if image:
            filename = secure_filename(image.filename)
            image.save(os.path.join('static/uploads', filename))  # Save the image to the uploads directory
            app.logger.debug(f"Image saved to {os.path.join('static/uploads', filename)}")  # Log the image save action
        else:
            filename = None

        conn.execute('INSERT INTO reports (description, location, image, notices) VALUES (?, ?, ?, ?)', (description, location, filename, 0))
        conn.commit()
        return jsonify({"message": "Report submitted successfully."}), 201  # Created

    except Exception as e:
        app.logger.error(f"Error inserting report: {str(e)}")  # Log the error
        return jsonify({"error": str(e)}), 500  # Return error message in JSON format

@app.route('/notice_report/<int:report_id>', methods=['GET', 'POST'])
def notice_report(report_id):
    if not session.get('username'):
        return redirect(url_for('login_page'))
    if session.get('user_type') != 'ngo':
        return "Access denied: Only NGO users can access this page.", 403

    conn = get_db_connection()
    report = conn.execute('SELECT * FROM reports WHERE id = ?', (report_id,)).fetchone()
    if not report:
        return "Report not found.", 404

    if request.method == 'POST':
        contact_info = request.form.get('contact_info')
        if not contact_info:
            return render_template('notice_report.html', report=report, error="Contact information is required.")

        try:
            # Insert NGO contact info
            conn.execute('INSERT INTO ngo_contacts (report_id, ngo_username, contact_info) VALUES (?, ?, ?)',
                         (report_id, session.get('username'), contact_info))
            # Update report status to 'Awaiting Confirmation'
            conn.execute('UPDATE reports SET status = ? WHERE id = ?', ('Awaiting Confirmation', report_id))
            conn.commit()
            return redirect(url_for('home'))
        except Exception as e:
            app.logger.error(f"Error submitting notice: {str(e)}")
            return render_template('notice_report.html', report=report, error="An error occurred. Please try again.")

    return render_template('notice_report.html', report=report)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    # Verify user credentials
    if username in users and users[username] == password:
        session['username'] = username
        session['user_type'] = 'client'
        return redirect(url_for('dashboard'))
    else:
        return render_template('login.html', error="Invalid username or password")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        # Simple email validation
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return render_template('signup.html', error="Invalid email address")
        if email in users:
            return render_template('signup.html', error="Email already registered")
        # For demo, password is fixed or can be added to form
        users[email] = 'defaultpassword'
        session['username'] = email
        session['user_type'] = 'client'
        return redirect(url_for('dashboard'))
    return render_template('signup.html')

@app.route('/ngo_login', methods=['GET', 'POST'])
def ngo_login():
    if request.method == 'POST':
        code_number = request.form.get('code_number')
        if code_number not in ngos:
            return render_template('ngo_login.html', error="Invalid NGO code number")
        session['username'] = code_number
        session['user_type'] = 'ngo'
        return redirect(url_for('dashboard'))
    return render_template('ngo_login.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('username'):
        return redirect(url_for('login_page'))
    if session.get('user_type') != 'ngo':
        return "Access denied: Only NGO users can access this page.", 403
    return render_template('dashboard.html')

@app.route('/update_report/<int:id>', methods=['POST'])
def update_report(id):
    try:
        conn = get_db_connection()
        conn.execute('UPDATE reports SET status = "helped" WHERE id = ?', (id,))
        conn.commit()
        return redirect(url_for('reports'))
    except Exception as e:
        app.logger.error(f"Error updating report: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/delete_report/<int:id>', methods=['DELETE'])
def delete_report(id):
    try:
        conn = get_db_connection()
        conn.execute('DELETE FROM reports WHERE id = ?', (id,))
        conn.commit()
        return jsonify({"message": "Report deleted successfully."}), 204
    except Exception as e:
        app.logger.error(f"Error deleting report: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove username from session
    session.pop('user_type', None)
    return redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # Add logic to verify user credentials
        session['username'] = username
        session['user_type'] = 'client'
        return redirect(url_for('dashboard'))
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
