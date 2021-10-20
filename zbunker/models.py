from zbunker import db, login_manager
from flask_login import UserMixin
from zbunker import bcrypt


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    prime = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"{self.username}, {self.email}"

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)


class OTPModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), nullable=False)
    otp = db.Column(db.Integer)


class Courses(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.Integer, primary_key=True, unique=True)
    is_prime = db.Column(db.Boolean, default=True, unique=False)
