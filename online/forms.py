#coding:utf-8
from django import forms



class UserForm(forms.Form):
    username = forms.CharField(label='用户名:', max_length=100)
    password = forms.CharField(label='密码:', widget=forms.PasswordInput())
    email = forms.EmailField()

class UserFormlog(forms.Form):
    username = forms.CharField(label='用户名:', max_length=100)
    password = forms.CharField(label='密码:', widget=forms.PasswordInput())

class ModifyForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=100)

class ValidateForm(forms.Form):
    validate = forms.CharField(label='验证码',)
    newpasswd = forms.CharField(label=u'新密码')

class FolderForm(forms.Form):
    folder_name = forms.CharField(label='文件夹名称', max_length=50)
    # create_time = forms.DateTimeField(label='创建时间')
    # modify_time = forms.DateTimeField(label='修改时间')
    description = forms.CharField(label='描述', max_length=50)

class FileForm(forms.Form):
    file_name = forms.CharField(label='文件名', max_length=50)
    file_loc = forms.FileField(label='选择文件')
#    file_size = forms.CharField(label='文件大小', max_length=50)
#    file_type = forms.CharField(label='文件类型', max_length=50)

