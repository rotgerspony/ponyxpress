
from twilio.rest import Client

def send_sms(body, to="+1234567890"):
    account_sid = "your_sid_here"
    auth_token = "your_token_here"
    client = Client(account_sid, auth_token)
    message = client.messages.create(body=body, from_="+15551234567", to=to)
    print("SMS sent:", message.sid)

# send_sms("Your package is out for delivery!")
