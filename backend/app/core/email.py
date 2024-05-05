import os
import pickle
import base64
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def create_service(client_secret_file, api_name, api_version, *scopes):
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]

    cred = None
    pickle_file = os.getenv('GMAIL_TOKEN_PATH', 'gmail_token.pickle')

    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()

        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)
    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        return service
    except Exception as e:
        print('Unable to connect.')
        print(e)
        return None


def send_email(data):
    service = create_service(
        os.getenv('GMAIL_SECRET_PATH', 'gmail_creds.json'),
        'gmail',
        'v1',
        ['https://mail.google.com/']
    )

    emailMsg = data['body']
    mimeMessage = MIMEMultipart()
    mimeMessage['to'] = data['to_email']
    mimeMessage['subject'] = data['subject']
    mimeMessage.attach(MIMEText(emailMsg, 'html'))
    raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()

    message = service.users().messages().send(userId='me', body={'raw': raw_string}).execute()
    return message

