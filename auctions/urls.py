from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new", views.new, name="new"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category>", views.category_listings, name="category_listings"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("bids", views.bids, name="bids"),
    path("user", views.user_page, name="user_page"),
    path("close/<str:listing_id>", views.close_listing, name="close_listing"),
    path("<int:listing_id>", views.listing_view, name="listing_view")
]
