import os
import markdown
from flask import Flask, request, render_template, jsonify
import google.generativeai as genai

app = Flask(__name__)

genai.configure(api_key=os.environ['API_KEY'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/user-details', methods=['GET'])
def user_details():
    return render_template('user-details.html')

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/process', methods=['POST'])
def process():
    try:
        uploaded_files = request.files.getlist("images")
        prompt = request.form.get("prompt")

        images = []
        for file in uploaded_files:
            image_data = {
                'mime_type': file.content_type,
                'data': file.read()
            }
            images.append(image_data)

        response = genai.GenerativeModel('gemini-1.5-flash').generate_content([prompt] + images)
        markdown_text = response.text

        html_text = markdown.markdown(markdown_text)

        return jsonify({"html": html_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)