# ইনস্টলেশন গাইড 🚀

## প্রয়োজনীয়তা

- Python 3.7 বা উপরে
- pip (Python প্যাকেজ ম্যানেজার)
- Git

## ধাপে ধাপে ইনস্টলেশন

### ১. রিপোজিটরি ক্লোন করুন

```bash
git clone https://github.com/jpjihad17-dot/ff-info-bot.git
cd ff-info-bot
```

### ২. ভার্চুয়াল এনভায়রনমেন্ট তৈরি করুন

**Linux/Mac এর জন্য:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows এর জন্য:**
```bash
python -m venv venv
venv\Scripts\activate
```

### ৩. ডিপেন্ডেন্সি ইনস্টল করুন

```bash
pip install -r requirements.txt
```

### ৪. এনভায়রনমেন্ট ভেরিয়েবল ��েটআপ করুন

`.env.example` ফাইলটি `.env` এ কপি করুন:

```bash
cp .env.example .env
```

অথবা Windows এ:
```bash
copy .env.example .env
```

### ৫. API Key যোগ করুন (ঐচ্ছিক)

**Free Fire API Key পেতে:**

1. [RapidAPI](https://rapidapi.com) এ যান এবং সাইন আপ করুন
2. "Free Fire API" খুঁজুন
3. API Key এবং Host পান
4. `.env` ফাইলে যোগ করুন:

```
RAPIDAPI_KEY=আপনার_api_key_এখানে
RAPIDAPI_HOST=freefire-api.p.rapidapi.com
```

**নোট:** API Key ছাড়াই বট চলবে, তবে ডামি ডেটা দেখাবে।

### ৬. অ্যাপ্লিকেশন চালান

```bash
python app.py
```

ব্রাউজারে খুলুন: `http://localhost:5000`

## সমস্যা সমাধান

### সমস্যা: "Command 'python' not found"
**সমাধান:** `python3` ব্যবহার করুন অথবা Python সঠিকভাবে ইনস্টল করুন

### সমস্যা: "No module named 'flask'"
**সমাধান:** নিশ্চিত করুন যে ভার্চুয়াল এনভায়রনমেন্ট সক্রিয় এবং `pip install -r requirements.txt` চালিয়েছেন

### সমস্যা: Port 5000 ব্যবহৃত হচ্ছে
**সমাধান:** `app.py` এ পোর্ট নম্বর পরিবর্তন করুন:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # 5000 থেকে 5001 এ পরিবর্তন করুন
```

## ডিপ্লয়মেন্ট

### Heroku এ ডিপ্লয় করতে:

1. Heroku অ্যাকাউন্ট তৈরি করুন
2. Heroku CLI ইনস্টল করুন
3. নিম্নলিখিত কমান্ড চালান:

```bash
heroku login
heroku create আপনার_অ্যাপ_নাম
git push heroku main
```

### Netlify এ স্ট্যাটিক ফাইল হোস্ট করতে:

1. `static` ফোল্ডার Netlify এ আপলোড করুন
2. API কল সঠিক ডোমেইনে পয়েন্ট করুন

## যোগাযোগ

যেকোনো সমস্যার জন্য GitHub Issues এ রিপোর্ট করুন।

---

**Happy Gaming!** 🎮
