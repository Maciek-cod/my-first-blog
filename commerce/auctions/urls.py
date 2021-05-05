from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("listing/<int:listing_id>/watchlistadd", views.watchlist_add, name="watchlistadd"),
    path("listing/<int:listing_id>/watchlistremove", views.watchlistremove, name="watchlistremove"),
    path("listing/<int:listing_id>/bid", views.place_bid, name="bid"),
    path("close/listing/<int:listing_id>", views.close_listing, name="close_listing"),
    path("closed", views.closed, name="closed"),
    path("listing/<int:listing_id>/comment", views.create_comment, name="comment"),
    path("mywatchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:cat>", views.category_view, name="category"),
]
