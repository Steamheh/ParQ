import os
from dotenv import load_dotenv
from flask import Flask
from flask_login import UserMixin, LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData

app = Flask(__name__)

# LOAD .ENV FILE
load_dotenv()

# SECRET KEY FOR FLASK FORMS
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['RECAPTCHA_PRIVATE_KEY'] = os.getenv('RECAPTCHA_PRIVATE_KEY')
app.config['RECAPTCHA_PUBLIC_KEY'] = os.getenv('RECAPTCHA_PUBLIC_KEY')


# DATABASE CONFIGURATION
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_ECHO'] = True if os.getenv('SQLALCHEMY_ECHO') == 'True' else False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True if os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS') == 'True' else False

login_manager = LoginManager()
login_manager.init_app(app)

metadata = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_names)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }
)


db = SQLAlchemy(app, metadata=metadata)
migrate = Migrate(app, db)

class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    bookings = db.relationship('Booking', backref='user', lazy=True)

    def __init__(self, email, firstname, lastname, phone, password):
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.phone = phone
        self.password = password
        self.role = "end_user"

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    def check_password(self, password):

        try:
            correct_password = passwordHasher.verify(self.password, password)
        except:
            correct_password = False
        return correct_password


#class Log(db.Model):


class Booking(db.Model, UserMixin):

    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    location = db.Column(db.Text, nullable=False)
    parkingspotid = db.Column(db.Text, nullable=False)
    numplate = db.Column(db.Text, nullable=False)


class City(db.Model, UserMixin):

    __tablename__ = 'cities'

    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.Text, nullable=False)


#class ParkingLot(db.Model, UserMixin):


from accounts.views import accounts_bp, passwordHasher

#from dashboard.views import dashboard_bp
from booking.views import booking_bp
app.register_blueprint(accounts_bp)
#app.register_blueprint(dashboard_bp)
app.register_blueprint(booking_bp)