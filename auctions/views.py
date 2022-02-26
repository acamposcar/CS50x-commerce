from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .forms import CreateListing, CreateComment
from .models import User, Listing, Comment, Bid, Category


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()})


def listing_view(request, listing_id):
    if request.method == "POST":
        form = CreateComment(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            content = form.cleaned_data["content"]
            user = User.objects.get(pk=request.user.id)
            listing = Listing.objects.get(pk=listing_id)
            comment = Comment(content = content, user = user, listing = listing)
            comment.save()
            return HttpResponseRedirect(reverse("listing_view", kwargs={'listing_id':listing.id}))
        else:
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "comments": listing.comments.all(),
                "comment_form": form
        })
    else:
        try:
            listing = Listing.objects.get(id=listing_id)
        except Listing.DoesNotExist:
            raise Http404("Listing not found.")
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "comments": listing.comments.all(),
            "comment_form": CreateComment()
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required(login_url=login_view)
def new(request):
    if request.method == "POST":
        form = CreateListing(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            starting_bid = form.cleaned_data["starting_bid"]
            user = User.objects.get(pk=request.user.id)
            image_url = form.cleaned_data["image"]
            category = Category.objects.get(category=form.cleaned_data["category"])

            listing = Listing(title = title, description = description,
            starting_bid = starting_bid,image_url = image_url, 
            category = category, user = user)

            listing.save()
            return HttpResponseRedirect(reverse("listing_view", kwargs={'listing_id':listing.id}))
        else:
            return render(request, "auctions/new.html", {
                "form": form
            })

        
    else:
        return render(request, "auctions/new.html", {
                "form": CreateListing(),
            })


def categories(request):
    pass


def watchlist(request):
    pass


