import os
import markdown
from flask import Flask, request, render_template, jsonify, redirect, url_for
import google.generativeai as genai
from flask_mail import Mail, Message

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

@app.route('/privacy', methods=['GET', 'POST'])
def privacy():
    return render_template('privacy.html')

@app.route('/terms', methods=['GET'])
def terms():
    return render_template('terms.html')

@app.route('/support', methods=['GET'])
def support():
    return render_template('support.html')

@app.route('/explore', methods=['GET'])
def explore():
    return render_template('explore.html')

@app.route('/pdf', methods=['GET'])
def pdf():
    return render_template('pdf.html')

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'Email_ID'
app.config['MAIL_PASSWORD'] = 'Password'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEFAULT_SENDER'] = 'Email_ID'

mail = Mail(app)

@app.route('/query', methods=['GET', 'POST'])
def query():
    if request.method == 'POST':
        email = request.form['email']
        message = request.form['message']
        
        user_msg = Message('Confirmation: Your Query Received', recipients=[email])
        user_msg.body = f"Dear User,\n\nThank you for your query. We have received the following message from you:\n\n{message}\n\nBest regards,\nPDF Nexus 🤖 Team"
        
        admin_msg = Message('New Query Received', recipients=['Email_ID'])
        admin_msg.body = f"New query received:\n\nEmail: {email}\nMessage:\n{message}"
        
        try:
            mail.send(user_msg)
            mail.send(admin_msg)
            return redirect(url_for('success'))
        except Exception as e:
            return f"Error: {str(e)}"
    return render_template('query.html')

@app.route('/success')
def success():
    return 'Query sent successfully!'

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        email = request.form['email']
        message = request.form['message']
        
        user_msg = Message('Confirmation: Your Feedback Received', recipients=[email])
        user_msg.body = f"Dear User,\n\nThank you for your feedback. We have received the following message from you:\n\n{message}\n\nBest regards,\nPDF Nexus 🤖 Team"
        
        admin_msg = Message('New Feedback Received', recipients=['Email_ID'])
        admin_msg.body = f"New feedback received:\n\nEmail: {email}\nMessage:\n{message}"
        
        try:
            mail.send(user_msg)
            mail.send(admin_msg)
            return redirect(url_for('feedback_success'))
        except Exception as e:
            return f"Error: {str(e)}"
    return render_template('feedback.html')

@app.route('/feedback_success')
def feedback_success():
    return 'Feedback sent successfully!'

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
