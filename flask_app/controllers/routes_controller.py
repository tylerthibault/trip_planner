from flask_app import app
from flask import render_template, redirect, session, request


@app.route('/')
def index():
    if "uuid" in session:
        return redirect("/dashboard")
    return render_template('/index.html')

@app.route('/dashboard')
def dashboard():
    if "uuid" not in session:
        return redirect('/')
    return render_template('/users/dashboard.html')
