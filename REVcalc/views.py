from typing import NewType
from django.http import request
from django.shortcuts import HttpResponseRedirect, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.db import IntegrityError
from .models import Sell_detail, User, Document, Transaction, Rate
from django.conf import settings
from .forms import DocumentForm
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'calcapp/index.html')

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, "calcapp/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "calcapp/login.html")

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
            return render(request, "calcapp/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "calcapp/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "calcapp/register.html")

@login_required
def load_data(request):
    files = Document.objects.filter(user=request.user)
    
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = request.user
            new_document = form.save() 
            Transaction.load_from_revolut_txt(new_document.document, request.user)
            Transaction.update_quantity_after_transaction(request.user)
            Rate.create_pln_rate(request.user)
            Sell_detail.create_sell_details(new_document.document, request.user)
            return redirect('load_data')
    else:
        form = DocumentForm()
    return render(request, 'calcapp/load_data.html', {
        'form': form,
        'files': files
    })

def my_transactions(request, user):
    user_transactions = Transaction.objects.filter(user=request.user).order_by('name', 'settle_date')
    active_transactions = Transaction.objects.filter(user=request.user, active=True, type="BUY").order_by('name','settle_date','type')

    total_profit = 0
    total_profit_pln = 0
    for transaction in user_transactions:
        for d in transaction.sold.all():
            total_profit += d.profit
            total_profit_pln += d.profit_pln

    tax = total_profit * 0.20
    tax_pln = float(total_profit_pln) * 0.19

    positive = ""
    if total_profit < 0:
        positive = "Your profit is negative"

    return render(request, "calcapp/my_transactions.html",{
        'user_transactions':user_transactions,
        'total_profit': total_profit,
        'tax': tax,
        'tax_pln': tax_pln,
        'positive': positive,
        'active_transactions': active_transactions,
        'total_profit_pln': total_profit_pln
        })