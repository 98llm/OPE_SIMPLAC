from flask import Flask, session, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, logout_user, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2

#Configure app
app = Flask(__name__)
app.config["SECRET_KEY"] = b"\x05\x19s\x8a\xd06\x07\xf8ofL0\xc5-\xc0"

#configure database
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:123@localhost:5432/teste"

db = SQLAlchemy(app)


login_manager = LoginManager(app)


connection = psycopg2.connect(
    host ="localhost",
    user = "postgres",
    password = "123",
    dbname = "teste"
)

cursor = connection.cursor()


class User(db.Model, UserMixin):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, autoincrement = True ,primary_key=True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    password = db.Column(db.String, nullable = False)

    def __repr__(self):
        return f'<user: {self.username}>'

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)



@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

'''
@app.route('/')
def index():
    users = User.query.filter_by(username = 'teste').first()
    return render_template('home.html', users=users)
'''

@app.route('/')
def index():
    if 0 == 0:
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login', methods = ['POST', 'GET'])
def login():
    next = request.args.get('next')
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']
        user = User.query.filter_by(username = user).first()

        checkPwd = check_password_hash(user.password, pwd)

        if not user or not checkPwd:
            return redirect(url_for('login'))
        
        login_user(user)
        return redirect(url_for('home'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
