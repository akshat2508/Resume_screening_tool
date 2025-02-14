from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from utils.text_extraction import extract_text  # Importing the text extraction function
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Initialize Flask app
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

# Resume Model
class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    file_path = db.Column(db.String(200), nullable=False)
    extracted_text = db.Column(db.Text, nullable=True)  # New Column

# Job Description Model
class JobDescription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    file_path = db.Column(db.String(200), nullable=False)
    extracted_text = db.Column(db.Text, nullable=True)  # Added this line

# Create the database and tables
with app.app_context():
    db.drop_all()  # This drops all tables
    db.create_all()  # This recreates them with the new schema
    print("Database and tables updated!")

@app.route('/')
def home():
    return "Welcome to the Resume Screening Tool!"

# Upload Resume Endpoint
@app.route('/upload-resume', methods=['POST'])
def upload_resume():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # Save the file
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Save metadata to the database
    new_resume = Resume(filename=file.filename, file_path=file_path)
    db.session.add(new_resume)
    db.session.commit()

    # Extract text from the uploaded resume
    extracted_text = extract_text(file_path)
    new_resume.extracted_text = extracted_text
    db.session.commit()

    return jsonify({"message": "Resume uploaded and text extracted successfully", "file_path": file_path}), 200

# Upload Job Description Endpoint
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

# Extract Text from Job Description Endpoint
@app.route('/extract-job-description', methods=['GET'])
def extract_text_from_job_description():
    job_description = JobDescription.query.first()  # Get the first uploaded job description

    if not job_description:
        return jsonify({"error": "No job description available"}), 404

    # Extract text from the job description PDF
    extracted_text = extract_text(job_description.file_path)
    job_description.extracted_text = extracted_text
    db.session.commit()

    return jsonify({"message": "Text extracted successfully", "text": extracted_text}), 200

# Extract Text Endpoint (if needed separately)
@app.route('/extract-text', methods=['GET'])
def extract_text_from_db():
    resumes = Resume.query.all()
    extracted_data = []
    for resume in resumes:
        extracted_data.append({
            "id": resume.id,
            "filename": resume.filename,
            "extracted_text": resume.extracted_text
        })
    return jsonify(extracted_data), 200

# Rank Resumes Endpoint
@app.route('/rank-resumes', methods=['GET'])
def rank_resumes():
    resumes = Resume.query.all()
    job_descriptions = JobDescription.query.all()

    if not resumes or not job_descriptions:
        return jsonify({"error": "No resumes or job descriptions available"}), 400

    # Prepare data for comparison
    results = []
    for jd in job_descriptions:
        jd_text = jd.extracted_text
        if not jd_text:
            return jsonify({"error": "Job description text not extracted"}), 400

        scores = []
        for resume in resumes:
            if resume.extracted_text:
                vectorizer = TfidfVectorizer()
                tfidf_matrix = vectorizer.fit_transform([jd_text, resume.extracted_text])
                score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
                scores.append((resume.id, resume.filename, score))

        # Sort by relevance score
        scores.sort(key=lambda x: x[2], reverse=True)
        results.append({
            "job_description": jd.filename,
            "ranked_resumes": scores
        })

    return jsonify(results), 200

if __name__ == '__main__':
    app.run(debug=True)
