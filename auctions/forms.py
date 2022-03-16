from django import forms
from django.db.models.fields import BLANK_CHOICE_DASH
from .models import Category

"""
Create Listing: Users should be able to visit a page to create a new listing. They should be able to specify a title for the listing, a text-based description, and what the starting bid should be. Users should also optionally be able to provide a URL for an image for the listing and/or a category (e.g. Fashion, Toys, Electronics, Home, etc.).
"""

class CreateListing(forms.Form):
    title = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "Title", "class":"form-control"}),  required=True)
    description = forms.CharField(widget=forms.Textarea(
        attrs={"placeholder": "Description", "rows":10, "class":"form-control"}), required=True)
    starting_price=forms.IntegerField(widget=forms.NumberInput(
        attrs={"placeholder": "Starting Price", "class":"form-control"}),  required=True)
    image=forms.URLField(widget=forms.URLInput(
        attrs={"placeholder": "Image URL", "class":"form-control"}),  required=False)    
    category=forms.ModelChoiceField(widget=forms.Select(
        attrs={"class":"custom-select"}), queryset=Category.objects.all(), required=False)


class CreateComment(forms.Form):
    content = forms.CharField(widget=forms.Textarea(
        attrs={"rows":5, "class":"form-control", "placeholder": "New comment"}), required=True, label=False)