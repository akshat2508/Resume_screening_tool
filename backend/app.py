from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os



# source ../venv/bin/activate


app = Flask(__name__)


# Configure Upload Folder and Database
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./resumes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# Define a model for Resumes
class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    file_path = db.Column(db.String(200), nullable=False)

# Define a model for Job Descriptions
class JobDescription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    file_path = db.Column(db.String(200), nullable=False)

# Create the database and tables
with app.app_context():
    db.drop_all()  # Drop all tables (optional)
    db.create_all()  # Recreate all tables
    print("Database and tables created!")


@app.route('/')
def home():
    return "Welcome to the Resume Screening Tool!"

# Endpoint to upload resumes
@app.route('/upload-resume', methods=['POST'])
def upload_resume():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # Save the file to the uploads folder
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Save metadata to the database
    new_resume = Resume(filename=file.filename, file_path=file_path)
    db.session.add(new_resume)
    db.session.commit()

    return jsonify({"message": "Resume uploaded successfully", "file_path": file_path}), 200

# Endpoint to upload job descriptions
@app.route('/upload-job-description', methods=['POST'])
def upload_job_description():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # Save the file to the uploads folder
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Save metadata to the database
    new_job = JobDescription(filename=file.filename, file_path=file_path)
    db.session.add(new_job)
    db.session.commit()

    return jsonify({"message": "Job description uploaded successfully", "file_path": file_path}), 200

if __name__ == '__main__':
    app.run(debug=True)
