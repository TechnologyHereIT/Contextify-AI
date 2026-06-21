import os
import sys
from flask import Flask, send_from_directory

app = Flask(__name__)

# مسار أساسي لتشغيل الخدمة دون انهيار الفحص
@app.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <meta http-equiv="X-UA-Compatible" content="IE=edge">
      <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
      <title>Contextify AI</title>
      <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@stlite/mountable@0.39.0/build/stlite.css">
    </head>
    <body>
      <div id="root"></div>
      <script src="https://cdn.jsdelivr.net/npm/@stlite/mountable@0.39.0/build/stlite.js"></script>
      <script>
        stlite.mount({
          requirements: ["requests", "pypdf"],
          entrypoint: "app.py",
          files: {
            "app.py": `""" + open("app.py", "r", encoding="utf-8").read().replace("`", "\\`").replace("$", "\\$") + """`
          }
        }, document.getElementById("root"));
      </script>
    </body>
    </html>
    """

# إتاحة المتغيرات التي يبحث عنها فحص Vercel
application = app
handler = app