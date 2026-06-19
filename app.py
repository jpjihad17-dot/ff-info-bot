from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv
import json

# লোড এনভায়রনমেন্ট ভেরিয়েবল
load_dotenv()

app = Flask(__name__)
CORS(app)

# API কনফিগারেশন
RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY')
RAPIDAPI_HOST = os.getenv('RAPIDAPI_HOST', 'freefire-api.p.rapidapi.com')

# ডামি ডেটা (যতক্ষণ API Key যোগ না করা হয়)
DUMMY_PLAYER_DATA = {
    "status": "success",
    "data": {
        "uid": "123456789",
        "name": "টেস্ট প্লেয়ার",
        "level": 45,
        "experience": 5000000,
        "continent": "AS",
        "rank": "Diamond",
        "rank_points": 8500,
        "kills": 1250,
        "deaths": 450,
        "headshots": 320,
        "matches": 2000,
        "wins": 450,
        "win_rate": 22.5,
        "kd_ratio": 2.78,
        "avatar_url": "https://via.placeholder.com/150",
        "status": "অনলাইন"
    }
}

# হোম পেজ
@app.route('/')
def index():
    return render_template('index.html')

# প্লেয়ার সার্চ API
@app.route('/api/player/<uid>', methods=['GET'])
def search_player(uid):
    try:
        # যদি API Key না থাকে, ডামি ডেটা রিটার্ন করুন
        if not RAPIDAPI_KEY or RAPIDAPI_KEY == 'your_api_key_here':
            return jsonify({
                "success": True,
                "message": "ডামি ডেটা (API Key সেট করলে রিয়েল ডেটা পাবেন)",
                "data": DUMMY_PLAYER_DATA["data"]
            })
        
        # রিয়েল API কল
        url = f"https://{RAPIDAPI_HOST}/player/{uid}"
        headers = {
            "x-rapidapi-key": RAPIDAPI_KEY,
            "x-rapidapi-host": RAPIDAPI_HOST
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            return jsonify({
                "success": True,
                "data": response.json()
            })
        else:
            return jsonify({
                "success": False,
                "error": "প্লেয়ার খুঁজে পাওয়া যায়নি",
                "status_code": response.status_code
            }), 404
            
    except requests.exceptions.Timeout:
        return jsonify({
            "success": False,
            "error": "API রিকোয়েস্ট টাইমআউট হয়েছে"
        }), 504
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# স্টেটাস চেক
@app.route('/api/status', methods=['GET'])
def status():
    api_status = "সংযুক্ত" if RAPIDAPI_KEY and RAPIDAPI_KEY != 'your_api_key_here' else "API Key প্রয়োজন"
    
    return jsonify({
        "status": "চলমান",
        "api_status": api_status,
        "version": "1.0.0"
    })

# সব গাইড
@app.route('/api/guides', methods=['GET'])
def get_guides():
    guides = [
        {
            "id": 1,
            "title": "নতুন খেলোয়াড়দের জন্য টিপস",
            "description": "Free Fire খেলা শুরু করার আগে যা জানতে হবে",
            "category": "শিক্ষানবিস"
        },
        {
            "id": 2,
            "title": "অস্ত্র নির্বাচনের সঠিক উপায়",
            "description": "বিভিন্ন পরিস্থিতিতে কোন অস্ত্র ব্যবহার করবেন",
            "category": "কৌশল"
        },
        {
            "id": 3,
            "title": "ম্যাপ নেভিগেশন গাইড",
            "description": "সব ম্যাপের গুরুত্বপূর্ণ স্থানগুলি জানুন",
            "category": "মানচিত্র"
        }
    ]
    return jsonify({
        "success": True,
        "data": guides
    })

# এরর হ্যান্ডলিং
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": "পেজ খুঁজে পাওয়া যায়নি"
    }), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({
        "success": False,
        "error": "সার্ভার এরর"
    }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
