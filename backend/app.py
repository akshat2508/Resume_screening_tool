from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from utils.text_extraction import extract_text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)  
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
    extracted_text = db.Column(db.Text, nullable=True)

# Job Description Model
class JobDescription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    file_path = db.Column(db.String(200), nullable=False)
    extracted_text = db.Column(db.Text, nullable=True)

# Create the database and tables
with app.app_context():
    JobDescription.query.delete()  # Remove old job descriptions
    db.session.commit()
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

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    extracted_text = extract_text(file_path)

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

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    extracted_text = extract_text(file_path)

    new_job = JobDescription(filename=file.filename, file_path=file_path, extracted_text=extracted_text)
    db.session.add(new_job)
    db.session.commit()

    return jsonify({"message": "Job description uploaded and text extracted successfully", "file_path": file_path}), 200

# Rank Resumes Endpoint
@app.route('/rank-resumes', methods=['GET','POST'])  # Changed from POST to GET
def rank_resumes():
    job_description = JobDescription.query.first()
    if not job_description:
        return jsonify({"error": "No job description found"}), 404

    job_description_text = job_description.extracted_text
    resumes = Resume.query.all()

    if not resumes:
        return jsonify({"error": "No resumes found"}), 404

    resume_texts = [resume.extracted_text for resume in resumes]
    resume_files = [resume.filename for resume in resumes]

    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform([job_description_text] + resume_texts)
    cosine_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

    ranked_resumes = sorted(
        zip(resume_files, cosine_similarities),
        key=lambda x: x[1],
        reverse=True
    )

    ranked_resumes_percentage = [
        {"rank": i + 1, "name": filename, "similarity": round(score * 100, 2)}
        for i, (filename, score) in enumerate(ranked_resumes)
    ]

    print("Ranked Resumes:", ranked_resumes_percentage)  # Debugging output

    return jsonify({
        "job_description": job_description.filename,
        "ranked_resumes": ranked_resumes_percentage
    }), 200

if __name__ == '__main__':
    app.run(debug=True)
