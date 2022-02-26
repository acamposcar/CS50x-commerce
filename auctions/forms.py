from django import forms
from django.db.models.fields import BLANK_CHOICE_DASH

"""
Create Listing: Users should be able to visit a page to create a new listing. They should be able to specify a title for the listing, a text-based description, and what the starting bid should be. Users should also optionally be able to provide a URL for an image for the listing and/or a category (e.g. Fashion, Toys, Electronics, Home, etc.).
"""
class createListing(forms.Form):
    CHOICES = (('fashion', 'Fashion'),('toys', 'Toys'),('electronics','Electronics'),('home','Home'))

    title = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "Title", "class":"form-control"}),  required=True)
    description = forms.CharField(widget=forms.Textarea(
        attrs={"placeholder": "Description", "rows":15, "class":"form-control"}), required=True)
    starting_bid=forms.IntegerField(widget=forms.NumberInput(
        attrs={"placeholder": "Starting Price", "class":"form-control"}),  required=True)
    image=forms.URLField(widget=forms.URLInput(
        attrs={"placeholder": "Image URL", "class":"form-control"}),  required=False)    
    category=forms.ChoiceField(widget=forms.Select(
        attrs={"class":"custom-select"}), choices=BLANK_CHOICE_DASH + list(CHOICES),  required=False)



class editEntry(forms.Form):
    content = forms.CharField(widget=forms.Textarea(
        attrs={"rows":15, "class":"form-control"}), required=True)