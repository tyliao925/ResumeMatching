from flask import Flask, jsonify, request
import PyPDF2
from openai import OpenAI
import json

with open('keys.txt', 'r') as file:
    key = file.read()
    print(key)
client = OpenAI(api_key=key)

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello, World!"

@app.route("/read_resume", methods=["POST"])
def read_resume():
    # file=@path_to_resume.pdf
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and file.filename.endswith('.pdf'):
        return jsonify(extract_student_info(file))
    
    return jsonify({'error': "Invalid file format. Please upload a PDF file."}), 400

def extract_student_info(file):
    text = extract_text_from_pdf(file)
    llm_response = llm_parse(text)
    return json.loads(llm_response)

def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

def llm_parse(text):
    prompt = """You are a recruiter looking to extract information from a student resume. 
c the name, school, gpa, major, tech_skills, experience_domain from the student resume. 
Always output plain JSON without any markdown or formatting, only the raw JSON object. 
Resume\n""" + text

    response = client.chat.completions.create(
        model="o1-mini",
        messages=[
            {"role": "user", "content": prompt},
        ],
    )

    return response.choices[0].message.content

if __name__ == '__main__':
    app.run(debug=True)
