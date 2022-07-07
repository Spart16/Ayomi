from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField
from wtforms.validators import DataRequired,Email,Length, ValidationError


class LoginForm(FlaskForm):
    mail=StringField('mail',validators=[DataRequired(),Email()])
    mdp=PasswordField('mdp',validators=[DataRequired(),Length(min=4,max=8)])
    btn=SubmitField("Se connecter")



class RegisterForm(FlaskForm):
    pseudo= StringField('name', validators=[DataRequired(),Length(min=4,max=10)])
    mail=StringField('mail', validators=[DataRequired(),Email()])
    mdp=PasswordField('mdp',validators=[DataRequired(),Length(min=4,max=8)])
    btn=SubmitField('Creer compte')

    def insertData(self):

    	if pseudo.data=='toto':
    		raise ValidationError("Pseudo non disponible")


class ModalForm(FlaskForm):
    pseudo= StringField('name', validators=[DataRequired(),Length(min=4,max=10)])
    mail=StringField('mail',validators=[DataRequired(),Email()])
    mdp=PasswordField('mdp',validators=[DataRequired(),Length(min=4,max=8)])
    btn=SubmitField("Enregistrer")







