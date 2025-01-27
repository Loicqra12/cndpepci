from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from models import User, Member, Page, News
from extensions import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/contact')
def contact():
    return render_template('contact.html')

@main_bp.route('/formation-programmes')
def formation_programmes():
    return render_template('formation_programmes.html')

@main_bp.route('/profession-detective')
def profession_detective():
    return render_template('profession_detective.html')

@main_bp.route('/client-services')
def client_services():
    return render_template('client_services.html')

@main_bp.route('/presse-actualites')
def presse_actualites():
    return render_template('presse_actualites.html')
