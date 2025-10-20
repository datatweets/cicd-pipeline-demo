# app.py
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/hello/<name>')
def hello(name):
    """Return a personalized greeting."""
    return jsonify({'message': f'Hello, {name}!'})

@app.route('/health')
def health():
    """Health check endpoint for monitoring."""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    # Run the application
    # Note: In production, use a proper WSGI server like Gunicorn
    app.run(host='0.0.0.0', port=5000)
