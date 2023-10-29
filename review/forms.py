from django.forms import ModelForm
from review.models import Review

class ProductForm(ModelForm):
    class Meta:
        model = Review
        fields = ["name", "price", "description"]