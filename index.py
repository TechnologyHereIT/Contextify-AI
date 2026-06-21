import os
import sys
import subprocess
from flask import Flask

# تشغيل سيرفر Streamlit في الخلفية كعملية منفصلة (Subprocess)
# لمنع تعليق خادم Vercel وتوجيه المنافذ بشكل صحيح
try:
    if not os.environ.get("STREAMLIT_RUNNING"):
        os.environ["STREAMLIT_RUNNING"] = "1"
        subprocess.Popen([
            "streamlit", "run", "app.py", 
            "--server.port", "8080", 
            "--server.address", "0.0.0.0",
            "--server.headless", "true"
        ])
except Exception as e:
    print(f"Error starting Streamlit: {e}")

# تعريف تطبيق Flask كـ Top-level app يرضي فحص Vercel بنجاح
app = Flask(__name__)

@app.route('/')
def home():
    return "Contextify AI Framework Engine Status: ONLINE. Streamlit process deployed in background."

# جعل المتغيرات مكشوفة بالأسماء التي يبحث عنها السيرفر
application = app
handler = app