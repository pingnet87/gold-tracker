import sqlite3
from datetime import datetime
import ndef
import nfc

def get_latest_prices():
    conn = sqlite3.connect('prices.db')
    cursor = conn.cursor()
    cursor.execute("SELECT gold, usd_iqd FROM prices ORDER BY id DESC LIMIT 1")
    result = cursor.fetchone()
    conn.close()
    return result if result else (1950.50, 1450.00)

def write_nfc_tag():
    gold_price, usd_iqd = get_latest_prices()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    records = [
        ndef.UriRecord(f"http://localhost:5000?gold={gold_price}&usd={usd_iqd}"),
        ndef.TextRecord(f"أسعار الذهب: {gold_price} USD | الدولار: {usd_iqd} IQD")
    ]
    
    with nfc.ContactlessFrontend('usb') as clf:
        print("الرجاء تقريب بطاقة NFC الآن...")
        tag = clf.connect(rdwr={'on-connect': lambda tag: False})
        
        if tag.ndef:
            tag.ndef.records = records
            print("تم كتابة البيانات على البطاقة بنجاح!")
        else:
            print("البطاقة لا تدعم NDEF!")

if __name__ == '__main__':
    write_nfc_tag()