# Free Fire Info Bot 🎮

একটি সম্পূর্ণ Free Fire তথ্য বট যা Python Flask দিয়ে তৈরি।

## ফিচার ✨

- 🔍 প্লেয়ার ইনফরমেশন সার্চ
- 📊 স্ট্যাটিস্টিকস এবং র‍্যাঙ্ক
- 🎯 ক্যারেক্টার ইনফো
- 📱 রেসপন্সিভ ডিজাইন
- 🇧🇩 সম্পূর্ণ বাংলা সাপোর্ট

## প্রযুক্তি 🛠️

- **Backend**: Python Flask
- **Frontend**: HTML, CSS, JavaScript
- **API**: Free Fire API (RapidAPI)
- **Database**: JSON (স্টার্টিং এ)

## ইনস্টলেশন 📦

```bash
# প্রজেক্ট ক্লোন করুন
git clone https://github.com/jpjihad17-dot/ff-info-bot.git
cd ff-info-bot

# ভার্চুয়াল এনভায়রনমেন্ট তৈরি করুন
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# ডিপেন্ডেন্সি ইনস্টল করুন
pip install -r requirements.txt

# সার্ভার চালান
python app.py
```

## ব্যবহার 🎯

1. ব্রাউজারে খুলুন: `http://localhost:5000`
2. প্লেয়ার ইউআইডি দিয়ে সার্চ করুন
3. সম্পূর্ণ ইনফরমেশন পাবেন

## API Key সেটআপ 🔑

1. [RapidAPI](https://rapidapi.com) এ সাইন আপ করুন
2. Free Fire API খুঁজে নিন
3. `.env` ফাইলে আপনার API Key যোগ করুন:

```
RAPIDAPI_KEY=your_api_key_here
RAPIDAPI_HOST=your_api_host_here
```

## ফাইল স্ট্রাকচার 📁

```
ff-info-bot/
├── app.py                 # মেইন Flask অ্যাপ্লিকেশন
├── requirements.txt       # পাইথন ডিপেন্ডেন্সি
├── .env.example          # এনভায়রনমেন্ট ভেরিয়েবল টেমপ্লেট
├── templates/
│   └── index.html        # মেইন পেজ
├── static/
│   ├── css/
│   │   └── style.css     # স্টাইলশীট
│   └── js/
│       └── script.js     # জাভাস্ক্রিপ্ট
└── README.md
```

## লাইসেন্স 📄

MIT License

## যোগাযোগ 📧

যেকোনো সমস্যা বা পরামর্শের জন্য Issue তৈরি করুন!

---

**Happy Gaming!** 🎮🇧🇩
