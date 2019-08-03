from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy
import os
from django.conf import settings

from .forms import BookForm
from .models import Book

import datetime
my_date = datetime.date.today() # if date is 01/01/2018
year, week_num, day_of_week = my_date.isocalendar()
print("Week #" + str(week_num) + " of year " + str(year))


class Home(TemplateView):
    template_name = 'home.html'


def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fname = uname + "_" + str(week_num) + "_" + str(year) + ".pdf"
        fs = FileSystemStorage()
        name = fs.save(fname, uploaded_file)
        context['url'] = fs.url(name)
    return render(request, 'upload.html', context)


def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {
        'books': books
    })


def upload_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            temp_fname = form.cleaned_data['pdf']
            uname = request.user.username
            fname = uname + "_" + str(week_num) + "_" + str(year) + ".pdf"
            report = Book(title=fname, author=uname, pdf=fname, cover="")
            handle_uploaded_file(temp_fname, fname)
            report.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'upload_book.html', {
        'form': form
    })

def handle_uploaded_file(sf, df):
    with open('media/books/pdfs/'+df, 'wb+') as destination:
         for chunk in sf.chunks():
             destination.write(chunk)

def delete_book(request, pk):
    if request.method == 'POST':
        book = Book.objects.get(pk=pk)
        book.delete()
    return redirect('book_list')


class BookListView(ListView):
    model = Book
    template_name = 'class_book_list.html'
    context_object_name = 'books'


class UploadBookView(CreateView):
    model = Book
    form_class = BookForm
    success_url = reverse_lazy('class_book_list')
    template_name = 'upload_book.html'

def GetUserName(request):
    current_user = request.user
    return current_user.id
