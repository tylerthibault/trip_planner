from flask_app import app
from flask import render_template, redirect, session, request


@app.route('/')
def index():
    return render_template('/index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('/dashboard.html')
