from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from django.http import Http404
from django.contrib.auth.models import User
from django.db.models import Count
from django.views.generic import UpdateView,ListView
from django.utils import timezone
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.urls import reverse_lazy
from django.contrib import messages
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from .models import Document
from .forms import DocumentForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.
"""
def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name,myfile)
        uploaded_file_url = fs.url(filename)
        return render(request,'simple_upload.html',{'uploaded_file_url':uploaded_file_url})
    return render(request,'simple_upload.html')
"""
def model_form_upload(request):
    my_doc = Document.objects.all()
    if request.method =='POST':
        form = DocumentForm(request.POST,request.FILES)
        if form.is_valid():
            dc = form.save()
            return render(request,'simple_upload.html',{'dc':dc,'documents':my_doc})
    else:
        form = DocumentForm()
    return render(request,'simple_upload.html',{'form':form,'documents':my_doc})