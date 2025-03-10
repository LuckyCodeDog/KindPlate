# app.py
from flask import Flask
from app.dashboard.dashboard import dashboard 
from flask import render_template
app = Flask(__name__)

# 注册蓝图
app.register_blueprint(dashboard, url_prefix='/dashboard')


@app.route("/")
def home():
    return render_template(f"base.html")

if __name__ == '__main__':
    app.run(debug=True)
