from flask import Flask, render_template, request, jsonify
from PyPDF2 import PdfReader
import re
import logging

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/')
def index():
    return render_template('index.html', ats_score=0, keyword_suggestions=[])

@app.route('/upload_resume', methods=['POST'])
def upload_resume():
    try:
        if 'resume' not in request.files:
            return jsonify({'error': 'No file uploaded'})
        
        resume_file = request.files['resume']
        if resume_file.filename == '':
            return jsonify({'error': 'No selected file'})
        
        resume_text = extract_text_from_pdf(resume_file)

        if 'job_description' not in request.files:
            return jsonify({'error': 'Job description file not found'})
        
        job_description_file = request.files['job_description']
        if job_description_file.filename == '':
            return jsonify({'error': 'No job description file selected'})
        
        job_description_text = extract_text_from_pdf(job_description_file)

        ats_score, keyword_suggestions = calculate_ats_score(resume_text, job_description_text)

        return jsonify({'ats_score': ats_score, 'keyword_suggestions': keyword_suggestions})
    except Exception as e:
        logging.error(str(e))
        return jsonify({'error': 'Internal Server Error'+str(e)}), 500

def extract_text_from_pdf(file):
    text = ""
    pdf_reader = PdfReader(file)
    for page_num in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page_num].extract_text()
    return text

def calculate_ats_score(resume_text, job_description_text):
    resume_keywords = set(re.findall(r'\b\w+\b', resume_text.lower()))
    job_description_keywords = set(re.findall(r'\b\w+\b', job_description_text.lower()))
    missing_keywords = job_description_keywords - resume_keywords
    ats_score = len(resume_keywords.intersection(job_description_keywords)) / len(job_description_keywords) * 100
    
    technical_terms = ['java', 'javascript', 'ruby', 'php', 'react','Tensorflow', 'Firebase','GoogleCloudPlatform','angular', 'node.js','Jenkins','Selenium','JIRA','typescript', 'db', 'mysql', 'postgresql', 'aws', 'docker', 'kubernetes','PostgreSQL']
    keyword_suggestions = [kw for kw in missing_keywords if kw in technical_terms]

    if not keyword_suggestions:
        soft_skills = ['communication', 'teamwork', 'problem-solving', 'time management', 'creativity']
        keyword_suggestions = soft_skills
    
    return round(ats_score, 2), keyword_suggestions

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
