from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required,logout_user


app = Flask(__name__)

db = SQLAlchemy(app)

userpass = 'mysql://root:@'
basedir = '127.0.0.1'
dbname = '/loginsys'

app.config['SQLALCHEMY_DATABASE_URI']=userpass+basedir+dbname
app.config['SECRET_KEY']='gfgsdjfghjkfgksdgfksgdkjgdskjfgsdkjgdkjgjd'


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'signin'


class User(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(255))
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



@app.route('/')
def signin():
    return render_template('index.html')


@app.route('/processor',methods=['POST'])
def processor():
    username = request.form['username']
    password = request.form['password']
    user=User.query.filter_by(username=username).first()
    if user:
        if user.password == password:
            login_user(user)
            return redirect(url_for('dashboard'))
    else:
        return("invalid username and password")

@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        new_user = User(email=email,username=username,password=password)
        db.session.add(new_user)
        db.session.commit()
        return("Signup complete!!!")

    return render_template('signup.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/logout')
def logout():
    logout_user()
    return('you have log out!!!')
if __name__ == '__main__':
  app.run(host='localhost', port=8000, debug=True)
 
