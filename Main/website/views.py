from flask import Blueprint, render_template, Flask, request, jsonify
from flask import Blueprint, jsonify, request, render_template
import traceback
from flask import current_app
from flask_login import  login_required, current_user


from . import db
import google.generativeai as genai
import os


views = Blueprint('views', __name__)

@views.route('/contact')
def contact():
    return render_template('contact.html')



@views.route('/faqs')
def faqs():
    return render_template('faqs.html')


@views.route('/')
@login_required
def home():
    return render_template('index.html', user=current_user)

@views.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@views.route('/yoga')
@login_required
def yoga():
    return render_template('yoga.html', user=current_user)


@views.route('/exercise')
@login_required
def exercise():
    return render_template('exercise.html', user=current_user)

@views.route('/test', methods=['GET'])
def test():
    return jsonify({'status': 'Server is running!'})



@views.route('/calorie-assistant')
@login_required
def calories():
    return render_template('calories.html')



@views.route('/chatbot')
def chatbot():
    return render_template("chatbot.html")  # This will serve the HTML file



@views.route('/api/search', methods=['POST'])
@login_required
def search():
    data = request.get_json()
    query = data.get('query')
    response = current_app.model.generate_content(
            f"As a fitness expert, please answer the following question: {query}"
        )
    
    return response.text
