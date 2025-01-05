from flask import Flask, jsonify, request
import json

from openai import OpenAI

with open('key.txt', 'r') as file:
    key = file.read()
client = OpenAI(api_key=key)

app = Flask(__name__)


@app.route("/")
def index():
    return "Hello, World!"

@app.route("/extract_jd", methods=["POST"])
def extract_jd():
    print(request)
    data = request.get_json()
    print(data)
    if not data or 'jd' not in data:
        return jsonify({"error": "Job description (jd) not provided"}), 400
    job_description = data['jd']
    print(job_description)
    result = extract_job_data(job_description)  # Ensure this function is defined
    return jsonify(result)
def extract_job_data(jd):
    result = []
    prompt = """extract detailed information from job description, including only 3 fields: Major, Tech skills and Experience domain. 
                Always output plain JSON without any markdown or formatting. \n
                Job description is:""" + jd
    try:
        # Call the LLM
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": prompt},
            ],
        )
        result = response.choices[0].message.content
        result = json.loads(result)
    except Exception as e:
        result.append({"error": f"Failed to process JD: {e}"})
    return result

if __name__ == '__main__':
    app.run(debug=True)