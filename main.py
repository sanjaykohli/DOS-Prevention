from flask import Flask, request, jsonify
import time
from collections import defaultdict

app = Flask(__name__)

# Dictionary to keep track of IP request timestamps
request_log = defaultdict(list)

# Define a rate limit (e.g., 100 requests per 60 seconds)
RATE_LIMIT = 2
RATE_LIMIT_PERIOD = 60  # in seconds

def is_rate_limited(ip):
    current_time = time.time()
    timestamps = request_log[ip]
    
    # Remove timestamps older than RATE_LIMIT_PERIOD
    timestamps = [t for t in timestamps if current_time - t < RATE_LIMIT_PERIOD]
    request_log[ip] = timestamps
    
    if len(timestamps) >= RATE_LIMIT:
        return True
    return False

@app.route('/')
def index():
    ip = request.remote_addr
    
    if is_rate_limited(ip):
        return jsonify({'error': 'Rate limit exceeded'}), 429
    
    # Log the current request
    request_log[ip].append(time.time())
    
    return jsonify({'message': 'Request successful'}), 200

if __name__ == '__main__':
    app.run(debug=True)
