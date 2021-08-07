from zbunker import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return(f"{self.username}, {self.email}")


class Courses(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    course_name = db.Column(db.Integer,primary_key=True, unique=True)
    is_prime = db.Column(db.Boolean,default=True, unique=False)

    


db.create_all()