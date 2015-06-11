from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)

    def __unicode__(self):
        return self.username

class Userinfo(models.Model):
    email = models.EmailField()
    tel = models.CharField(max_length=11)
    address = models.CharField(max_length=50)
    User = models.ForeignKey(User)

class Folder(models.Model):
    folder_name = models.CharField(max_length=50)
    create_time = models.DateTimeField()
    modify_time = models.DateTimeField()
    description = models.CharField(max_length=50)
    User = models.ForeignKey(User)

    def __unicode__(self):
        return self.folder_name

class File(models.Model):
    file_name = models.CharField(max_length=50)
    file_loc = models.FileField(upload_to='./upload/')
    file_size = models.CharField(max_length=50)
    file_type = models.CharField(max_length=50)
    upload_time = models.DateTimeField()
    Folder = models.ForeignKey(Folder)

    def __unicode__(self):
        return self.file_name



