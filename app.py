from flask import Flask, render_template, request, redirect, url_for
import boto3
import os
from dotenv import load_dotenv
from datetime import datetime
from flask_bootstrap import Bootstrap5


# Load secrets
load_dotenv()
app = Flask(__name__)
bootstrap = Bootstrap5(app)


def login_required():
    pass


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("home.html")


@app.route("/callback", methods=["GET", "POST"]) #Using for Cognito Hosted UI
def callback():
    return redirect(url_for("dashboard"))


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(debug=True)
