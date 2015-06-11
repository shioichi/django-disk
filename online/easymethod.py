from models import User
def change_password(username, newpass):
    p = User.objects.get(username=username)
    p.password = newpass
    p.save()