from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SelectField, IntegerField, FloatField
from wtforms.validators import DataRequired, Email, Length
from flask_wtf.file import FileAllowed, FileField

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
    photo = FileField('Photo de profil', validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], 'Images uniquement!')
    ])
    agency_name = StringField('Nom de l\'agence')
    role = StringField('Rôle')
    certifications = TextAreaField('Certifications')
    domains = TextAreaField('Domaines d\'expertise')
    experience_years = IntegerField('Années d\'expérience')
    license_number = StringField('Numéro de licence')
    website = StringField('Site web')
    latitude = FloatField('Latitude')
    longitude = FloatField('Longitude')

class PageForm(FlaskForm):
    title = StringField('Titre', validators=[DataRequired()])
    content = TextAreaField('Contenu', validators=[DataRequired()])
