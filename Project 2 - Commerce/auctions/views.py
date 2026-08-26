from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from decimal import Decimal

from .models import User, AuctionListing, Watchlist, Bid, Comment


def index(request):
    return render(request, "auctions/index.html")


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

@login_required
def createListing(request):
    category = request.POST.get("category")
    if request.method == "GET":
        return render(request, "auctions/createListing.html")
    
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        starting_bid = request.POST.get("starting_bid")
        image_url = request.POST.get("image_url")
        AuctionListing.objects.create(
            title = title,
            description = description,
            starting_bid = starting_bid,
            image_url = image_url,
            category = category,
            created_by = request.user
        )
        return HttpResponseRedirect(reverse("index"))
        
def index(request):
    listings = AuctionListing.objects.filter(is_active=True)

    return render(request, "auctions/index.html", {
        "listings": listings
    })

def listing(request, listing_id):
    listing = AuctionListing.objects.get(id=listing_id)

    if request.user.is_authenticated:
        is_watchlisted = Watchlist.objects.filter(
            user=request.user,
            listing=listing
        ).exists()
    else:
        is_watchlisted = False

    bids = Bid.objects.filter(listing=listing).order_by("-amount")
    highestBid = bids.first()
    comments = Comment.objects.filter(listing=listing)

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "is_watchlisted": is_watchlisted,
        "highestBid": highestBid,
        "comments": comments
    })

@login_required
def watchlist(request, listing_id):
    listing = AuctionListing.objects.get(id=listing_id)

    if Watchlist.objects.filter(
        user=request.user,
        listing=listing
    ).exists():
        Watchlist_item = Watchlist.objects.get(
            user=request.user,
            listing=listing
        )
        Watchlist_item.delete()
    else:
        Watchlist.objects.create(
            user=request.user,
            listing=listing
        )

    return HttpResponseRedirect(
        reverse("listing", args=[listing_id])
    )

@login_required
def watchlistPage(request):
    watchlist_items = Watchlist.objects.filter(user=request.user)

    return render(request, "auctions/watchlist.html", {
        "watchlist_items": watchlist_items
    })

@login_required
def bid(request, listing_id):
    listing = AuctionListing.objects.get(id=listing_id)
    if not listing.is_active:
        return redirect("listing", listing_id=listing.id)
    bidAmt = Decimal(request.POST.get("bid"))

    bids = Bid.objects.filter(listing=listing).order_by("-amount")
    highestBid = bids.first()

    if highestBid is not None:
        if bidAmt > highestBid.amount:
            Bid.objects.create(
                bidder = request.user,
                listing = listing,
                amount = bidAmt

            )
            return HttpResponseRedirect(reverse("listing", args=[listing.id]))
        else: 
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "error": "Your bid must be greater than current highest bid."
            })
    else:
        if bidAmt >= listing.starting_bid:
            Bid.objects.create(
                bidder = request.user,
                listing = listing,
                amount = bidAmt
            )
            return HttpResponseRedirect(reverse("listing", args=[listing.id]))
        else: 
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "error": "Your bid must be at least the starting bid."
            })
        
@login_required
def close_listing(request, listing_id):
    listing = AuctionListing.objects.get(id=listing_id)

    if request.user != listing.created_by:
        return redirect("listing", listing_id=listing.id)

    bids = Bid.objects.filter(listing=listing).order_by("-amount")
    highest_bid = bids.first()

    if highest_bid:
        listing.winner = highest_bid.bidder

    listing.is_active = False
    listing.save()

    return redirect("listing", listing_id=listing.id)

@login_required
def comment(request, listing_id):
    listing = AuctionListing.objects.get(id=listing_id)
    text = request.POST.get("comment")

    Comment.objects.create(
        author=request.user,
        listing=listing,
        text=text
    )

    return redirect("listing", listing_id=listing.id)

def categories(request):
    categories = [
        "Electronics",
        "Clothing",
        "Toys",
        "Books"
    ]

    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def category(request, category):
    listings = AuctionListing.objects.filter(
        category=category,
        is_active=True
    )

    return render(request, "auctions/category.html", {
        "listings": listings,
        "category": category
    })