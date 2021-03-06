from flask import Flask,render_template,request,redirect,url_for,flash,session
from formulaire import LoginForm,RegisterForm,ModalForm
from config import Config
from flask_sqlalchemy import SQLAlchemy


#from  werkzeug.security import generate_password_hash,check_password_hash

app = Flask(__name__)
app.config.from_object(Config)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SECRET_KEY']="my key"
db = SQLAlchemy(app)

#classe du model de notre base de donnees
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pseudo= db.Column(db.String(20), unique=True)
    email = db.Column(db.String(120), unique=True)
    mdp= db.Column(db.Text(120))

#route vers la page d'affichage et modification des donnees
@app.route('/infos/<int:id>',methods=['POST','GET'])
def infos(id):
	id1=session['user']['id']
	if id1==id:
		title='Informations'
		form=ModalForm()
		usr=Users.query.filter_by(id=id).first()
		if form.validate_on_submit():
			pseudo=form.pseudo.data
			mail=form.mail.data
			mdp=form.mdp.data
			update_=Users.query.filter_by(id=id).update({'pseudo':pseudo,'email':mail,'mdp':mdp})
			db.session.commit()

			usr.pseudo=form.pseudo.data
			usr.mail=form.mail.data
			usr.mdp=form.mdp.data

			form.pseudo.data=''
			form.mail.data=''
			form.mail.data=''
			flash("Information modifiee avec succes",'success')

		return render_template('Pages/infos.html',title=title,form=form,usr=usr)
	return redirect(url_for('infos',id=id1))


#route vers la de connexion
@app.route('/',methods=['POST','GET'])
def login():
	form=LoginForm()
	title='login'
	pseudo_=None
	if form.validate_on_submit():
		usr=Users.query.filter_by(email=form.mail.data).first()
		if not usr:
			flash("Ce compte est inexistant ",'danger')
		elif usr.mdp==form.mdp.data :
			session['user']={
			     'email':form.mail.data,
			     'id':usr.id
			}
			return redirect(url_for('infos',id=usr.id))
		else:
			flash("Le mot de passe est incorrecte",'danger')
		
	return render_template('Pages/login.html',title=title,form=form)



#route de deconnexion 
@app.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('login'))

#route vers la page de creation de compte
@app.route('/register',methods=['POST','GET'])
def register():
	form=RegisterForm()
	title='register'
	result=None
	if form.validate_on_submit():
		usr=Users.query.filter_by(pseudo=form.pseudo.data).first()

		if usr is None:
			mail_=Users.query.filter_by(email=form.mail.data).first()
			if mail_ is None:
				usr=Users(pseudo=form.pseudo.data,email=form.mail.data,mdp=form.mdp.data)
				db.session.add(usr)
				db.session.commit()
				form.pseudo.data=''
				form.mail.data=''
				form.mdp.data=''
				flash("Votre compte a ete cree avec succes",'success')
			else:
				flash("Cet email existe deja !",'danger')
		else:
		  	flash("Le pseudo n'est plus disponible !",'danger')
		    
	return render_template('Pages/register.html',title=title,form=form,)


if __name__=='__main__':
	db.create_all()
	app.run(debug=True)
