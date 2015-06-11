#coding:utf-8
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django import forms
from models import User, Userinfo, Folder, File
from forms import UserForm, ModifyForm, ValidateForm, FolderForm, FileForm, UserFormlog
from django.core.mail import send_mail
import random, string
from easymethod import change_password
from django.core.servers.basehttp import FileWrapper
from django.utils import timezone
import os, datetime, sys

# Create your views here.

reload(sys)
sys.setdefaultencoding('utf8')
def regist(req):
    errors1 = []

    if req.method == 'POST':
        uf = UserForm(req.POST)
        if uf.is_valid():

            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            email = uf.cleaned_data['email']

            if User.objects.filter(username=username):
                  errors1.append('用户名已经存在，请换一个啦')
                  return render_to_response('index2.html', {'errors1': errors1}, context_instance=RequestContext(req))
            else:
                  User.objects.create(username=username, password=password)
                  f = User.objects.get(username=username)
                  create_time = timezone.now()
                  modify_time = timezone.now()
                  f.userinfo_set.create(email=email, tel='8888888', address='default')
                  f.folder_set.create(folder_name='默认文件夹', create_time=create_time, modify_time=modify_time)
                  return render_to_response('index2.html',  context_instance=RequestContext(req))
    else:
        uf = UserForm()
    return render_to_response('index2.html', {'uf': uf}, context_instance=RequestContext(req))

def login(req):
    if req.method == 'POST':
        uf = UserFormlog(req.POST)
        if uf.is_valid():
          username = uf.cleaned_data['username']
          password = uf.cleaned_data['password']
              # 获取表单数据与数据库做比较
        user = User.objects.filter(username__exact=username, password__exact=password)
        if user:
            req.session['username'] = username
            response = HttpResponseRedirect('/online/index/')
            response.set_cookie('username', username, 3600)
            return response
        else:
            message = '用户名不存在或密码错误'
            return render_to_response('index2.html', {'message': message}, context_instance=RequestContext(req))
    else:
        uf = UserFormlog()
    return render_to_response('index2.html', context_instance=RequestContext(req))

def index(req, s=''):
    username = req.COOKIES.get('username', '')
    a = User.objects.get(username=username)
    b = a.folder_set.all()
    if req.method == 'POST':
        if req.POST.has_key('s_thread'):
            filename = req.POST.get('s_thread')
#            filename = 'upload/readme.txt'
            wrapper = FileWrapper(file(filename))
            response = HttpResponse(wrapper, content_type='text/plain')
            response['Content-Length'] = os.path.getsize(filename)
            response['Content-Encoding'] = 'utf-8'
            response['Content-Disposition'] = 'attachment;filename=%s' % filename
            return response
        elif req.POST.has_key('s_delete'):
            file_loc = req.POST.get('s_delete')
            try:
                os.remove(file_loc)
            except WindowsError:
                pass
            f = Folder.objects.get(folder_name=s)
            c = f.file_set.filter(file_loc=file_loc)
            c.delete()
            return HttpResponseRedirect('/online/index/')
        return render(req, 'menu.html', locals())

    else:
        if not s.strip():
            s = b[0].folder_name
            req.session['folder_name'] = s
            folder_id = Folder.objects.get(folder_name=s)
            files_list = folder_id.file_set.all()
            return render(req, 'menu.html', {'TutorialList': b, 'username': username, 'files_list': files_list})
        else:
            req.session['folder_name'] = s
            folder_id = Folder.objects.get(folder_name=s)
            files_list = folder_id.file_set.all()

    return render(req, 'menu.html', {'TutorialList': b, 'username': username, 'files_list': files_list})

def logout(req):
    response = HttpResponseRedirect('/online/login/')
    response.delete_cookie('username')
    return response

def sendmail(req):
     if req.method == 'POST':
         mf = ModifyForm(req.POST)
         if mf.is_valid():
             username = mf.cleaned_data['username']
             if User.objects.filter(username=username):
                 a = User.objects.get(username=username)
                 b = a.userinfo_set.all()[0]
                 email = b.email
                 message = ''.join(random.sample(string.ascii_letters + string.digits, 4))
                 req.session['validate'] = message
                 req.session['username'] = username
                 title = "修改银翼网盘密码验证邮件！."
                 # message = 'Hello! This is a message!'
                 sender = '291883225@qq.com'
                 mail_list = [email, ]
                 send_mail(
                             subject=title,
                             message=message,
                             from_email=sender,
                             recipient_list=mail_list,
                             fail_silently=False,
                             connection=None
                           )
                 return HttpResponseRedirect('/online/validate/')
             else:
                 error = '该用户名不存在'
                 return render_to_response('modify_new.html', {'error': error}, context_instance=RequestContext(req))

     else:
        mf = ModifyForm()
     return render_to_response('modify_new.html', context_instance=RequestContext(req))

def validate(req):
    message = []
    message1 = req.session.get('validate')
    username = req.session.get('username')
    user_pass = "pass"
    if req.method == 'POST':
        vf = ValidateForm(req.POST)
        if vf.is_valid():
            validate2 = vf.cleaned_data['validate']
            newpasswd = vf.cleaned_data['newpasswd']
            if cmp(message1, validate2):
                message.append(u'验证码错误！')

                return render_to_response('modify_new.html', {'message': message, 'user_pass': user_pass}, context_instance=RequestContext(req))
            else:
                change_password(username, newpasswd)
                message.append(u'密码修改成功了！请返回登陆首页。')

                return render_to_response('modify_new.html', {'message': message, 'user_pass': user_pass}, context_instance=RequestContext(req))
    else:
        vf = ValidateForm()
    return render_to_response('modify_new.html', {'user_pass': user_pass}, context_instance=RequestContext(req))

def upload(req):
    up_files = 'yes'
    if req.method == "POST":
        ff = FileForm(req.POST, req.FILES)
        folder_name = req.session.get('folder_name')
        if ff.is_valid():
            #获取表单数据
            b = ' Byte'
            file_name = ff.cleaned_data['file_name']
            file_loc = ff.cleaned_data['file_loc']
            file_handel = req.FILES['file_loc']
            file_size = str(file_handel.size) + b
            file_type_split1 = str(file_handel.name)
            file_type_split2 = file_type_split1.split('.')
            file_type = file_type_split2[1]
            #写入数据库
            upload_time = timezone.now()
            f = Folder.objects.get(folder_name=folder_name)
            f.modify_time = upload_time
            f.save()
            f.file_set.create(file_name=file_name, file_loc=file_loc, file_size=file_size, file_type=file_type, upload_time=upload_time)
            return HttpResponseRedirect('/online/index/')
    else:
        ff = FileForm()

    return render(req, 'create_folder_new.html', {'ff': ff, 'up_files': up_files})

def create_fr(req):
    username = req.COOKIES.get('username', '')
    if req.method == "POST":
        ff = FolderForm(req.POST)
        if ff.is_valid():
            folder_name = ff.cleaned_data['folder_name']
            description = ff.cleaned_data['description']
            create_time = timezone.now()
            modify_time = timezone.now()
            #写入数据库
            f = User.objects.get(username=username)
            f.folder_set.create(folder_name=folder_name, create_time=create_time, modify_time=modify_time, description=description)
            return HttpResponseRedirect('/online/index/')
    else:
        ff = FolderForm()
    return render(req, 'create_folder_new.html', {'ff': ff})

def folder_info(req):
    folder_name = req.session.get('folder_name')
    username = req.COOKIES.get('username', '')
    f = Folder.objects.get(folder_name=folder_name)
    if req.method == "POST":
        if req.POST.has_key('folder_rename'):
            folder_rename = req.POST.get('folder_rename')
            f.folder_name = folder_rename
            f.save()
            print f.folder_name
        if req.POST.has_key('description'):
            description = req.POST.get('description')
            f.description = description
            f.save()
        return HttpResponseRedirect('/online/index/')
    else:
        a = User.objects.get(username=username)
        b = a.folder_set.get(folder_name=folder_name)
        return render(req, 'folder_info.html', {'fi': b})
def html_test(req):
    return render(req, 'menu.html')

def user_info(req):
    username = req.COOKIES.get('username', '')
    a = User.objects.get(username=username)
    b = a.userinfo_set.all()[0]
    if req.method == 'POST':
        if req.POST.has_key('user_tel'):
            user_tel = req.POST.get('user_tel')
            b.tel = user_tel
            b.save()
        if req.POST.has_key('user_add'):
            user_add = req.POST.get('user_add')
            b.address = user_add
            b.save()
        return HttpResponseRedirect('/online/index/')
    else:
        return render(req, 'user_info.html', {'username': username, 'b': b})











