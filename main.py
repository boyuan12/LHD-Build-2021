"""
    Simplest Implmentation of sending a message using Twilio in Python
"""

import os
from twilio.rest import Client


account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
client = Client(account_sid, auth_token)

phone = input("Phone number: ")
message = input("Message: ")

try:
    client.messages.create(from_='+19162800623', body=message, to=phone)
    print("Message sent!")
except Exception as e:
    print(e)
