####### LINCOLN FITNESS #######
### GROUP 21                ###
###############################


from flask import session


class User():
    def __init__(self, name, role, id="", email="", role_id=""):
        self.name = name
        self.role = role
        self.id = id
        self.role_id = role_id
        self.email = email

        if session.get("name") != name or session.get("role") != role or session.get("id") != id or session.get("email") != email or session.get("role_id") != role_id:
            session["name"] = name
            session["role"] = role
            session["id"] = id
            session["role_id"] = role_id
            session["email"] = email
            session["is_authenticated"] = True

    def __str__(self):
        return f"🟢 <User(id = {self.id},  name = {self.name}, role = {self.role}, role_id = {self.role_id}, email = {self.email})>"


def current_user():
    name = session.get("name")
    role = session.get("role")
    id = session.get("id")
    email = session.get("email")
    role_id = session.get("role_id")

    if name == None or role == None or id == None or email == None or role_id == None:
        return None

    return User(name=name, role=role, id=id, email=email, role_id=role_id)


def clear_session():
    session.clear()
