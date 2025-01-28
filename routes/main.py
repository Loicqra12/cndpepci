from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from models import User, Member, Page, News
from extensions import db, mail
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Email
from flask_mail import Message

class ContactForm(FlaskForm):
    name = StringField('Nom', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Sujet', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('home.html')

@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        try:
            # Créer le message
            msg = Message(
                subject=f'[CNDPEPCI] {form.subject.data}',
                recipients=[current_app.config['MAIL_DEFAULT_SENDER']],
                reply_to=form.email.data,
                body=f'''Message de {form.name.data} ({form.email.data}):

{form.message.data}
'''
            )
            # Envoyer l'email
            mail.send(msg)
            
            # Email de confirmation à l'expéditeur
            confirm_msg = Message(
                subject='Confirmation de réception de votre message - CNDPEPCI',
                recipients=[form.email.data],
                body=f'''Bonjour {form.name.data},

Nous avons bien reçu votre message et nous vous en remercions.
Nous vous répondrons dans les plus brefs délais.

Cordialement,
L'équipe CNDPEPCI
'''
            )
            mail.send(confirm_msg)
            
            flash('Votre message a été envoyé avec succès!', 'success')
            return redirect(url_for('main.contact'))
        except Exception as e:
            current_app.logger.error(f'Erreur lors de l\'envoi du message: {str(e)}')
            flash('Une erreur est survenue lors de l\'envoi du message. Veuillez réessayer plus tard.', 'error')
    return render_template('contact.html', form=form)

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
