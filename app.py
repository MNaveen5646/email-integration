from flask import Flask, request, jsonify
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content

app = Flask(__name__)

# You should replace this with your SendGrid API key
SENDGRID_API_KEY = 'REDACTED'

@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.get_json()
    recipient_email = data.get("recipient_email")
    
    if not SENDGRID_API_KEY:
        return jsonify({"error": "SENDGRID_API_KEY is not set"}), 500
    if not recipient_email:
        return jsonify({"error": "Recipient email is missing"}), 400

    try:
        sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)

        from_email = Email("digital@orientspectra.com")  # Replace with your SendGrid email
        to_email = To(recipient_email)
        subject = "Test Email from Flask API"
        content = Content("text/plain", "This is a test email sent from a Flask API using SendGrid.")

        mail = Mail(from_email, to_email, subject, content)

        # Send email
        response = sg.send(mail)

        # Return a success message with status code
        if response.status_code == 202:
            return jsonify({"message": "Email sent successfully!", "status_code": response.status_code}), 200
        else:
            return jsonify({"message": "Failed to send email", "status_code": response.status_code, "response_body": response.body.decode()}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/send-email-lead-form-popup', methods=['POST'])
def send_email_lead_form():
    data = request.get_json()
    recipient_email = data.get("recipient_email")
    Dynamic_content = data.get("content") #we need to add content or required fileds like this...
    
    if not SENDGRID_API_KEY:
        return jsonify({"error": "SENDGRID_API_KEY is not set"}), 500
    if not recipient_email:
        return jsonify({"error": "Recipient email is missing"}), 400

    try:
        sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)

        from_email = Email(recipient_email)  # Replace with your SendGrid email
        to_email = To("digital@orientspectra.com")
        subject = "Test Email from Flask API"
        content = Content(Dynamic_content)

        mail = Mail(from_email, to_email, subject, content)

        # Send email
        response = sg.send(mail)

        # Return a success message with status code
        if response.status_code == 202:
            return jsonify({"message": "Email sent successfully!", "status_code": response.status_code}), 200
        else:
            return jsonify({"message": "Failed to send email", "status_code": response.status_code, "response_body": response.body.decode()}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

