from flask import Flask, render_template, request, redirect, url_for, session
import boto3
import os
from dotenv import load_dotenv
from datetime import datetime
from flask_bootstrap import Bootstrap5
import requests
from functools import wraps



# Load secrets
load_dotenv()
app = Flask(__name__)
app.secret_key = 'secret-key'
bootstrap = Bootstrap5(app)


#Cognito Configurations
COGNITO_DOMAIN = os.getenv('COGNITO_DOMAIN')
CLIENT_ID = os.getenv('CLIENT_ID')
REDIRECT_URI = 'http://localhost:5000/callback'
TOKEN_URL = f'https://{COGNITO_DOMAIN}/oauth2/token'
LOGOUT_URL = f'https://{COGNITO_DOMAIN}/logout?client_id={CLIENT_ID}&logout_uri=http://localhost:5000/'


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'id_token' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function



@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("home.html")


@app.route("/login")
def login():
    hosted_ui_url = (
        f'https://{COGNITO_DOMAIN}/login?client_id={CLIENT_ID}'
        f'&response_type=code&scope=email+openid+phone+profile'
        f'&redirect_uri={REDIRECT_URI}'
    )
    return redirect(hosted_ui_url)


@app.route('/signup')
def signup():
    hosted_ui_url = (
        f'https://{COGNITO_DOMAIN}/signup?client_id={CLIENT_ID}'
        f'&response_type=code&scope=email+openid+phone+profile'
        f'&redirect_uri={REDIRECT_URI}'
    )
    return redirect(hosted_ui_url)
    

@app.route("/callback", methods=["GET", "POST"]) #Using for Cognito Hosted UI
def callback():
    code = request.args.get('code')
    if not code:
        return 'Missing code', 400

    data = {
        'grant_type': 'authorization_code',
        'client_id': CLIENT_ID,
        'code': code,
        'redirect_uri': REDIRECT_URI
    }

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    response = requests.post(TOKEN_URL, data=data, headers=headers)
    if response.status_code != 200:
        return f'Error exchanging code: {response.text}', 400

    tokens = response.json()
    session['id_token'] = tokens['id_token']
    session['access_token'] = tokens['access_token']

    return redirect('/dashboard')


@login_required
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    return render_template("dashboard.html")


@app.route('/logout')
def logout():
    session.clear()
    return redirect(LOGOUT_URL)


if __name__ == "__main__":
    app.run(debug=True)
