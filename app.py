# app.py
from MySQLdb import OperationalError
from flask import Flask
from app.dashboard.dashboard import dashboard 
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
from config import Config

app = Flask(__name__)

# 注册蓝图
app.register_blueprint(dashboard, url_prefix='/dashboard')
app.config.from_object(Config)
db = SQLAlchemy(app)
from dal.models import *

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/")
def home():
    try:
        # 尝试连接并执行查询
        with app.app_context():
            db.engine.connect()
        return "数据库连接成功!"
    except OperationalError as e:
        return f"数据库连接失败: {e}"

@app.route("/docs")
def docs():
    return render_template(f"docs.html")


if __name__ == '__main__':
    app.run(debug=True)
