from homepage.models import Book
from django.forms import ModelForm

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "publisher", "price", "language", "pages", "genres", "description", "coverImg"]