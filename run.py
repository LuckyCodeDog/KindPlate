# app.py
from MySQLdb import OperationalError
from flask import Flask
from app.dashboard.dashboard import dashboard 
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
from app import create_app


app = create_app()

#error handling
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
