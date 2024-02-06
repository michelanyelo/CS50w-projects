from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # individual listing
    path("listing/<str:listing_id>", views.listing_by_id, name="listing"),
    path("category/<str:slug>", views.category_listings, name="category_listings"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path("remove_watchlist/<int:listing_id>", views.remove_watchlist, name="remove_watchlist"),
    path("add_watchlist/<int:listing_id>", views.add_watchlist, name="add_watchlist"),
    path("watchlist", views.personal_watchlist, name="watchlist"),
    path("add_comment/<int:listing_id>", views.add_comment, name="add_comment"),
    path("add_bid/<int:listing_id>", views.add_bid, name="add_bid"),
    path("close_auction/<int:listing_id>", views.close_auction, name="close_auction")
]
