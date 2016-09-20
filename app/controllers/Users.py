
from system.core.controller import *

class Users(Controller):
    def __init__(self, action):
        super(Users, self).__init__(action)
        self.load_model('User')
 
    def index(self):
        return self.load_view('index.html')

    def friends(self):
        info = {
        'user_id': session['id'] 
        }
        users = self.models['User'].show_users()
        friends = self.models['User'].show_friends(info)
        return self.load_view('friends.html', users = users, friends= friends) 

    def create_user(self):
        user_details = {
        'name': request.form['name'],
        'alias': request.form['alias'],
        'date_of_birth':request.form['dob'],
        'email': request.form['email'],
        'password':request.form['password'],
        'comfirmpw':request.form['comfirmpw']
        }
        create_status = self.models['User'].add_user(user_details)
        if create_status['status'] == True :
            session['id'] = create_status['user']['id']
            session['alias'] = create_status['user']['alias']
            return redirect('/friends')
        else:
            for message in create_status['errors']:
                flash(message,'regis_errors')
            return redirect('/')

    def login_user(self):
        user_details = {
            'email': request.form['email'],
            'password': request.form['password']
        }
        login_status = self.models['User'].login_user(user_details)
        if login_status['status'] == True:
            session['id'] = login_status['user']['id']
            session['alias'] = login_status['user']['alias']
            return redirect('/friends')
        else:
            for message in login_status['errors']:
                flash(message,'regis_errors')
                return redirect('/')
        print session['id']

    def add_friends(self):
        info = {
            'friend': request.form['user'],
            'user_id': request.form['friend']
        }
        friend = self.models['User'].add_friends(info)
        return redirect('/friends')

    def view(self, id):
        view = self.models['User'].view(id)
        return self.load_view('view.html', view = view)
            

    def logout(self):
        session.clear()
        return redirect('/')





