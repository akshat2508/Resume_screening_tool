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
    # Remove all job descriptions but keep resumes
    JobDescription.query.delete()  # This deletes all job descriptions
    db.session.commit()
    
    # Create tables if not already present
    db.create_all()
    print("Database updated: Previous job descriptions removed, resumes preserved.")


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

    # Extract text from the uploaded resume
    extracted_text = extract_text(file_path)

    # Save metadata and extracted text to the database
    new_resume = Resume(filename=file.filename, file_path=file_path, extracted_text=extracted_text)
    db.session.add(new_resume)
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

    # Extract text from the uploaded job description
    extracted_text = extract_text(file_path)

    # Save metadata and extracted text to the database
    new_job = JobDescription(filename=file.filename, file_path=file_path, extracted_text=extracted_text)
    db.session.add(new_job)
    db.session.commit()

    return jsonify({"message": "Job description uploaded and text extracted successfully", "file_path": file_path}), 200

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
@app.route('/rank-resumes', methods=['POST'])
def rank_resumes():
    # Check if a job description is uploaded
    if 'file' not in request.files:
        return jsonify({"error": "No job description uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # Save the job description file
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Extract text from the job description
    job_description_text = extract_text(file_path)

    # Get all stored resumes from the database
    resumes = Resume.query.all()
    if not resumes:
        return jsonify({"error": "No resumes found in the database"}), 404

    # Extract text of all resumes
    resume_texts = [resume.extracted_text for resume in resumes]
    resume_files = [resume.filename for resume in resumes]

    # Apply TF-IDF and Cosine Similarity
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform([job_description_text] + resume_texts)
    cosine_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

    # Rank resumes by similarity score
    ranked_resumes = sorted(
        zip(resume_files, cosine_similarities),
        key=lambda x: x[1],
        reverse=True
    )

    # Convert similarity scores to percentages
    ranked_resumes_percentage = [
        (i + 1, filename, round(score * 100, 2)) for i, (filename, score) in enumerate(ranked_resumes)
    ]

    # Return the ranked resumes
    return jsonify({
        "job_description": file.filename,
        "ranked_resumes": ranked_resumes_percentage
    }), 200

if __name__ == '__main__':
    app.run(debug=True)
