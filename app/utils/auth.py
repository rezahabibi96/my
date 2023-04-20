from models import users as users_md


data = [
    {
        'id': '',
        'fullname': '',
        'username': '',
        'email': '',
        'password': ''
    }
]

for user in data:
    password = users_md.bc.generate_password_hash(user['password'])
    user = users_md.Users(user['id'], user['fullname'], user['username'], user['email'], password)
    user.save()