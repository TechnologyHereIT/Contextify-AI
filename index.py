import os
import sys
import base64
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    try:
        # تحديد المسار الحالي لضمان قراءة ملف app.py الأصلي المرفوع
        current_dir = os.path.dirname(os.path.abspath(__file__))
        app_py_path = os.path.join(current_dir, "app.py")
        
        # قراءة كود الـ Streamlit الأصلي بالكامل
        with open(app_py_path, "r", encoding="utf-8") as f:
            python_code = f.read()
            
        # تشفيره لـ base64 لتمريره بأمان تام للمتصفح دون تدمير الـ Syntax
        encoded_code = base64.b64encode(python_code.encode("utf-8")).decode("utf-8")
        
    except Exception as e:
        return f"Error loading app.py: {str(e)}", 500

    # إرجاع واجهة العرض التي تشغل stlite بأمان
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <meta http-equiv="X-UA-Compatible" content="IE=edge">
      <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
      <title>Contextify AI - Workspace</title>
      <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@stlite/mountable@0.54.0/build/stlite.css">
    </head>
    <body>
      <div id="root"></div>
      <script src="https://cdn.jsdelivr.net/npm/@stlite/mountable@0.54.0/build/stlite.js"></script>
      <script>
        // فك التشفير النقي داخل المتصفح مباشرة متوافق مع كافة النصوص والرموز
        const base64Code = "{encoded_code}";
        const decodedCode = decodeURIComponent(atob(base64Code).split('').map(function(c) {{
            return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
        }}).join(''));

        stlite.mount({{
          requirements: ["requests", "pypdf"],
          entrypoint: "app.py",
          files: {{
            "app.py": decodedCode
          }},
          streamlitConfig: {{
            "server.headless": true,
            "theme.primaryColor": "#0f172a"
          }}
        }}, document.getElementById("root"));
      </script>
    </body>
    </html>
    """

# المتغيرات المطلوبة للتعرف على الـ Serverless Function بنجاح
application = app
handler = app
