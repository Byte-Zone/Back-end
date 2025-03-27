# 🚀 Interface Service

## 📌 Overview
This is a web-based interface built using **HTML, CSS, JavaScript, and Python**. It provides an interactive platform to visualize and interact with **Particulate Matter (PM2.5)** data collected over a specified period.
<br>

## ✅ Prerequisites
- **Python**
- **Git**
- **Run the API service**
- **SSH Key**
- **Web Browser**
<br>

## 📦 Installation
To install, follow these steps:

1. **Clone the repository:**
   ```sh
   git clone git@github.com:Byte-Zone/Services.git
   cd Services/interface
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
To start the interface, run:
```sh
cd source
gunicorn -w 4 -b 0.0.0.0:{port} app:app
```
<br> 

Once the interface is running, users can:
- Select a date range to fetch PM2.5 data inserted in that period.
<br>

## 🎨 Technologies Used
- **HTML** - Structure of the interface
- **CSS** - Styling and layout
- **JavaScript** - API calls and dynamic content rendering
- **Python** - Backend API
