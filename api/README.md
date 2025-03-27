# 🚀 API Service

## 📌 Overview
This is a Python-based API that collects **Particulate Matter (PM2.5)** data added on a specified period. 
<br>

## ✅ Prerequisites
- **Python**
- **Git**
- **PostgreSQL**
- **SSH Key**
<br>

## 📦 Installation
To install and run the API, follow these steps:

1. **Clone the repository:**
   ```sh
   git clone git@github.com:Byte-Zone/Services.git
   cd Services/api
   ```
2. **Create a virtual environment and activate it:**
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
<br>

## 🚀 Usage
To start the API, run:
```sh
cd source
gunicorn -w 4 -b 0.0.0.0:{port} app:app
```
<br> 

### 🌍 API Endpoints
| ⚡ Method | 📌 Endpoint | 📝 Description |
|----------|-----------|---------------|
| **GET**  | `/data/initialdate/<initial_date>/finaldate/<final_date>` | Collects Particulate Matter (PM2.5) data added on a specified period.  |
