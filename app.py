from flask import Flask, jsonify
import requests

app = Flask(__name__)

# NSE वेबसाइट के लिए सही Headers ताकि Request ब्लॉक न हो
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,hi;q=0.8'
}

@app.route('/')
def home():
    return "NSE Option Chain API is Live! Go to /option-chain to see data."

@app.route('/option-chain')
def get_option_chain():
    try:
        # 1. पहले होमपेज पर जाकर Cookies सेट करना ज़रूरी है
        session = requests.Session()
        session.get("https://www.nseindia.com", headers=HEADERS, timeout=10)
        
        # 2. अब असली Option Chain API एंडपॉइंट को हिट करें
        url = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"
        response = session.get(url, headers=HEADERS, timeout=10)
        
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": f"NSE responded with status code {response.status_code}"}), response.status_code
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
                           
