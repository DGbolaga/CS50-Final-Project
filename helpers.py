from flask_login import login_user, LoginManager, logout_user, login_required, UserMixin

class User(UserMixin):
    def __init__(self, id, name, email, password):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        
    
    