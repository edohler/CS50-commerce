from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("new", views.newlisting, name="newlisting"),
    path("categories/<str:categorie_name>", views.listinggroup, name="listinggroup"),
    path("listings/<str:item>", views.item, name="item")
]
