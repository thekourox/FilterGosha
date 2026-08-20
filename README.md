# 📖 دفترچه راهنمای کار با فیلترگشا (FilterGosha)

<div align="center">

![Version](https://img.shields.io/badge/FilterGosha-v1.3.3-10b981?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Lifespan_Core-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram-@FilterGosha-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)

</div>

---

## 🚀 ۱. راه‌اندازی سریع سرور

### روش پیشنهادی: استقرار روی Railway
1. مخزن را در گیت‌هاب خود **Fork** کنید.
2. در سایت [Railway.app](https://railway.app) روی **New Project → Deploy from GitHub repo** کلیک کرده و مخزن خود را انتخاب کنید.
3. در تنظیمات سرویس، از بخش **Volumes** یک مسیر ماندگار به آدرس `/data` ایجاد و متصل کنید (ضروری برای ذخیره همیشگی دیتابیس).
4. در بخش **Networking** یک Public Domain به برنامه اختصاص دهید.

### روش Docker
```bash
docker run -d \
  --name filtergosha \
  -p 9890:9890 \
  -p 1080:1080 \
  -v $(pwd)/data:/data \
  -e ADMIN_PASSWORD="YourPassword" \
  --restart unless-stopped \
  $(docker build -q .)
```

### روش اجرای مستقیم با پایتون
```bash
pip install -r requirements.txt
python -m uvicorn main:app --host 0.0.0.0 --port 9890
```

---

## 🔑 ۲. اطلاعات و ورود به پنل

- **آدرس ورود:** `https://your-domain.com/login` یا `http://SERVER_IP:9890/login`
- **رمز عبور پیش‌فرض:** `FilterGoshaKING`

---

## 🛠️ ۳. راهنمای ساخت کانفیگ‌ها (نودها)

از منوی «کانفیگ‌ها» روی **«کانفیگ جدید»** کلیک کرده و پروتکل مورد نظر را انتخاب نمایید:

| نوع کانفیگ | کاربرد اصلی | تنظیمات شبکه |
| :--- | :--- | :--- |
| **WebSocket** | بهترین گزینه برای عبور از ورکر کلادفلر | پشتیبانی از uTLS، Fragment و Clean IP |
| **gRPC** | پینگ بسیار پایین با مالتی‌پلکسینگ HTTP/2 | پورت 443 و ALPN پیش‌فرض `h2` |
| **XHTTP** | متد جدید Xray (انشعاب خودکار پکت) | پایدار در برابر فیلترینگ شدید |
| **SOCKS5** | اتصال مستقیم تلگرام، کنسول، ویندوز و نرم‌افزارها | پورت TCP مستقل (1080) با نام‌کاربری ۶ رقمی |
| **کاستوم** | تعریف پروکسی‌های خارجی یا لینک‌های اختصاصی | پشتیبانی از متغیرهای `{host}` و `{username}` |

---

## 👥 ۴. راهنمای مدیریت اشتراک‌ها (ساب‌ها)

1. به بخش **«اشتراک‌ها»** بروید و روی **«اشتراک جدید»** کلیک کنید.
2. نام، حجم مجاز (GB)، تعداد روز اعتبار، محدودیت تعداد آی‌پی و سرعت (Mbps) را مشخص کنید.
3. تیک کانفیگ‌هایی که مایلید به این اشتراک متصل باشند را فعال کرده و ذخیره نمایید.
4. **لینک ساب اختصاصی (`/sub/{id}`):**
   - **برای کلاینت‌ها (v2rayNG, Sing-Box, Hiddify, NekoBox, Shadowrocket):** کپی کردن لینک ساب و الصاق مستقیم در برنامه.
   - **برای کاربر:** ارسال لینک ساب به کاربر برای باز کردن در مرورگر و مشاهده‌ی حجم باقی‌مانده، وضعیت مصرف، تاریخ انقضا و نام‌کاربری اختصاصی SOCKS5.

---

## ⚙️ ۵. متغیرهای محیطی (Environment Variables)

| نام متغیر | کاربرد | مقدار پیش‌فرض |
| :--- | :--- | :--- |
| `ADMIN_PASSWORD` | تغییر کلمه عبور ورود به پنل | `FilterGoshaKING` |
| `DATA_DIR` | مسیر فایل دیتابیس SQLite | `/data` |
| `WORKER_DOMAIN` | آدرس دامنه کلادفلر ورکر | *(خالی)* |
| `CLEAN_IP` | آی‌پی تمیز پیش‌فرض کلاینت‌ها | *(خالی)* |
| `REMARK_PREFIX` | پیشوند متنی اول نام لینک‌ها | `FilterGosha` |

---

## 💖 ۶. حمایت مالی (Donation)

توسعه و نگهداری این پروژه به صورت کاملاً متن‌باز انجام می‌شود. در صورت تمایل می‌توانید از طریق آدرس‌های رمزارز زیر از پروژه حمایت کنید:

- **USDT (BEP20):**  
  `0xd593ae9D32bEA690EC62460C54BF3951aFFF7803`

- **USDT (TRC20):**  
  `THaaHzoTwXfUfcrtYTDXRsMmk9qhnXa56M`

---

## 📢 پشتیبانی و ارتباط

- **کانال رسمی تلگرام:** [@FilterGosha](https://t.me/FilterGosha)
- **گزارش مشکلات:** [GitHub Issues](https://github.com/thekourox/FilterGosha/issues)

---

## 📜 Version Changelog (Release History)

### 🔹 v1.3.3 (Current Release)
- **Feature:** Introduced native direct TCP SOCKS5 server with 6-character short username authentication.
- **Feature:** Added dedicated SOCKS5 protocol selector cards in the admin dashboard.
- **UI/UX:** Automated form clean-up for SOCKS5 by auto-hiding redundant TLS/Fragment anti-filtering fields.
- **UI/UX:** Added short SOCKS5 username display box on client subscription web pages.
- **Fix:** Fixed protocol validation falling back to `vless-grpc` upon saving SOCKS5 configurations.

### 🔹 v1.3.2
- **Fix:** Resolved Windows SQLite file locking `PermissionError (WinError 32)` during database import/restore operations.
- **Refactor:** Standardized database connection lifecycle with explicit connection cleanup handlers.

### 🔹 v1.3.1
- **Refactor:** Upgraded FastAPI core event handlers from deprecated `@app.on_event` to modern Lifespan async context managers.
- **Fix:** Resolved circular import dependencies across relay modules (`relay_vless`, `relay_grpc`, `relay_socks5`, `xhttp_siz10`).

### 🔹 v1.3.0
- **Architecture:** Complete transition to a Many-to-Many subscription model (multiple nodes connected to multiple user subscriptions).
- **Database:** Migrated persistent storage engine to SQLite (`x4g_state.db`) with automated default seeding.
- **Feature:** Added automated database backup export and conflict-checking import endpoints.

### 🔹 v1.2.4
- **Feature:** Added native XHTTP (Auto / Split-HTTP) transport support for high-resilience CDN bypass.
- **Feature:** Integrated uTLS fingerprinting profiles (`chrome`, `firefox`, `safari`, `ios`, `android`, `edge`, `random`).
- **Feature:** Added custom ALPN negotiations (`h2`, `http/1.1`).

### 🔹 v1.2.0
- **Feature:** Implemented TLS ClientHello Fragment (Anti-DPI) engine with customizable packet splitting modes (`tlshello`, `1-3`, `1-5`).
- **Feature:** Added real-time IP limiter per node/subscription with automatic active connection eviction.
- **Feature:** Added bandwidth throttling (speed limit in Mbps) per user.

### 🔹 v1.0.0 (Initial Core Release)
- **Core:** Initial release featuring VLESS over WebSocket and VLESS over gRPC.
- **UI:** Responsive dark glassmorphism web management dashboard with live traffic metrics and activity logs.
- **Subscription:** Smart dual-purpose subscription endpoints supporting both web dashboards and client base64 feeds.
