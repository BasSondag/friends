
from system.core.router import routes

#users login
routes['default_controller'] = 'Users'
routes['POST']['/create'] = 'Users#create_user'
routes['POST']['/login'] = 'Users#login_user'
routes['/logout'] = 'Users#logout'


#friends dasbord
routes['/friends'] = 'Users#friends'
routes['POST']['/addfriends']= 'Users#add_friends'
routes['POST']['/removefriend'] = 'Users#removefriend'

#view friends
routes['/view/<id>'] = 'Users#view'