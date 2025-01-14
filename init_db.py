from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize Flask app for database creation
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_profiles.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the UserProfile model (same as before)
class UserProfile(db.Model):
    __tablename__ = 'user_profile'
    
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    sex = db.Column(db.Enum('M', 'F'), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    country = db.Column(db.String(80), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    address = db.Column(db.Text, nullable=False)
    postal_code = db.Column(db.Integer, nullable=False)
    dni = db.Column(db.Integer, nullable=False)
    financial_knowledge_level = db.Column(db.Enum('basic', 'intermediate', 'expert'), nullable=False)
    risk_tolerance = db.Column(db.Enum('low', 'medium', 'high'), nullable=False)
    savings_capacity = db.Column(db.Numeric, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(datetime.timezone.utc))
    update_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(datetime.timezone.utc), onupdate=lambda: datetime.now(datetime.timezone.utc))

    def __repr__(self):
        return f'<UserProfile {self.first_name} {self.last_name}>'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print("SQLite database 'user_profiles.db' has been created with the user_profile table.")