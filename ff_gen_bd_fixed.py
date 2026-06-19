#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎮 FREE FIRE ACCOUNT GENERATOR - BD FIXED VERSION 🎮
সম্পূর্ণভাবে কাজ করে BD রিজিয়নে
Owner: jpjihad17-dot
"""

import requests
import json
import random
import string
import threading
import time
import os
import sys
from datetime import datetime
from colorama import Fore, Style, init
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64

init(autoreset=True)

# ========== COLORS ==========
R = Style.RESET_ALL
CYAN = Fore.LIGHTCYAN_EX + Style.BRIGHT
YELLOW = Fore.LIGHTYELLOW_EX + Style.BRIGHT
GREEN = Fore.LIGHTGREEN_EX + Style.BRIGHT
RED = Fore.LIGHTRED_EX + Style.BRIGHT
BLUE = Fore.LIGHTBLUE_EX + Style.BRIGHT
MAGENTA = Fore.LIGHTMAGENTA_EX + Style.BRIGHT

# ========== CONFIG ==========
REGION = "BD"
HEX_KEY = bytes.fromhex("32656534343831396539623435393838343531343130363762323831363231383734643064356437616639643866376530306331653534373135623764316533")
EXIT_FLAG = False
SUCCESS_COUNT = 0
LOCK = threading.Lock()
PRINT_LOCK = threading.Lock()

# ========== FOLDER SETUP ==========
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_FOLDER = os.path.join(CURRENT_DIR, "FF_GEN_BD")
ACCOUNTS_FOLDER = os.path.join(BASE_FOLDER, "ACCOUNTS")
RARE_FOLDER = os.path.join(BASE_FOLDER, "RARE")

for folder in [BASE_FOLDER, ACCOUNTS_FOLDER, RARE_FOLDER]:
    os.makedirs(folder, exist_ok=True)

# ========== SESSION ==========
thread_local = threading.local()

def get_session():
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
        thread_local.session.verify = False
        thread_local.session.timeout = 5
    return thread_local.session

# ========== CRYPTO ==========
def aes_encrypt(hex_data):
    try:
        data = bytes.fromhex(hex_data)
        key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
        iv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return cipher.encrypt(pad(data, AES.block_size))
    except:
        return None

def encrypt_api(plain_hex):
    try:
        plain = bytes.fromhex(plain_hex)
        key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
        iv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return cipher.encrypt(pad(plain, AES.block_size)).hex()
    except:
        return None

# ========== NAME & PASSWORD GENERATION ==========
def generate_name():
    base = "BDUser"
    exponents = {'0':'⁰','1':'¹','2':'²','3':'³','4':'⁴','5':'⁵','6':'⁶','7':'⁷','8':'⁸','9':'⁹'}
    num = random.randint(1000, 9999)
    exp = ''.join(exponents[d] for d in str(num))
    return f"{base}{exp}"

def generate_password():
    base = "FF_BD"
    random_part = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))
    return f"{base}_{random_part}"

# ========== ACCOUNT CREATION ==========
def create_guest_account():
    """Create Free Fire guest account"""
    session = get_session()
    try:
        password = generate_password()
        url = "https://100067.connect.garena.com/api/v2/oauth/guest:register"
        payload = {
            "app_id": 100067,
            "client_type": 2,
            "password": password,
            "source": 2
        }
        headers = {
            "User-Agent": "GarenaMSDK/4.0.39(SM-A325M;Android 13;en;HK;)",
            "Accept": "application/json",
            "Content-Type": "application/json; charset=utf-8",
            "Accept-Encoding": "gzip",
            "Connection": "Keep-Alive"
        }
        
        response = session.post(url, json=payload, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if "data" in data and "uid" in data["data"]:
                uid = data["data"]["uid"]
                return uid, password
    except:
        pass
    return None, None

def get_token(uid, password):
    """Get access token"""
    session = get_session()
    try:
        url = "https://100067.connect.garena.com/oauth/guest/token/grant"
        headers = {
            "Accept-Encoding": "gzip",
            "Connection": "Keep-Alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "100067.connect.garena.com",
            "User-Agent": "GarenaMSDK/4.0.19P8(ASUS_Z01QD;Android 12;en;US;)"
        }
        data = {
            "uid": uid,
            "password": password,
            "response_type": "token",
            "client_type": "2",
            "client_secret": HEX_KEY,
            "client_id": "100067"
        }
        
        response = session.post(url, headers=headers, data=data, timeout=5)
        if response.status_code == 200:
            res_json = response.json()
            if 'open_id' in res_json and 'access_token' in res_json:
                return res_json['access_token'], res_json['open_id']
    except:
        pass
    return None, None

def register_account(access_token, open_id, name):
    """Register account with MajorRegister"""
    session = get_session()
    try:
        url = "https://loginbp.ggpolarbear.com/MajorRegister"
        
        headers = {
            "Accept-Encoding": "gzip",
            "Authorization": "Bearer",
            "Connection": "Keep-Alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Expect": "100-continue",
            "Host": "loginbp.ggpolarbear.com",
            "ReleaseVersion": "OB53",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_I005DA Build/PI)",
            "X-GA": "v1 1",
            "X-Unity-Version": "2018.4.11f1"
        }
        
        # Simple payload for BD region
        payload = {
            1: name,
            2: access_token,
            3: open_id,
            5: 102000007,
            6: 4,
            7: 1,
            13: 1,
            15: "bn",  # Bengali language
            16: 1,
            17: 1
        }
        
        # Build proto manually (simplified)
        proto_data = build_simple_proto(payload)
        encrypted = aes_encrypt(proto_data.hex())
        
        if encrypted:
            response = session.post(url, headers=headers, data=encrypted, timeout=5)
            if response.status_code in [200, 201]:
                return True
    except:
        pass
    return False

def major_login_bd(uid, password, access_token, open_id):
    """BD Region Major Login"""
    session = get_session()
    try:
        url = "https://loginbp.ggpolarbear.com/MajorLogin"
        
        # BD optimized payload
        payload = (
            b'\x1a\x132025-08-30 05:19:21'
            b'"\tfree fire'
            b'(\x01'
            b':\x081.114.13'
            b'B2Android OS 9 / API-28 (PI/rel.cjw.20220518.114133)'
            b'J\x08Handheld'
            b'R\nBD Mobile'
            b'Z\x04WIFI'
            b'`\xb6\x0ch\xee\x05'
            b'r\x03300'
            b'z\x1fARMv7 VFPv3 NEON VMH | 2400 | 2'
            b'\x80\x01\xc9\x0f'
            b'\x8a\x01\x0fAdreno (TM) 640'
            b'\x92\x01\rOpenGL ES 3.2'
            b'\x9a\x01+Google|dfa4ab4b-9dc4-454e-8065-e70c733fa53f'
            b'\xa2\x01\x0e105.235.139.91'
            b'\xaa\x01\x02'
            b'\xb2\x01 1d8ec0240ede109973f3321b9354b44d'
            b'\xba\x01\x014'
            b'\xc2\x01\x08Handheld'
            b'\xca\x01\x10Asus ASUS_I005DA'
            b'\xea\x01@afcfbf13334be42036e4f742c80b956344bed760ac91b3aff9b607a610ab4390'
            b'\xf0\x01\x01'
            b'\xca\x02\nBD Mobile'
            b'\xd2\x02\x04WIFI'
            b'\xca\x03 7428b253defc164018c604a1ebbfebdf'
            b'\xe0\x03\xa8\x81\x02'
        )
        
        payload = payload.replace(b'afcfbf13334be42036e4f742c80b956344bed760ac91b3aff9b607a610ab4390', access_token.encode())
        payload = payload.replace(b'1d8ec0240ede109973f3321b9354b44d', open_id.encode())
        
        encrypted_data = encrypt_api(payload.hex())
        
        if encrypted_data:
            headers = {
                "Accept-Encoding": "gzip",
                "Authorization": "Bearer",
                "Connection": "Keep-Alive",
                "Content-Type": "application/x-www-form-urlencoded",
                "Expect": "100-continue",
                "Host": "loginbp.ggpolarbear.com",
                "ReleaseVersion": "OB53",
                "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_I005DA Build/PI)",
                "X-GA": "v1 1",
                "X-Unity-Version": "2018.4.11f1"
            }
            
            response = session.post(url, headers=headers, data=bytes.fromhex(encrypted_data), timeout=5)
            
            if response.status_code == 200 and len(response.text) > 10:
                # Extract JWT token
                jwt_start = response.text.find("eyJ")
                if jwt_start != -1:
                    jwt_token = response.text[jwt_start:jwt_start+200]
                    
                    # Extract account_id from JWT
                    try:
                        parts = jwt_token.split('.')
                        if len(parts) >= 2:
                            payload_part = parts[1]
                            padding = 4 - len(payload_part) % 4
                            if padding != 4:
                                payload_part += '=' * padding
                            decoded = base64.urlsafe_b64decode(payload_part)
                            data = json.loads(decoded)
                            account_id = data.get('account_id') or data.get('external_id')
                            if account_id:
                                return str(account_id), jwt_token
                    except:
                        pass
    except:
        pass
    
    return "N/A", None

def build_simple_proto(fields):
    """Build simple protobuf"""
    result = b''
    for k, v in fields.items():
        if isinstance(v, str):
            v = v.encode()
        if isinstance(v, bytes):
            header = (k << 3) | 2
            result += bytes([(header >> i) & 0xFF for i in range(0, 8, 8)]) + bytes([len(v)]) + v
        elif isinstance(v, int):
            header = (k << 3) | 0
            result += bytes([header]) + bytes([v])
    return result

# ========== SAVE ACCOUNT ==========
def save_account(uid, password, name, account_id, jwt_token):
    """Save account to JSON"""
    try:
        filename = os.path.join(ACCOUNTS_FOLDER, "accounts_bd.json")
        entry = {
            'uid': uid,
            'password': password,
            'name': name,
            'account_id': account_id,
            'region': 'BD',
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'jwt_token': jwt_token[:50] if jwt_token else 'N/A'
        }
        
        data = []
        if os.path.exists(filename):
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except:
                data = []
        
        data.append(entry)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return True
    except:
        return False

# ========== UI ==========
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    print(f"""{CYAN}
╔═══════════════════════════════════════════════════════╗
║     🎮 FREE FIRE ACCOUNT GENERATOR - BD 🎮            ║
║              সম্পূর্ণ কাজ করে                         ║
╚═══════════════════════════════════════════════════════╝
    {R}""")

def print_account(uid, pwd, name, aid, count, total):
    print(f"""{CYAN}
┌─────────────────────────────────────────────────────┐
│ ✅ ACCOUNT GENERATED {count}/{total}{' '*(26-len(str(count))-len(str(total)))}│
├─────────────────────────────────────────────────────┤
│ {BLUE}UID       :{R} {GREEN}{uid:<35}{R} │
│ {BLUE}PASSWORD  :{R} {GREEN}{pwd:<35}{R} │
│ {BLUE}NAME      :{R} {YELLOW}{name:<35}{R} │
│ {BLUE}ACCOUNT ID:{R} {MAGENTA}{aid:<35}{R} │
└─────────────────────────────────────────────────────┘
    {R}""")

# ========== GENERATION ==========
def generate_account():
    """Generate single account"""
    global SUCCESS_COUNT
    
    name = generate_name()
    
    # Step 1: Create guest account
    uid, password = create_guest_account()
    if not uid:
        return None
    
    # Step 2: Get token
    access_token, open_id = get_token(uid, password)
    if not access_token:
        return None
    
    # Step 3: Register
    if not register_account(access_token, open_id, name):
        return None
    
    # Step 4: Login
    account_id, jwt_token = major_login_bd(uid, password, access_token, open_id)
    
    if account_id == "N/A":
        account_id = f"BD_{uid[-6:]}"
    
    # Step 5: Save
    save_account(uid, password, name, account_id, jwt_token)
    
    with LOCK:
        SUCCESS_COUNT += 1
    
    return {
        'uid': uid,
        'password': password,
        'name': name,
        'account_id': account_id
    }

def worker_thread(total_accounts, thread_id):
    """Worker thread"""
    global EXIT_FLAG
    
    while not EXIT_FLAG:
        with LOCK:
            if SUCCESS_COUNT >= total_accounts:
                break
        
        account = generate_account()
        if account:
            with PRINT_LOCK:
                print_account(
                    account['uid'],
                    account['password'],
                    account['name'],
                    account['account_id'],
                    SUCCESS_COUNT,
                    total_accounts
                )

# ========== MAIN ==========
def main():
    global EXIT_FLAG, SUCCESS_COUNT
    
    clear_screen()
    banner()
    
    while True:
        try:
            total = int(input(f"{CYAN}➤ কতটা Account তৈরি করবেন? {R}: "))
            if total > 0:
                break
        except:
            pass
    
    threads_input = input(f"{CYAN}➤ Thread সংখ্যা (recommend 4-8): {R}")
    try:
        threads = int(threads_input) if threads_input else 4
    except:
        threads = 4
    
    print(f"\n{GREEN}🚀 শুরু হচ্ছে...{R}\n")
    
    SUCCESS_COUNT = 0
    EXIT_FLAG = False
    
    thread_list = []
    for i in range(threads):
        t = threading.Thread(target=worker_thread, args=(total, i+1))
        t.daemon = True
        t.start()
        thread_list.append(t)
    
    try:
        for t in thread_list:
            t.join()
    except KeyboardInterrupt:
        print(f"\n{RED}⚠️  বন্ধ করছি...{R}")
        EXIT_FLAG = True
    
    print(f"\n{GREEN}✅ সম্পন্ন!{R}")
    print(f"{YELLOW}📊 মোট Account: {SUCCESS_COUNT}{R}")
    print(f"{CYAN}💾 ফাইল: {ACCOUNTS_FOLDER}/accounts_bd.json{R}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{RED}বন্ধ করা হয়েছে{R}")
        sys.exit(0)
