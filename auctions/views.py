from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView
from django import forms
import re

from .models import *

class RegisterForm (forms.ModelForm):
    class Meta:
        model = Auction
        fields = ['name', 'categorie', 'picture', 'price', 'text']

class BidForm (forms.Form):
    bid = forms.DecimalField(max_digits=8, decimal_places=2, required=False, label=False, widget=forms.NumberInput(attrs={'placeholder': 'Bid'}))

class CommentForm (forms.Form):
    comment = forms.CharField(max_length=200, required=False, label=False, widget=forms.TextInput(attrs={'placeholder': 'Comment'}))


def index(request):
    return render(request, "auctions/index.html", {
        "auctions": Auction.objects.all()
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

def categories(request):
    cat = [lis[1] for lis in Auction.categories] 
    return render(request, "auctions/categories.html", {
        "categories": cat
        })

def watchlist(request):
    pass

def newlisting(request):
    user = request.user
    if user.is_authenticated:
        if request.method == "POST":
            name = request.POST["name"]
            categorie = request.POST["categorie"]
            picture = request.POST["picture"]
            price = request.POST["price"]
            text = request.POST["text"]
            
            try:
                auction = Auction(name=name, categorie=categorie, picture=picture, price=price, text=text, user=user, active=True)
                auction.save()
            except IntegrityError:
                return render(request, "auctions/newlisting.html", {
                    "message": "An auction with this name already exists.",
                    "form": RegisterForm()
                    })
            return render(request, "auctions/index.html", {
                "auctions": Auction.objects.all()
                })
        else:
            return render(request, "auctions/newlisting.html", {
                "form": RegisterForm()
                })
    else:
        return render(request, "auctions/login.html")

def listinggroup(request, categorie_name):
    listings = Auction.objects.filter(categorie=categorie_name)
    return render(request, "auctions/index.html", {
        "auctions": listings,
        "side": "Categorie",
        "categorie": categorie_name
        })

def watchlist(request):
    user = request.user
    if user.is_authenticated:
        watched = Watchlist.objects.filter(user=user.pk)
        listings = Auction.objects.filter(pk__in=[e.item.id for e in watched])
        return render(request, "auctions/index.html", {
            "auctions": listings,
            "side": "Watchlist"
            })
    else:
        return render(request, "auctions/login.html")

def item(request, item):
    user = request.user
    if user.is_authenticated:
        listing = Auction.objects.get(name=item)
        comments = Comment.objects.filter(item=listing.pk)
        lastBid = Bid.objects.filter(item=listing.pk).last()
        message = []
        win = []
        try:
            watch = Watchlist.objects.get(item=listing, user=user)
        except Watchlist.DoesNotExist:
            watch = []
        if request.method == "POST":
            if 'bidSubmit' in request.POST:
                bid_value = float(request.POST["bid"])
                if bid_value > listing.price:
                    new_bid = Bid(item=listing, bid=bid_value, user=user)
                    new_bid.save()
                    listing.price = f"{bid_value:.2f}"
                    listing.save()
                    message = "Bid accomplished! Your bid is the current bid."
                else:
                    message = "Error: Your bid has to be higher than the actual Price!"
            elif 'commentSubmit' in request.POST:
                comment_new = request.POST["comment"]
                comment_entry = Comment(item=listing, text=comment_new, user=user)
                comment_entry.save()
            elif 'addWatchlist' in request.POST:
                watchlist = Watchlist(item=listing, user=user)
                watchlist.save()
                watch = "Yes"
            elif 'removeWatchlist' in request.POST:
                watch.delete()
                watch = []
            elif 'closeSubmit' in request.POST:
                listing.active = False
                listing.save()
            if user == lastBid.user:
                message = "Your bid is the current bid."
                win = True
        elif user == lastBid.user:
            message = "Your bid is the current bid."
            win = True
        return render(request, "auctions/item.html", {
                "item": listing,
                "comments": comments,
                "form_bid": BidForm(),
                "form_comment": CommentForm(),
                "message": message,
                "watchlist": watch,
                "win": win
                })
    else:
        return render(request, "auctions/login.html")


