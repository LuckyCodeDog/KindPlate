from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user



def roles_required(*required_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash("Please log in to access first.")
                return redirect(url_for('home.account')) 

            if current_user.role.value not in required_roles:
                flash("You do not have permission to access this page.")
                return redirect(url_for('home.index')) 

            return f(*args, **kwargs)
        return decorated_function
    return decorator


def dashboard_roles_required(*required_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash("Please log in to access first.")
                return redirect(url_for('dashboard.login')) 

            if current_user.role.value not in required_roles:
                flash("You do not have permission to access this page.")
                return redirect(url_for('dashboard.login')) 
            return f(*args, **kwargs)
        return decorated_function
    return decorator