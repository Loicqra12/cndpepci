from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SelectField, IntegerField, FloatField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from models import User
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
class RegistrationForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Confirmer le mot de passe', validators=[DataRequired(), EqualTo('password')])
    
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Ce nom d\'utilisateur est déjà utilisé.')
            
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Cette adresse email est déjà utilisée.')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Nouveau mot de passe', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Confirmer le mot de passe', validators=[DataRequired(), EqualTo('password')])

class ForumTopicForm(FlaskForm):
    title = StringField('Titre', validators=[DataRequired(), Length(max=200)])
    content = TextAreaField('Contenu', validators=[DataRequired()])
    
class ForumPostForm(FlaskForm):
    content = TextAreaField('Message', validators=[DataRequired()])

class ForumCategoryForm(FlaskForm):
    name = StringField('Nom', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description')
    position = IntegerField('Ordre d\'affichage', default=0)
