from flask import Flask, jsonify, send_from_directory
import os

app = Flask(__name__, static_folder='static')

@app.route('/')
def serve_index():
    return send_from_directory('templates', 'index.html')

@app.route('/api/prices')
def get_prices():
    return jsonify({
        "gold_price": 1950.50,
        "usd_iqd_rate": 1450.00,
        "timestamp": "2025-08-15 15:00:00"
    })

if __name__ == '__main__':
    app.run(debug=True)
