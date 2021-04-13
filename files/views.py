from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from .models import UserFile
from .forms import FileForm, FileShareForm, FileRenameForm
# from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect, FileResponse
from django.urls import reverse
from django.contrib.auth.models import User
import os
from django.conf import settings
from . import functions

# Create your views here.
def index(request):
    return render(request, 'files/index.html')

@login_required
def myfiles(request):
    # files = request.user.files.all()
    # files = UserFile.objects.all().filter(uploader = request.user)
    return render(request, 'files/myfiles.html',{
        'files':request.user.files.filter(in_trash=0),
        'form':FileForm(),
        'shareform' : FileShareForm(),
        'renameform' : FileRenameForm()
    })

@login_required
def save_file(request):
    # files = UserFile.objects.all().filter(uploader = request.user)
    # files = request.user.files.all()
    form = FileForm()
    if request.method == 'POST' and request.FILES['file']:
        userform = FileForm(request.POST ,request.FILES)
        myfile = request.FILES['file']
        filename = myfile.name
        size = functions.convert_bytes(myfile.size)
        print(size)
        # fs = FileSystemStorage()
        # filename = fs.save(myfile.name, myfile)
        if userform.is_valid():
            file = userform.save(commit = False)
            file.file_name = filename
            file.uploader = request.user
            file.size = size
            file.save()
            return HttpResponseRedirect(reverse('myfiles'))
        else:
            return render(request, 'files/myfiles.html', {
                'files': request.user.files.filter(in_trash=0),
                'form': userform,
                'shareform' : FileShareForm(),
                'renameform' : FileRenameForm(),
                'error': True
            })
    else:
        return render(request, 'files/myfiles.html',{
            'files':request.user.files.filter(in_trash=0),
            'form':FileForm(),
            'shareform' : FileShareForm(),
            'renameform' : FileRenameForm()
        })

@login_required
def share_file(request, file_id):
    shareform = FileShareForm()
    if request.method == 'POST':
        # files=UserFile.objects.all().filter(uploader = request.user)
        file = UserFile.objects.get(pk = file_id, uploader=request.user)
        shareform = FileShareForm(request.POST)
        if shareform.is_valid():
            user=User.objects.get(email=request.POST['email'])
            file.shared_with.add(user)
            file.save()
            return HttpResponseRedirect(reverse('myfiles'))
        else:
            return render(request, 'files/myfiles.html', {
                'files': request.user.files.filter(in_trash=0),
                'shareform': shareform,
                'form':FileForm(),
                'share_error': True,
                'renameform' : FileRenameForm()
            })
    else:
        return render(request, 'files/myfiles.html',{
            'files':request.user.files.filter(in_trash=0),
            'form':FileForm(),
            'shareform' : FileShareForm(),
            'renameform' : FileRenameForm()
        })

@login_required
def rename_file(request, file_id):
    if request.method == 'POST':
        file = UserFile.objects.get(pk = file_id, uploader=request.user)
        initial_path = file.file.path
        filename, file_extension = os.path.splitext(initial_path)
        file.file.name = "user_"+str(request.user.id)+"/"+request.POST['new_name']+file_extension
        new_path = settings.MEDIA_ROOT + file.file.name
        file.file_name = request.POST['new_name']+file_extension
        os.rename(initial_path, new_path)
        file.save()
        return HttpResponseRedirect(reverse('myfiles'))
    else:
        return render(request, 'files/myfiles.html', {
            'files':request.user.files.filter(in_trash=0),
            'form':FileForm(),
            'shareform' : FileShareForm(),
            'renameform' : FileRenameForm()
        })

@login_required
def move_to_trash(request, file_id):
    file = UserFile.objects.get(pk = file_id, uploader=request.user)
    file.in_trash = 1
    file.save()
    return HttpResponseRedirect(reverse('myfiles'))

@login_required
def shared_with_me(request):
    return render(request, 'files/shared_files.html',{
        'files':request.user.shared_with.filter(in_trash=0),
        'form':FileForm(),
    })

@login_required
def mytrash(request):
    return render(request, 'files/mytrash.html',{
        'files':request.user.files.filter(in_trash=1),
        'form':FileForm(),
    })

@login_required
def restore(request, file_id):
    file = UserFile.objects.get(pk = file_id, uploader=request.user)
    file.in_trash = 0
    file.save()
    return HttpResponseRedirect(reverse('mytrash'))

@login_required
def permanent_delete(request, file_id):
    file = UserFile.objects.get(pk = file_id, uploader=request.user)
    initial_path = file.file.path
    file.delete()
    os.remove(initial_path)
    return HttpResponseRedirect(reverse('mytrash'))

@login_required
def serverFile(request, user_id, file):
    file_owner = User.objects.get(pk = user_id)
    if file_owner == request.user:
        doc = get_object_or_404(UserFile, file="user_"+str(request.user.id)+"/"+file, uploader = request.user)
        # path, filename = os.path.split(file)
        # response = FileResponse(doc.file)
        return FileResponse(doc.file)
    else:
        doc = UserFile.objects.filter(file="user_"+str(user_id)+"/"+file, shared_with = request.user).first()
        print(doc)
        if doc:
            return FileResponse(doc.file)
        else:
            return render(request, 'files/not_found.html', {
                'message': "You are not authorized to access the file."
            })