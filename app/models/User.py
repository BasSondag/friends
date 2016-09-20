
from system.core.model import Model
import re 

class User(Model):
    def __init__(self):
        super(User, self).__init__()
    
    def add_user(self, user):
        EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
        errors = []
        if not user['name']:
            errors.append('Name cannot be blank')
        if not user['alias']:
            errors.append('Alias cannot be blank')
        if not user['date_of_birth']:
            errors.append('date of birth cannot be blank')
            # errors.append('day of birth must be in past')
        if not user['email']:
            errors.append('Email cannot be blank')
        elif not EMAIL_REGEX.match(user['email']):
            errors.append('Must be real email')
        if not user['password']:
            errors.append('password cannot be blank')
        if not user['comfirmpw']:
            errors.append('Name cannot be blank')
        if user['password'] != user['comfirmpw']:
            errors.append('password does not macth comfirm')
        if errors:
            return {"status": False, "errors": errors}
        else:
            password = user['password']
            hashed_pw = self.bcrypt.generate_password_hash(password)
            query = "INSERT INTO users(name, alias, date_of_birth, email, pw_hash, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, NOW(), NOW())"
            data  =[user['name'], user['alias'],user['date_of_birth'], user['email'], hashed_pw]
            user = self.db.query_db(query, data)
            get_user_query = "SELECT * FROM users ORDER BY id DESC LIMIT 1" 
            get_user = self.db.query_db(get_user_query)
            return {"status": True, "user": get_user[0]}

    def login_user(self, user):
        errors = []
        if not user['email']:
            errors.append('Email cannot be blank')
            return {"status": False, "errors": errors}
        else:
            password = user['password']
            query = "SELECT * FROM users WHERE email = %s LIMIT 1"
            data = [user['email']]
            users = self.db.query_db(query, data)
            if users:
                if self.bcrypt.check_password_hash(users[0]['pw_hash'], password):
                    return {"status": True, "user": users[0]}
            else: 
                errors.append('Password and email do not match')
                return {"status": False, "errors": errors}

    def show_friends(self,info):
        query = "SELECT users.id, users.name, users.alias, users.email, userfriends.friend, userfriends.user_id FROM users JOIN userfriends ON users.id = userfriends.user_id where userfriends.friend = %s"
        data =  [info['user_id']]
        friends = self.db.query_db(query, data)
        return friends

    def show_users(self):   
        query = "SELECT * FROM users "
        users = self.db.query_db(query)
        return users  

    def add_friends(self, info):
        query = "INSERT INTO userfriends(friend, user_id) VALUES ( %s, %s)"
        data = [info['friend'], info['user_id']]
        friend = self.db.query_db(query, data)
        return friend

    def view(self, id):
        query = "SELECT * from users where users.id = %s"
        data =[id]
        view = self.db.query_db(query, data)
        return view



