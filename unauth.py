import os
import time
import logging
import requests
from tkinter import *
from tkinter import messagebox, scrolledtext
from requests_oauthlib import OAuth2Session
from ratelimit import limits, sleep_and_retry
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("THIRD_PARTY_API_KEY")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TOKEN_URL = "https://api.example.com/oauth/token"
API_URL = "https://api.example.com/secure-data"

# Configure logging
logging.basicConfig(filename="api_access.log", level=logging.INFO)

# OAuth2 Setup
def get_oauth_session():
    oauth = OAuth2Session(CLIENT_ID)
    token = oauth.fetch_token(
        TOKEN_URL,
        client_secret=CLIENT_SECRET
    )
    return OAuth2Session(CLIENT_ID, token=token)

# Rate limiting configuration: 5 requests per minute
@sleep_and_retry
@limits(calls=5, period=60)
def fetch_data_with_security():
    try:
        # OAuth2 Session setup
        session = get_oauth_session()
        
        # Secure headers
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        
        # Make a secure HTTPS request
        response = session.get(API_URL, headers=headers)
        
        # Log the API access
        logging.info(f"API request made to {API_URL} with status code {response.status_code}")
        
        # Raise an error for non-200 responses
        response.raise_for_status()
        
        # Validate and return data
        data = response.json()
        if not validate_data(data):
            raise ValueError("Data validation failed")
        
        return data

    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
        messagebox.showerror("Error", f"HTTP error: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logging.error(f"Request error occurred: {req_err}")
        messagebox.showerror("Error", f"Request error: {req_err}")
    except Exception as err:
        logging.error(f"Other error occurred: {err}")
        messagebox.showerror("Error", f"An error occurred: {err}")

# Data validation function to verify expected keys in response
def validate_data(data):
    required_keys = ["id", "value", "timestamp"]  # Example keys
    return all(key in data for key in required_keys)

# Function to securely fetch data and display in the GUI
def fetch_and_display_data():
    data = fetch_data_with_security()
    if data:
        result_text.delete(1.0, END)  # Clear previous data
        result_text.insert(END, str(data))  # Display new data

# Create GUI with Tkinter
root = Tk()
root.title("Secure IoT API Fetcher")
root.geometry("600x400")

# Title label
Label(root, text="IoT API Secure Data Fetcher", font=("Arial", 16)).pack(pady=10)

# Fetch data button
fetch_button = Button(root, text="Fetch Secure Data", font=("Arial", 12), command=fetch_and_display_data)
fetch_button.pack(pady=5)

# Text area to display fetched data
result_text = scrolledtext.ScrolledText(root, width=70, height=15, font=("Arial", 10))
result_text.pack(pady=10)

# Run the main Tkinter loop
root.mainloop()