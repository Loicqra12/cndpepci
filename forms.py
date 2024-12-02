from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class ContactForm(FlaskForm):
    name = StringField('Nom', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Sujet', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])

class MemberForm(FlaskForm):
    first_name = StringField('Prénom', validators=[DataRequired()])
    last_name = StringField('Nom', validators=[DataRequired()])
    email = StringField('Email', validators=[Email()])
    phone = StringField('Téléphone', validators=[DataRequired()])
    region = SelectField('Région', choices=[
        ('abidjan', 'Abidjan'),
        ('yamoussoukro', 'Yamoussoukro'),
        ('bouake', 'Bouaké'),
        ('korhogo', 'Korhogo'),
        ('san_pedro', 'San-Pédro')
    ])
    specialization = StringField('Spécialisation')
    bio = TextAreaField('Biographie')
    address = StringField('Adresse')

class PageForm(FlaskForm):
    title = StringField('Titre', validators=[DataRequired()])
    content = TextAreaField('Contenu', validators=[DataRequired()])
