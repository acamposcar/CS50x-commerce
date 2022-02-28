from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.contrib import messages
from .forms import CreateListing, CreateComment
from .models import User, Listing, Comment, Bid, Category, Watchlist


def index(request):
    '''
    Shows all open listings.
    '''
    
    return render(request,"auctions/index.html",{
            "listings": Listing.objects.filter(closed=False).order_by("-date"),
            "active":'home'
            })


def listing_view(request, listing_id):
    '''
    Shows detailed information for single listing.
    POST method allowed to add new comments.
    '''

    try:
        listing = Listing.objects.get(id=listing_id)
    except Listing.DoesNotExist:
        raise Http404("Listing not found.")

    comments = listing.comments.all()

    if request.user.is_authenticated:
        on_watchlist = listing.watchlist_listing.filter(user=request.user.id).exists()
    else:
        on_watchlist = False

    if request.method == "POST":

        comment_form = CreateComment(request.POST)
        if comment_form.is_valid() and request.user.is_authenticated:
            content = comment_form.cleaned_data["content"]
            user = User.objects.get(pk=request.user.id)
            comment = Comment(content=content, user=user, listing=listing)
            comment.save()
            return HttpResponseRedirect(
                reverse("listing_view", kwargs={"listing_id": listing.id})
            )
        else:
            return render(
                request,
                "auctions/listing.html",
                {
                    "listing": listing,
                    "comments": comments,
                    "comment_form": comment_form,
                    "on_watchlist": on_watchlist,
                    "active":'listing'
                },
            )
    else:
        return render(
            request,
            "auctions/listing.html",
            {
                "listing": listing,
                "comments": comments,
                "comment_form": CreateComment(),
                "on_watchlist": on_watchlist,
                "active":'listing'
            },
        )


def login_view(request):
    '''
    Login page
    POST method allowed to login user
    '''

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
            return render(request,"auctions/login.html",{
                    "message": "Invalid username and/or password.",
                    "active":'login'
                })
    else:
        return render(request, "auctions/login.html", {"active": 'login'})


def logout_view(request):
    '''
    Logout
    '''

    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    '''
    Register page
    POST method allowed to create new user
    '''

    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "auctions/register.html", {"message": "Passwords must match.", "active":'register'}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken.", 
                "active":'register'})

        login(request, user)

        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "auctions/register.html", {"active":'register'})


@login_required(login_url=login_view)
def close_listing(request, listing_id):
    '''
    POST method allowed to open/close listings
    '''

    if request.method == "POST":

        try:
            listing = Listing.objects.get(pk=listing_id)
        except Listing.DoesNotExist:
            raise Http404("Listing not found.")

        listing_owner = listing.user.id

        if listing_owner == request.user.id:
            if listing.closed == False:
                listing.closed = True
                listing.save()
            else:
                listing.closed = False
                listing.save()
            return HttpResponseRedirect(
                reverse("listing_view", kwargs={"listing_id": listing.id}))

    return HttpResponse("Error 405: Not available")


@login_required(login_url=login_view)
def new(request):
    '''
    New listing page.
    POST method allowed to create new listing.
    '''

    if request.method == "POST":
        form = CreateListing(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            starting_price = form.cleaned_data["starting_price"]
            user = User.objects.get(pk=request.user.id)
            image_url = form.cleaned_data["image"]
            category = Category.objects.get(category=form.cleaned_data["category"])

            listing = Listing(
                title=title,
                description=description,
                starting_price=starting_price,
                image_url=image_url,
                category=category,
                user=user,
            )

            listing.save()
            return HttpResponseRedirect(
                reverse("listing_view", kwargs={"listing_id": listing.id})
            )
        else:
            return render(request, "auctions/new.html", {"form": form, "active":'new'})

    else:
        return render(
            request,
            "auctions/new.html",
            {
                "form": CreateListing(),
                "active":'new'
            }
        )


@login_required(login_url=login_view)
def watchlist(request):
    '''
    Watchlist page
    POST method allowed to add/delete listing to watchlist
    '''
    user_id = request.user.id

    if request.method == "POST":

        add_watchlist = request.POST["add_watchlist"]

        listing_id = request.POST["listing_id"]

        user = User.objects.get(pk=user_id)
        listing = Listing.objects.get(pk=listing_id)

        if add_watchlist == "True":
            watchlist = Watchlist(user=user, listing=listing)
            watchlist.save()
            # return HttpResponseRedirect(reverse("watchlist"))
            return HttpResponseRedirect(
                reverse("listing_view", kwargs={"listing_id": listing.id})
            )
        else:
            Watchlist.objects.filter(user=user, listing=listing).delete()

            return HttpResponseRedirect(
                reverse("listing_view", kwargs={"listing_id": listing.id})
            )

    else:
        watchlist_listing_ids = User.objects.get(
            pk=request.user.id
        ).watchlist_user.values_list("listing")
        listings = Listing.objects.filter(id__in=watchlist_listing_ids, closed=False)

        return render(
            request, "auctions/watchlist.html", {"listings": listings.order_by("-date"), "active":'watchlist'}
        )


@login_required(login_url=login_view)
def user_page(request):
    '''
    User page. It shows listings in which the user has participated.
    - Selling
    - Closed
    - Active Bids
    - Won (closed bids)
    '''
    user_id = request.user.id
    user_bids_id = User.objects.get(pk=request.user.id).bid_user.values_list("listing")

    selling = Listing.objects.filter(user=user_id, closed=False)
    closed = Listing.objects.filter(user=user_id, closed=True)
    open_bids = Listing.objects.filter(id__in=user_bids_id, closed=False)
    closed_bids = Listing.objects.filter(id__in=user_bids_id, closed=True)

    won_bids = list()

    for listing in closed_bids:
        max_bid = listing.bids.order_by("-price").first()

        if max_bid.user.id == user_id:
            won_bids.append(listing)

    return render(
        request,
        "auctions/user.html",
        {"selling": selling, "closed": closed, "won": won_bids, "bid": open_bids, "active":'user'},
    )


def categories(request):
    '''
    Category page. Allows to select category
    '''
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {"categories": categories, "active":'categories'})


def category_listings(request, category):
    '''
    Category page. Shows articles grouped according to their category.
    '''
    categories = Category.objects.all()
    listings = Listing.objects.filter(closed=False, category__category=category).order_by("-date")

    return render(
        request, "auctions/categories.html", {
            "listings": listings, 
            "categories": categories,
            "current_category": category,
            "active":'categories'}
    )


@login_required(login_url=login_view)
def bids(request):
    '''
    Handles logic to make bids
    POST method allowed to create a new bid if it is bigger than existing bids
    '''

    if request.method == "POST":

        new_bid = float(request.POST["price"])
        listing_id = request.POST["listing_id"]
        user_id = request.user.id

        user = User.objects.get(pk=user_id)
        listing = Listing.objects.get(pk=listing_id)

        if new_bid > listing.current_bid and new_bid >= listing.starting_price and new_bid > 0:

            bid = Bid(price=new_bid, user=user, listing=listing)
            bid.save()

            listing.current_bid_winner = user
            listing.current_bid = new_bid
            listing.save()
            return HttpResponseRedirect(
                reverse("listing_view", kwargs={"listing_id": listing.id})
                )
        else:
            messages.error(request, 'The bid must be greater than the current price')
            return HttpResponseRedirect(reverse("listing_view", kwargs={"listing_id": listing.id}) )

                
    else:
        return HttpResponse("Error 405: Not available")