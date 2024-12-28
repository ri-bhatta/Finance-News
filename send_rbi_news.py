import os
import pickle
import base64
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.text import MIMEText

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

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
        print(f"Message sent: {message['id']}")
    except HttpError as error:
        print(f"An error occurred: {error}")

def search_rbi_news():
    """Dummy function to get news. Replace with your actual code."""
    return "Today's RBI news: Placeholder for actual news."

if __name__ == '__main__':
    # Retrieve sender and recipient email from environment variables
    sender_email = os.environ['SENDER_EMAIL']
    recipient_email = os.environ['RECEIVER_EMAIL']

    # Authenticate and get the Gmail API service
    service = authenticate_gmail()

    # Email details
    subject = "Daily RBI News"
    body = search_rbi_news()

    # Send the email
    send_email(service, sender_email, recipient_email, subject, body)
