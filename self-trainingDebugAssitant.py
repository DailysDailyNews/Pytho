import argparse
from flask import Flask, request, abort, jsonify
from sklearn.ensemble import RandomForestClassifier
import numpy as np

app = Flask(__name__)
app.debug = True
# Allowed IPs for simplicity, you can expand this list
allowed_ips = ['127.0.0.1']

# Placeholder for training data
training_data = []
training_labels = []

@app.before_request
def limit_remote_addr():
    if request.remote_addr not in allowed_ips:
        abort(403)  # Forbidden

@app.route('/')
def home():
    return "Welcome to the secure site!"

@app.route('/log', methods=['POST'])
def log_data():
    data = request.json
    training_data.append([data['type'], data['target'], data['timestamp']])
    training_labels.append(1)  # Placeholder label, adjust as needed
    return jsonify(success=True)

@app.route('/train', methods=['POST'])
def train_model():
    if len(training_data) < 10:
        return jsonify(success=False, message="Not enough data to train the model")

    X = np.array(training_data)
    y = np.array(training_labels)
    model = RandomForestClassifier()
    model.fit(X, y)
    return jsonify(success=True, message="Model trained successfully")

@app.errorhandler(403)
def forbidden(error):
    return "Access forbidden: You don't have permission to access this resource.", 403

@app.errorhandler(404)
def page_not_found(error):
    return "Page not found: The requested URL was not found on the server.", 404

@app.errorhandler(500)
def internal_server_error(error):
    return "Internal server error: An unexpected error occurred.", 500

def run_server(host, port):
    app.run(host=host, port=port)

def main():
    parser = argparse.ArgumentParser(description="Security Bot for Website")
    parser.add_argument('--host', type=str, default='127.0.0.1', help='Host to run the server on')
    parser.add_argument('--port', type=int, default=5000, help='Port to run the server on')
    args = parser.parse_args()

    run_server(args.host, args.port)

if __name__ == '__main__':
    main()
