import os
import pickle
import base64
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.text import MIMEText
import logging

# Gmail API scopes 
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def authenticate_gmail():
    """Authenticate the Gmail API and return the service."""
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)

def create_email(sender, to, subject, body):
    """Create an email message."""
    message = MIMEText(body)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

def send_email(service, sender, to, subject, body):
    """Send an email using Gmail API."""
    email = create_email(sender, to, subject, body)
    try:
        message = service.users().messages().send(userId='me', body=email).execute()
        logging.info(f"Message sent: {message['id']}")
    except HttpError as error:
        logging.error(f"An error occurred while sending email: {error}")

def fetch_rbi_news():
    """Fetch RBI news. Replace with your actual implementation."""
    try:
        # Example: Replace with real API call or web scraping logic
        return "Today's RBI news: Placeholder for actual news."
    except Exception as e:
        logging.error(f"Failed to fetch RBI news: {e}")
        return "Failed to retrieve news."

if __name__ == '__main__':
    try:
        # Retrieve sender and recipient email from environment variables
        sender_email = os.environ.get('SENDER_EMAIL')
        recipient_email = os.environ.get('RECEIVER_EMAIL')

        if not sender_email or not recipient_email:
            logging.error("Environment variables SENDER_EMAIL or RECEIVER_EMAIL are not set.")
            exit(1)

        # Authenticate and get the Gmail API service
        service = authenticate_gmail()

        # Email details
        subject = "Daily RBI News"
        body = fetch_rbi_news()

        # Send the email
        send_email(service, sender_email, recipient_email, subject, body)

    except Exception as main_error:
        logging.error(f"An unexpected error occurred: {main_error}")
