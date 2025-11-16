# 📦 **pg-manager v1.0**

**pg-manager** is a lightweight automation tool designed for **PasarGuard panel management**, providing:

* Automated client creation
* Volume & validity management
* A clean **FastAPI REST backend**
* A simple **Telegram Bot** using Telebot
* Easy `.env` configuration
* Minimal dependencies — simple to deploy & modify

This project is intentionally kept **simple, clean, and easy to customize**.

---

## 🚀 **Features**

* 👥 Bulk client creation
* 📡 REST API (FastAPI)
* 🤖 Telegram Bot (Telebot)
* 🔑 `.env` configuration support
* ⚡ Easy installation & deployment
* 🧩 Clear project structure

---

## 🏗️ **Project Structure**

```
pg-manager/
│
├── main.py              # Main FastAPI application (bot + API)
├── api.py               # Login + user creation endpoints
├── bot.py               # Telegram bot using Telebot
│
├── panel_client.py      # PasarGuard panel HTTP client (requests)
├── .env                 # Environment configuration
│
├── requirements.txt
└── README.md
```

---

# ⚙️ **Installation**

You can install pg-manager automatically using this command:

### **📌 One-Line Install (recommended)**

```bash
bash <(curl -Ls https://raw.githubusercontent.com/iliya-Developer/pg-manager/master/install.sh)
```

This installer will:

✔ Download the project
✔ Ask for your **Bot Token** and **Admin ID**
✔ Create a virtual environment
✔ Install all dependencies
✔ Create/update `.env`
✔ Install a systemd service
✔ Start the pg-manager service

Everything is automated.

---

## 📡 **REST API Endpoints**

Run FastAPI server manually (if not using systemd):

```bash
uvicorn main:app --host 0.0.0.0 --port 9000 --reload
```

Base URL:

```
http://127.0.0.1:9000
```

---

### 👤 **POST /create-users**

Create one or multiple new PasarGuard clients.

#### Example Request

```json
{
    "address": "https://your-panel.com:8000/dashboard",
    "panel_username": "",
    "panel_password": "",
    "username": "",
    "status": "",
    "expire": 0,
    "data_limit": 0,
    "group_ids": [1, 2],
    "on_hold_timeout": 1,
    "on_hold_expire_duration": 1
}
```

---

# 🤖 **Telegram Bot Commands**

The Telegram bot communicates directly with your FastAPI backend.

| Command   | Description        |
| --------- | ------------------ |
| `/start`  | Welcome message    |
| `/create` | Create new clients |

---

# 🔧 **Environment Configuration (`.env`)**

Ensure you have a `.env` file with:

```
BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
ADMIN_ID=YOUR_ADMIN_TELEGRAM_ID
API_URL=http://127.0.0.1:9000/create-users
```

---

# 🤝 **Contributing**

Contributions, issues, and feature requests are welcome.
Open an **Issue** or make a **Pull Request** anytime.

---

# 📄 **License**

This project is licensed under the **MIT License**.

---

# 💰 **Support the Project**

If pg-manager helps you and you'd like to support development:

* **TRX (Tron):** `TJFzpTArQvGRo5QJ8vz8YX2F4bVeuKXv8k`
* **USDT (BEP20):** `0x47e832e2F8D1c3F593Ec94d1Ddb497F81847AAF7`

---

# ⭐️ **Star the Project**

If this project helped you, consider giving it a ⭐️ on GitHub to support future improvements.

---

# 📬 **Contact**

For questions, suggestions, or bug reports:
➡️ Open an **Issue** on this repository.

---