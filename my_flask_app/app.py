from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a strong secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)  # Using email as username
    password = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    grade = db.Column(db.String(50), nullable=False)
    career_interest = db.Column(db.String(150), nullable=False)
    about_yourself = db.Column(db.Text, nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        username = request.form['email']  # Use email as username
        password = request.form['password']
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        grade = request.form['grade']
        career_interest = request.form['careerInterest']
        about_yourself = request.form['aboutYourself']

        # Hash the password
        hashed_password = generate_password_hash(password, method='sha256')

        # Create a new user
        new_user = User(
            username=username,
            password=hashed_password,
            email=username,
            first_name=first_name,
            last_name=last_name,
            grade=grade,
            career_interest=career_interest,
            about_yourself=about_yourself
        )

        # Add the user to the database
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! You can now log in.', 'success')
        return jsonify(success=True)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('profile'))  # Redirect to the profile page after successful login
        else:
            flash('Login failed. Check your username and password.', 'danger')
    return render_template('student.html')  # Render the login page if GET request

@app.route('/profile')
@login_required
def profile():
    return render_template('studentprofile.html', name=current_user.first_name)  # Display the user's first name

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)