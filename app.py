from flask import Flask, render_template, jsonify, request
import requests

app = Flask(__name__)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,hi;q=0.8'
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/option-chain')
def get_option_chain():
    # फ्रंटएंड से इंडेक्स का नाम पकड़ेगा (NIFTY, BANKNIFTY, या SENSEX)
    symbol = request.args.get('symbol', 'NIFTY').upper()
    
    try:
        session = requests.Session()
        
        # NIFTY और BANKNIFTY के लिए NSE की वेबसाइट काम करेगी
        if symbol in ['NIFTY', 'BANKNIFTY']:
            session.get("https://www.nseindia.com", headers=HEADERS, timeout=10)
            url = f"https://www.nseindia.com/api/option-chain-indices?symbol={symbol}"
            response = session.get(url, headers=HEADERS, timeout=10)
            
        # SENSEX के लिए BSE की वेबसाइट का लॉजिक या कोई अन्य फ्री सोर्स लगेगा
        else:
            # (यदि आपकी HTML फ़ाइल सिर्फ टेस्टिंग के लिए बनी है तो यह मॉक सक्सेस रिस्पॉन्स दे देगा)
            return jsonify({"message": f"{symbol} data route active", "records": {"expiryDates": [], "data": []}})
        
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": f"Exchange Error: {response.status_code}"}), response.status_code
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
                        
