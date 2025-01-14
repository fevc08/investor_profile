from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_profiles.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

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
    savings_capacity = db.Column(db.Enum('low', 'medium', 'high'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(datetime.timezone.utc))
    update_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(datetime.timezone.utc), onupdate=lambda: datetime.now(datetime.timezone.utc))

    def __repr__(self):
        return f'<UserProfile {self.first_name} {self.last_name}>'

# Route for rendering the form
@app.route('/')
def form():
    return render_template('form.html')

# Route for handling form submission
@app.route('/submit-profile', methods=['POST'])
def submit_profile():
    # Retrieve form data
    form_data = request.form
    
    # Calculate scores based on form answers
    financial_knowledge_score = calculate_financial_knowledge(form_data)
    risk_tolerance_score = calculate_risk_tolerance(form_data)
    savings_capacity_score = calculate_savings_capacity(form_data)
    
    # Determine the level based on scores
    financial_knowledge_level = determine_level(financial_knowledge_score, ['basic', 'intermediate', 'expert'])
    risk_tolerance = determine_level(risk_tolerance_score, ['low', 'medium', 'high'])
    savings_capacity = determine_savings_capacity(calculate_savings_capacity, ['low', 'medium', 'high'])
    
    # Create or update the user profile
    user_profile = UserProfile.query.filter_by(user_id=1).first()  # Assuming user_id is 1 for this example
    
    if user_profile:
        # Update existing profile
        user_profile.first_name = form_data['first_name']
        user_profile.last_name = form_data['last_name']
        user_profile.sex = form_data['sex']
        user_profile.date_of_birth = datetime.strptime(form_data['date_of_birth'], '%Y-%m-%d').date()
        user_profile.country = form_data['country']
        user_profile.city = form_data['city']
        user_profile.address = form_data['address']
        user_profile.postal_code = int(form_data['postal_code'])
        user_profile.dni = int(form_data['dni'])
        user_profile.financial_knowledge_level = financial_knowledge_level
        user_profile.risk_tolerance = risk_tolerance
        user_profile.savings_capacity = savings_capacity
    else:
        # Create new profile
        user_profile = UserProfile(
            user_id=1,
            first_name=form_data['first_name'],
            last_name=form_data['last_name'],
            sex=form_data['sex'],
            date_of_birth=datetime.strptime(form_data['date_of_birth'], '%Y-%m-%d').date(),
            country=form_data['country'],
            city=form_data['city'],
            address=form_data['address'],
            postal_code=int(form_data['postal_code']),
            dni=int(form_data['dni']),
            financial_knowledge_level=financial_knowledge_level,
            risk_tolerance=risk_tolerance,
            savings_capacity=savings_capacity
        )
        db.session.add(user_profile)
    
    db.session.commit()
    
    return redirect(url_for('form'))

# Helper functions for score calculation
def calculate_financial_knowledge(form_data):
    score = 0
    if 'question1' in form_data and form_data['question1'] == 'correct':
        score += 10
    if 'question2' in form_data and form_data['question2'] == 'correct':
        score += 15
    # Add more questions as needed
    return score

def calculate_risk_tolerance(form_data):
    score = 0
    if 'risk_question1' in form_data and form_data['risk_question1'] == 'high':
        score += 30
    if 'risk_question2' in form_data and form_data['risk_question2'] == 'medium':
        score += 20
    # Add more questions as needed
    return score

def calculate_savings_capacity(form_data):
    score = 0
    if 'income' in form_data:
        score += int(form_data['income']) - int(form_data['expenses']) * 0.1  # 10% of income as an example
    return score

def determine_level(score, levels):
    if score >= 10:
        return levels[2]
    elif score < 10 and score >= 5:
        return levels[1]
    else:
        return levels[0]

def determine_savings_capacity(score, levels):
    if score < 100:
        return levels[0]
    elif score >= 100 and score < 500:
        return levels[1]
    else:
        return levels[2]

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # This will create the database if it doesn't exist
    app.run()