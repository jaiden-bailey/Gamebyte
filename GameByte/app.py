from flask import Flask, render_template, request, redirect, session, url_for
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import werkzeug
from werkzeug.security import check_password_hash, generate_password_hash
import requests
import datetime as dt



app = Flask(__name__)


app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

users = {'mike': {'password': 'milk_123'}}

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site123.db' # Local SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# User Loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Define the User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(1000), nullable=False)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
    
# Protected route
@app.route('/protected')
@login_required
def protected():
    return render_template('profile.html')



    
# index page route
@app.route('/')
def index():
    return render_template('index.html')


# reviews page route
@app.route('/reviews')
def reviews():
    return render_template('reviews.html')



#login page route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                session['user_id'] = user.id
                return redirect(url_for('protected'))
            else:
                return 'Invalid password!'
        else:
            return 'No account found!'
    return render_template('login.html')

# register page route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password'] 
        hashed_password = werkzeug.security.generate_password_hash(password=password, method='scrypt', salt_length=16)
        if User.query.filter_by(email=email).first():
            return "An account with this email or username already exists."
        user = User(username=username, email=email, password=hashed_password)
        try:
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
        except IntegrityError:
            db.session.rollback()
            return "An account with this email already exists."
    else:
        return render_template('register.html')



# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear() 
    return render_template('index.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)