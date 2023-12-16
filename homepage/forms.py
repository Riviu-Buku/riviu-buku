from django.forms import ModelForm
from homepage.models import FavoriteBook

class BookForm(ModelForm):
    class Meta:
        model = FavoriteBook
        fields = [
            "title",
            "author",
            ]