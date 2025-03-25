# app.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
from app import create_app


app = create_app()

#error handling
@app.errorhandler(404)
def page_not_found(e):
    error_message = str(e)
    return render_template('404.html', error_message=error_message), 404

@app.errorhandler(500)
def page_not_found(e):
    error_message = str(e)
    return render_template('500.html', error_message=error_message), 500

if __name__ == '__main__':
    app.run(debug=True)
