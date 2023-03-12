from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request


def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('psw')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('djangoapp:index')
    else:
        messages.error(request, "Invalid method.")
        return redirect('djangoapp:index')


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("djangoapp:index")


# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(
                username=username, password=password, first_name=first_name, last_name=last_name)
            user.save()
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships


def get_dealerships(request):
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/bec822c8-a2c5-45b1-8f87-735b5416bfde/dealership-package/get-dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/bec822c8-a2c5-45b1-8f87-735b5416bfde/dealership-package/get-review/"
        # Get dealers from the URL
        dealer_reviews = get_dealer_reviews_from_cf(url, dealer_id)
        # Concat all dealer's name
        dealer_names = ' '.join(
            [dealer.sentiment for dealer in dealer_reviews])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)


# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    url = "https://us-south.functions.appdomain.cloud/api/v1/web/bec822c8-a2c5-45b1-8f87-735b5416bfde/dealership-package/post-review"
    if User.is_authenticated:
        if request.method == "POST":
            review = {}
            review["id"] = request.POST.get("id")
            review["name"] = request.POST.get("name")
            review["dealership"] = dealer_id
            review["review"] = request.POST.get("review")
            review["purchase"] = request.POST.get("purchase")
            review["purchase_date"] = datetime.strptime(
                request.POST.get("purchase_date"), '%m-%d-%Y')
            review["car_make"] = request.POST.get("car_make")
            review["car_model"] = request.POST.get("car_model")
            review["car_year"] = request.POST.get("car_year")
            json_payload = {}
            json_payload["review"] = review
            post_request(url, json_payload, dealer_id=dealer_id)
            print("Review added")
    else:
        print("User not authenticated")
