from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import User, Listing, Bid, Comment, Watchlist
from .forms import ItemForm, BidForm, CommentForm
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def index(request):
    listings = Listing.objects.all().order_by('id').filter(active=True)
    time_now = timezone.now()
    
    for listing in listings:
        listing.watched = ""
        watch_list = Watchlist.objects.filter(items=listing)

        for watch in watch_list:
            if watch.user == request.user:
                listing.watched = "*"
    
    context = {
        'listings':listings,
        'time_now':time_now,
    }
    return render(request, "auctions/index.html", context=context)


def closed(request):
    listings = Listing.objects.all().order_by('id').filter(active=False)
    time_now = timezone.now()
    
    for listing in listings:
        listing.watched = ""
        watch_list = Watchlist.objects.filter(items=listing)

        for watch in watch_list:
            if watch.user == request.user:
                listing.watched = "*"
    
    context = {
        'listings': listings,
        'time_now': time_now,
    }
    return render(request, "auctions/closed.html", context=context)


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


def create(request):
    if request.method == "POST":
        form = ItemForm(request.POST)
        
        if form.is_valid():
            item = form.save(commit=False)
            item.author = request.user
            item.published_date = timezone.now()
            item.save()
            return render(request, "auctions/create.html", {
                'form': form,
                'message': 'Your item is now listed.',
            })
    else:
        form = ItemForm()
        return render(request, "auctions/create.html", {
            'form': form
        })


def listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    time_now = timezone.now()
    form = BidForm()
    comment_form = CommentForm()
    comments = Comment.objects.filter(listing=listing_id)

    context = {
        'listing': listing,
        'time_now': time_now,
        'form': form,
        'comment_form': comment_form,
        'comments': comments,
    }
    return render(request, "auctions/listing.html", context=context)


def watchlist_add(request, listing_id):
    item_to_save = get_object_or_404(Listing, pk=listing_id)

    if Watchlist.objects.filter(user=request.user, items=listing_id).exists():
        return HttpResponseRedirect(reverse("index"))
        
    user_list, created = Watchlist.objects.get_or_create(user=request.user)
    user_list.items.add(item_to_save)
    messages.add_message(request, messages.SUCCESS, "Successfully added to your watchlist")
    return HttpResponseRedirect(reverse("index"))


def watchlistremove(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    watchlist = Watchlist.objects.get(user=request.user)
    watchlist.items.remove(listing)
    watchlist.save()
    return HttpResponseRedirect(reverse("index"))


def place_bid(request, listing_id):
    if request.method == 'POST':
        auction_to_add = Listing.objects.get(id=listing_id)
        total_bid = request.POST["bid"]
        if int(total_bid) <= auction_to_add.start_bit:
            return HttpResponse('Your bid must be bigger then initial bid.')
        if  auction_to_add.last_bid is None:
            bid = Bid.objects.create(user=auction_to_add.author, listing=auction_to_add, bid=auction_to_add.start_bit)
            auction_to_add.bids.add(bid)
            auction_to_add.last_bid = bid
            auction_to_add.save()
        if int(total_bid) <= auction_to_add.last_bid.bid:
            return HttpResponse('Your bid must be bigger then current bid.')
        
        bid = Bid.objects.create(user=request.user, listing=auction_to_add, bid=total_bid)
        auction_to_add.bids.add(bid)
        auction_to_add.last_bid = bid
        auction_to_add.save()
        return HttpResponseRedirect(reverse("listing", kwargs={'listing_id':listing_id}))


def create_comment(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    time_now = timezone.now()
    form = BidForm()

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.listing = Listing.objects.filter(id = listing_id).first()
            comment.user = request.user
            comment.date = timezone.now()
            comment.save()
    
    comment_form = CommentForm()
    comments = Comment.objects.filter(listing=listing_id)
    
    context = {
        'listing': listing,
        'time_now': time_now,
        'form': form,
        'comment_form': comment_form,
        'comments': comments,
    }
    return render(request, "auctions/listing.html", context=context)


@login_required
def close_listing(request, listing_id):
    if request.method == 'GET':
        listing_object = Listing.objects.get(id=listing_id)
        winner = Bid.objects.filter(listing=listing_object).first()

        if winner is None:
            listing_object.active = False
            listing_object.save()
        else:
            listing_object.winner = winner.user
            listing_object.active = False
            listing_object.save()

        return HttpResponseRedirect(reverse("index"))


def watchlist (request):
    my_list = Watchlist.objects.filter(user=request.user)

    if my_list:
        my_watchlist = my_list[0]
        time_now = timezone.now()
        
        context = {
            'items': my_watchlist.items.all(),
            'time_now': time_now,
        }
        return render(request, "auctions/watchlist.html", context=context)
    else:
        return render(request, "auctions/watchlist.html", {
        "error": 'Your Watchlist is empty.'
    })

def categories (request):
    l = []
    li = Listing.objects.all()
    
    for listing in li:
        if listing.category:
            if listing.category not in l:
                l.append(listing.category)
                
    return render(request, "auctions/categories.html", {
        "the_categories": l
    })


def category_view (request, cat):
    the_category = Listing.objects.filter(category=cat)
    time_now = timezone.now()
    l = []
    li = Listing.objects.all()
    
    for listing in li:
        if listing.category:
            if listing.category not in l:
                l.append(listing.category)

    return render(request, "auctions/categories.html", {
        "category": cat,
        "categories": the_category,
        "the_categories": l,
        "time_now": time_now,
    })