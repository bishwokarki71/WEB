import random
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, redirect, url_for, session, request, flash, jsonify
from datetime import timedelta
from flask import make_response
import socket
import os


app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

app.permanent_session_lifetime = timedelta(minutes=3)  # Set session timeout to 5 minutes

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

@app.before_request
def make_session_permanent():
    # Make the session permanent for every request
    session.permanent = True

# Admin email credentials (use your actual admin email here)
ADMIN_EMAIL = "aayanakarki71@gmail.com"  # Your admin email address
ADMIN_PASSWORD = "ohgi nhlg ncgw svtc"  # Use App Password for Gmail

# Function to read the current admin password from the file
def get_admin_password():
    with open('admin_password.txt', 'r') as f:
        return f.read().strip()

# Function to generate a new random password
def generate_new_password():
    length = 12  # Length of the password
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(length))

# Function to update the password in the file
def update_password(new_password):
    with open('admin_password.txt', 'w') as f:
        f.write(new_password)

# Function to send email to the admin with the new password
def send_password_to_admin(new_password):
    try:
        # Setup the SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(ADMIN_EMAIL, ADMIN_PASSWORD)

        # Create the email content
        subject = "Your New Admin Password"
        body = f"Hello Admin,\n\nYour new password is: {new_password}\n\nBest regards,\nYour Flask App"
        msg = MIMEMultipart()
        msg['From'] = ADMIN_EMAIL
        msg['To'] = ADMIN_EMAIL
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Send the email
        server.sendmail(ADMIN_EMAIL, ADMIN_EMAIL, msg.as_string())
        server.quit()
        print("New password sent to the admin email successfully!")
    except Exception as e:
        print(f"Error: {e}")

# Function to send email for unauthorized login attempts
def send_failed_login_email(username, ip_address, user_agent):
    try:
        print("Sending email for failed login attempt...")  # Debugging
        # Setup the SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(ADMIN_EMAIL, ADMIN_PASSWORD)

        # Create the email content
        subject = "Unauthorized Login Attempt"
        body = f"Hello Admin,\n\nAn unauthorized login attempt was made with the following details:\n\nUsername: {username}\nIP Address: {ip_address}\nDevice/Browser: {user_agent}\n\nBest regards,\nYour Flask App"
        msg = MIMEMultipart()
        msg['From'] = ADMIN_EMAIL
        msg['To'] = ADMIN_EMAIL
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Send the email
        server.sendmail(ADMIN_EMAIL, ADMIN_EMAIL, msg.as_string())
        server.quit()
        print("Unauthorized login attempt email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")  # Log the error if any

# Route for login
@app.route('/', methods=['GET', 'POST'])
def login():
    session.clear()

    error = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if entered password matches the admin password
        if username == "hi" and password == get_admin_password():
            new_password = generate_new_password()
            update_password(new_password)  # Update the password in the file
            send_password_to_admin(new_password)  # Send the new password to the admin's email
            session["logged_in"] = True
            return redirect(url_for('main'))  # Redirect to the main page after successful login
        else:
            # Send email on failed login attempt
            ip_address = request.remote_addr
            user_agent = request.user_agent.string
            send_failed_login_email(username, ip_address, user_agent)
            error = "❌ Incorrect password."

    return render_template('login.html', error=error)

# Route for the main page
@app.route('/main')
def main():
    if not session.get("logged_in"):
        flash("You must log in first!")
        return redirect(url_for("login"))
    return render_template('main.html')  # Render the main page after login

@app.route('/yes')
def yes():
    if not session.get("logged_in"):
        flash("You must log in first!")
        return redirect(url_for("login"))
    return render_template('yes.html')

@app.route('/no1')
def no1():
    if not session.get("logged_in"):
        flash("You must log in first!")
        return redirect(url_for("login"))
    return render_template('no1.html')

@app.route('/no2')
def no2():
    if not session.get("logged_in"):
        flash("You must log in first!")
        return redirect(url_for("login"))
    return render_template('no2.html')

@app.route('/no3')
def no3():
    if not session.get("logged_in"):
        flash("You must log in first!")
        return redirect(url_for("login"))
    return render_template('no3.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)  # Remove login flag from session
    flash('You have been logged out.')
    return redirect(url_for('login'))

@app.route('/check_logged_in')
def check_logged_in():
    if 'logged_in' in session and session['logged_in']:
        return jsonify(logged_in=True)
    else:
        return jsonify(logged_in=False)


#if __name__ == '__main__':
 #   app.run(debug=True, port=5001)  # Use port 5001 to avoid port conflicts

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)