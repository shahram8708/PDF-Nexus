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
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        user_msg = Message('Login Confirmation: Successful Login', recipients=[email])
        user_msg.body = (
            f"Dear {username},\n\n"
            f"You have successfully logged in to PDF Nexus 🤖.\n\n"
            f"You are now a member of our service! You will receive daily emails about our AI tools, which you can explore and utilize.\n\n"
            f"If you wish to cancel your membership, you can do so by clicking the following link:\n"
            f"https://pdf-nexus.onrender.com/cancel\n\n"
            f"Best regards,\nPDF Nexus 🤖 Team"
        )
        
        admin_msg = Message('User Login Notification', recipients=['Email'])
        admin_msg.body = f"User {username} has logged in with the email address: {email}."
        
        try:
            mail.send(user_msg)
            mail.send(admin_msg)
            return redirect(url_for('user_details'))
        except Exception as e:
            return f"Error: {str(e)}"
    
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
app.config['MAIL_USERNAME'] = 'Email'
app.config['MAIL_PASSWORD'] = 'Password'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEFAULT_SENDER'] = 'Email'

mail = Mail(app)

@app.route('/query', methods=['GET', 'POST'])
def query():
    if request.method == 'POST':
        email = request.form['email']
        message = request.form['message']
        
        user_msg = Message('Confirmation: Your Query Received', recipients=[email])
        user_msg.body = (
            f"Dear User,\n\n"
            f"Thank you for your query. We have received the following message from you:\n\n"
            f"{message}\n\n"
            f"You are now a member of our service! You will receive daily emails about our AI tools, which you can explore and utilize.\n\n"
            f"If you wish to cancel your membership, you can do so by clicking the following link:\n"
            f"https://pdf-nexus.onrender.com/cancel\n\n"
            f"Best regards,\nPDF Nexus 🤖 Team"
        )
        
        admin_msg = Message('New Query Received', recipients=['Email'])
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
        rating = request.form.get('rating', 'No rating') 
        
        user_msg = Message('Confirmation: Your Feedback Received', recipients=[email])
        user_msg.body = (
            f"Dear User,\n\n"
            f"Thank you for your feedback. We have received the following message from you:\n\n"
            f"{message}\n\n"
            f"Rating: {rating} stars\n\n"
            f"You are now a member of our service! You will receive daily emails about our AI tools, which you can explore and utilize.\n\n"
            f"If you wish to cancel your membership, you can do so by clicking the following link:\n"
            f"https://pdf-nexus.onrender.com/cancel\n\n"
            f"Best regards,\nPDF Nexus 🤖 Team"
        )
        
        admin_msg = Message('New Feedback Received', recipients=['Email'])
        admin_msg.body = (
            f"New feedback received:\n\n"
            f"Email: {email}\n"
            f"Message:\n{message}\n"
            f"Rating: {rating} stars"
        )
        
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

@app.route('/membership', methods=['GET', 'POST'])
def membership():
    if request.method == 'POST':
        email = request.form['email']
        
        user_msg = Message('Membership Confirmation', recipients=[email])
        user_msg.body = (
            f"Dear User,\n\n"
            f"Thank you for registering for our membership. We have received your email address:\n\n"
            f"{email}\n\n"
            f"You are now a member of our service! You will receive daily emails about our AI tools, which you can explore and utilize.\n\n"
            f"If you wish to cancel your membership, you can do so by clicking the following link:\n"
            f"https://pdf-nexus.onrender.com/cancel\n\n"
            f"Best regards,\nPDF Nexus 🤖 Team"
        )
  
        admin_msg = Message('New Membership Registration', recipients=['Email'])
        admin_msg.body = f"New membership registration:\n\nEmail: {email}"
        
        try:
            mail.send(user_msg)
            mail.send(admin_msg)
            return redirect(url_for('membership_success'))
        except Exception as e:
            return f"Error: {str(e)}"
    return render_template('membership.html')

@app.route('/membership_success')
def membership_success():
    return 'Membership registration successful!'

@app.route('/cancel', methods=['GET', 'POST'])
def cancel():
    if request.method == 'POST':
        email = request.form['email']

        user_msg = Message('Membership Cancellation Confirmation', recipients=[email])
        user_msg.body = (
            f"Dear User,\n\n"
            f"You have successfully canceled your membership with PDF Nexus 🤖. You will no longer receive emails or no have access to the AI tools.\n\n"
            f"If you wish to rejoin our membership, you can do so by clicking the following link:\n"
            f"https://pdf-nexus.onrender.com/membership\n\n"
            f"Best regards,\nPDF Nexus 🤖 Team"
        )
        
        admin_msg = Message('Membership Cancellation', recipients=['Email'])
        admin_msg.body = f"Membership cancellation:\n\nEmail: {email}"
        
        try:
            mail.send(user_msg)
            mail.send(admin_msg)
            return redirect(url_for('cancel_success'))
        except Exception as e:
            return f"Error: {str(e)}"
    return render_template('cancel.html')

@app.route('/cancel_success')
def cancel_success():
    return 'Membership canceled successful!'

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
