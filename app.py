from flask import Flask, render_template, jsonify
import sqlite3
from datetime import datetime
import requests

app = Flask(__name__)

# مصادر البيانات (ستحتاج إلى استبدالها بمصادر حقيقية)
GOLD_API_URL = "https://api.goldapi.io/api/XAU/USD"
GOLD_API_KEY = "your_gold_api_key"
EXCHANGE_API_URL = "https://api.exchangerate.host/convert?from=USD&to=IQD"

def get_db_connection():
    conn = sqlite3.connect('prices.db')
    conn.row_factory = sqlite3.Row
    return conn

def fetch_gold_price():
    try:
        headers = {"x-access-token": GOLD_API_KEY}
        response = requests.get(GOLD_API_URL, headers=headers)
        return response.json()['price']
    except:
        # قيمة افتراضية في حالة فشل الاتصال
        return 1950.50

def fetch_usd_iqd_rate():
    try:
        response = requests.get(EXCHANGE_API_URL)
        return round(response.json()['result'], 2)
    except:
        # قيمة افتراضية في حالة فشل الاتصال
        return 1450.00

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/prices')
def get_prices():
    gold_price = fetch_gold_price()
    usd_iqd = fetch_usd_iqd_rate()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # حفظ البيانات في قاعدة البيانات
    conn = get_db_connection()
    conn.execute("INSERT INTO prices (gold, usd_iqd, timestamp) VALUES (?, ?, ?)",
                (gold_price, usd_iqd, timestamp))
    conn.commit()
    conn.close()
    
    return jsonify({
        'gold_price': gold_price,
        'usd_iqd_rate': usd_iqd,
        'timestamp': timestamp
    })

if __name__ == '__main__':
    # إنشاء قاعدة البيانات إذا لم تكن موجودة
    conn = sqlite3.connect('prices.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS prices
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  gold REAL NOT NULL,
                  usd_iqd REAL NOT NULL,
                  timestamp TEXT NOT NULL)''')
    conn.close()
    
    app.run(debug=True)