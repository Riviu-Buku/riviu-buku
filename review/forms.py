from django import forms
from review.models import Review

class ReviewForm(forms.ModelForm):
    # Define choices for star ratings
    STARS_CHOICES = [
        (1, "1 star ⭐"),
        (2, "2 stars ⭐⭐"),
        (3, "3 stars ⭐⭐⭐"),
        (4, "4 stars ⭐⭐⭐⭐"),
        (5, "5 stars ⭐⭐⭐⭐⭐"),
    ]

    # Create a ChoiceField for the stars with the predefined choices
    stars = forms.ChoiceField(
        choices=STARS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),  # Optional: Add a CSS class for styling
    )

    class Meta:
        model = Review
        fields = ["stars", "description"]