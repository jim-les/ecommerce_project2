import base64
import requests
from datetime import datetime

# M-Pesa API base URLs
BASE_URL = "https://sandbox.safaricom.co.ke"
TOKEN_URL = f"{BASE_URL}/oauth/v1/generate?grant_type=client_credentials"
STK_PUSH_URL = f"{BASE_URL}/mpesa/stkpush/v1/processrequest"

def get_access_token():
    consumer_key = "L7Tt0YnuxqNJkzaV5O6C9JUGKY1Ga1hctYytNeDCqjcPm1lq"
    consumer_secret = "YEhWMayqsAiomlDTV2VcEa8fnrWyahnDHg5rvmmpecZdMO1NiUB9kUxA1bstAAZL"
    auth = base64.b64encode(f"{consumer_key}:{consumer_secret}".encode()).decode()

    try:
        response = requests.get(TOKEN_URL, headers={"Authorization": f"Basic {auth}"})
        response.raise_for_status()
        return response.json().get("access_token")
    except requests.exceptions.RequestException as e:
        print("Error getting access token:", e)
        raise


# Function to generate the M-Pesa password
def generate_password():
    business_shortcode = 174379
    passkey = "1234AsEn"
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    password = base64.b64encode(f"{business_shortcode}{passkey}{timestamp}".encode()).decode()
    return password, timestamp

# Function to initiate an STK Push
def simulate_mpesa_express(amount, phone_number):
    business_shortcode = 174379
    callback_url = "https://web hook.site/1f1b1b1d-0b7b-4b7b-8b7b-1b7b1b7b1b7b"

    try:
        token = get_access_token()
        print("Access Token:", token)

        password, timestamp = generate_password()
        print("M-Pesa Password:", password + "\nTimestamp:", timestamp)

        request_data = {
            "BusinessShortCode": 174379,
            "Password": "MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMjQxMjMxMDk1MTM5",
            "Timestamp": "20241231095139",
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": '254113159363',  # Customer's phone number
            "PartyB": 174379,
            "PhoneNumber": phone_number,
            "CallBackURL": 'https://mydomain.com/path',
            "AccountReference": "Azanona",
            "TransactionDesc": "Test Payment",
        }

        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(STK_PUSH_URL, json=request_data, headers=headers)
        response.raise_for_status()

        print("M-Pesa Express Response:", response.json())
    except requests.exceptions.RequestException as e:
        print("Error simulating M-Pesa Express:", e)
        raise

if __name__ == "__main__":
    try :
        simulate_mpesa_express(100, '254113159363')
    except Exception as e:
        print("Error:", e)
        raise