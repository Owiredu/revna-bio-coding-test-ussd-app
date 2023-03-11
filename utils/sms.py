import requests
from config import MNOTIFY_SMS_API_KEY


def send_sms(phone_number: str, message: str) -> None:
    """Send SMS to a recipient phone number

    Args:
        phone_number (str): The recipient's phone number
        message (str): The message content
    """
    # compose the request URL, appending the API key to it as a query parameter
    url = "https://api.mnotify.com/api/sms/quick" + "?key=" + MNOTIFY_SMS_API_KEY
    # compose the request data
    data = {
        "recipient[]": [phone_number],
        "sender": "UniBase",
        "message": message,
        'is_schedule': False,
        'schedule_date': ''
    }
    # send the SMS request
    response = requests.post(url, data)
    # handle the response
    if response.status_code == 200:
        data = response.json()
        if data.get("status") == "success":
            print("SMS sent successfully")
        else:
            print("Failed to send SMS")
    else:
        print("Failed to send SMS")