from flask import Flask, request, render_template,jsonify,flash
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
db = SQLAlchemy(app)



# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Define a model for the feedback data
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hostler_day_scholar = db.Column(db.String(20), nullable=False)
    location_specific = db.Column(db.String(20), nullable=False)
    academic_block = db.Column(db.Integer)
    category = db.Column(db.String(20), nullable=False)
    feedback = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text,nullable=False)
    course = db.Column(db.Text,nullable=False)
    branch = db.Column(db.Text,nullable=False)
    Semester = db.Column(db.Integer)


    def __repr__(self):
        return f'<Feedback {self.id}>'

# Create a route for handling the form submission
@app.route('/home')
def homepage():
    return render_template('dean.html')
@app.route('/academicfacility',methods=['GET'])
def academicfacility():
    return render_template('academicfacility.html')
@app.route('/sportfacility')
def sportfacility():
    return render_template('sportfacility.html')
@app.route('/campusfacility')
def campusfacility():
    return render_template('campusfacility.html')
@app.route('/research')
def research():
    return render_template('research.html')
@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')
@app.route('/submission', methods=['POST'])
def feedback():
    if request.method == 'POST':
        # Get the form data from the request
        print("RECEIVED!")
        data = request.get_json()
        hostler_day_scholar = data['stutype']
        location_specific = data['locspec']
        academic_block = data['ab']
        category = data['cat']
        feedback = data['feed']
        name = data['name']
        course = data['cou']
        branch = data['bra']
        semester = data['sem']
        print(semester)
        # Create a new feedback instance
        new_feedback = Feedback(
            name=name,
            course=course,
            branch=branch,
            Semester=semester,
            hostler_day_scholar=hostler_day_scholar,
            location_specific=location_specific,
            academic_block=academic_block,
            category=category,
            feedback=feedback
        )

        # Add the new feedback instance to the database
        db.session.add(new_feedback)
        db.session.commit()
        print(new_feedback)

        # Render a thank you page
        return render_template('thank_you.html')

    # Render the feedback form
    return render_template('complainpage.html')


@app.route('/')
def home():
    return render_template('dean.html')

@app.route('/complain')
def complain():
    return render_template('loginpagewelfare.html')

@app.route('/success')
def openfeedback():
    return render_template('complainpage.html')

@app.route('/placement')
def placement():
    return render_template('placement.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    student= data['student']
    print(data)
    dean = data['dean']
    print(dean)
    if(username=="dean" and password=="5678" and dean=="dean"):
        return "successdean"
    if(username=="naman" and password=="1234" and student=="student"):
        return "success"
    print("failed")
    
    return "failed"

@app.route('/contactus')
def contactus():
    return render_template('contactus.html')

@app.route('/feedbacks') 
def feedbacks():
    feedbacks = Feedback.query.all()
    print(feedbacks)
    return render_template('feedback_list.html', feedbacks=feedbacks)

@app.route('/feedback/search',methods=['GET'])
def search_feedbacks():
    category = request.args.get('category')
    hostler_day_scholar = request.args.get('hostler_day_scholar')
    
    print(hostler_day_scholar)
    feedbacks = Feedback.query.filter_by(hostler_day_scholar=hostler_day_scholar).all()
    print(feedbacks)
    return render_template('feedback_list.html', feedbacks=feedbacks)

if __name__ == '__main__':

    app.run(debug=True)
