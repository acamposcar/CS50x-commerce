from django import forms
from django.db.models.fields import BLANK_CHOICE_DASH
from .models import Category

"""
Create Listing: Users should be able to visit a page to create a new listing. They should be able to specify a title for the listing, a text-based description, and what the starting bid should be. Users should also optionally be able to provide a URL for an image for the listing and/or a category (e.g. Fashion, Toys, Electronics, Home, etc.).
"""

# TODO: Form select not updating when adding new item from Django Admin. 
# TODO: ----- must be first option

choices = list()
categories = Category.objects.all()
print(categories)
for category in categories:
    choices.append((category.category, category.category.capitalize()))


class CreateListing(forms.Form):
    title = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "Title", "class":"form-control"}),  required=True)
    description = forms.CharField(widget=forms.Textarea(
        attrs={"placeholder": "Description", "rows":10, "class":"form-control"}), required=True)
    starting_bid=forms.IntegerField(widget=forms.NumberInput(
        attrs={"placeholder": "Starting Price", "class":"form-control"}),  required=True)
    image=forms.URLField(widget=forms.URLInput(
        attrs={"placeholder": "Image URL", "class":"form-control"}),  required=False)    
    category=forms.ChoiceField(widget=forms.Select(
        attrs={"class":"custom-select"}), choices=choices)

# TODO
class EditEntry(forms.Form):
    content = forms.CharField(widget=forms.Textarea(
        attrs={"rows":15, "class":"form-control"}), required=True)


class CreateComment(forms.Form):
    content = forms.CharField(widget=forms.Textarea(
        attrs={"rows":5, "class":"form-control", "placeholder": "New comment"}), required=True, label=False)