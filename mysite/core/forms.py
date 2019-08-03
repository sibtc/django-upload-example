from django import forms

from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('pdf',)
        #fields = ('title', 'author', 'pdf', 'cover')
