# DDoS Mitigation Example using Flask and Rate Limiting
from flask import Flask, request, abort
import time
import logging

app = Flask(__name__)

# IP-based rate limiting dictionary
requests = {}

RATE_LIMIT = 100  # Maximum 100 requests per minute per IP
TIME_WINDOW = 60  # Time window in seconds

def check_rate_limit(ip):
    current_time = time.time()
    if ip not in requests:
        requests[ip] = [current_time]
        return True
    # Clean up old requests
    requests[ip] = [t for t in requests[ip] if current_time - t < TIME_WINDOW]
    # Check if the IP exceeded the rate limit
    if len(requests[ip]) >= RATE_LIMIT:
        return False
    requests[ip].append(current_time)
    return True

@app.route('/secure-device', methods=['GET'])
def secure_device():
    user_ip = request.remote_addr
    if not check_rate_limit(user_ip):
        abort(429, description="Rate limit exceeded.")
    return "IoT Device is secure!"

# Logging function to track DDoS attempts
logging.basicConfig(filename="ddos_logs.log", level=logging.INFO)

def log_ddos_attempt(ip):
    logging.info(f"DDoS attempt detected from IP: {ip}, time: {time.time()}")

if __name__ == '_main_':
    app.run(debug=True)