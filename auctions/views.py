from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Max

from .forms import CreateListing, CreateComment
from .models import User, Listing, Comment, Bid, Category, Watchlist


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(closed = False)})


def listing_view(request, listing_id):

    try:
        listing = Listing.objects.get(id=listing_id)
    except Listing.DoesNotExist:
        raise Http404("Listing not found.")


    comments = listing.comments.all()
    try:
        max_bid = listing.bids.order_by('-price')[0]
        bid_price = max_bid.price
        bid_user = max_bid.user
    except IndexError:
        bid_price = 0
        bid_user=""


    if bid_price == None or listing.starting_bid > bid_price:
        bid_price = listing.starting_bid

    
    if request.user.is_authenticated:
        on_watchlist = listing.watchlist_listing.filter(user=request.user.id).exists()
    else:
        on_watchlist = False

    if request.method == "POST":
        comment_form = CreateComment(request.POST)
        if comment_form.is_valid() and request.user.is_authenticated:
            content = comment_form.cleaned_data["content"]
            user = User.objects.get(pk=request.user.id)
            comment = Comment(content = content, user = user, listing = listing)
            comment.save()
            return HttpResponseRedirect(reverse("listing_view", kwargs={'listing_id':listing.id}))
        else:
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "max_bid": bid_price,
                "bid_user": bid_user,
                "comments": comments,
                "comment_form": comment_form,
                "on_watchlist": on_watchlist
        })
    else:
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "max_bid": bid_price,
            "bid_user": bid_user,
            "comments": comments,
            "comment_form": CreateComment(),
            "on_watchlist": on_watchlist
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
def close_listing(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        listing_owner = listing.user.id

        if listing_owner == request.user.id:
            if listing.closed == False:
                listing.closed = True
                listing.save()
            else:
                listing.closed = False
                listing.save()
            return HttpResponseRedirect(reverse("listing_view", kwargs={'listing_id':listing.id}))
    
    return HttpResponse("Error 405: Not available")




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


@login_required(login_url=login_view)
def watchlist(request):
    user_id = request.user.id

    if request.method == "POST":

        add_watchlist = request.POST['add_watchlist']
        
        listing_id = request.POST['listing_id']

        user = User.objects.get(pk=user_id)
        listing = Listing.objects.get(pk=listing_id)

        if add_watchlist == "True":
            watchlist = Watchlist(user=user, listing=listing)
            watchlist.save()
        else:
            Watchlist.objects.filter(user=user, listing=listing).delete()
        
        return HttpResponseRedirect(reverse("watchlist"))

    else:
        watchlist_listing_ids = User.objects.get(pk=request.user.id).watchlist_user.values_list("listing")
        listings = Listing.objects.filter(id__in=watchlist_listing_ids, closed=False)

        return render(request, "auctions/watchlist.html", {
            "listings": listings})


def categories(request):
    
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories})


def category_listings(request, category):

    listings = Listing.objects.filter(category__category = category)
    return render(request, "auctions/index.html", {
        "listings": listings})


@login_required(login_url=login_view)
def bids(request):

    if request.method == "POST":

        new_bid = float(request.POST['price'])
        listing_id = request.POST['listing_id']
        user_id = request.user.id

        user = User.objects.get(pk=user_id)
        listing = Listing.objects.get(pk=listing_id)

        try:
            max_bid = listing.bids.order_by('-price')[0]
            bid_price = max_bid.price

        except IndexError:
            bid_price = 0


        starting_bid = listing.starting_bid

        if new_bid <= bid_price or new_bid <= starting_bid:
            return HttpResponseRedirect(reverse("listing_view", kwargs={'listing_id':listing.id}))

        bid = Bid(price = new_bid, user = user, listing = listing)
        bid.save()

    return HttpResponseRedirect(reverse("listing_view", kwargs={'listing_id':listing.id}))