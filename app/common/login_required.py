from functools import wraps
from flask import redirect, url_for
from flask_login import current_user



def roles_required(*required_roles):

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('home.login')) 

            if current_user.role.value not in required_roles:
                return redirect(url_for('home.index')) 

            return f(*args, **kwargs)
        return decorated_function
    return decorator
