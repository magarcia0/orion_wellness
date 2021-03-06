from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from core.forms import JoinForm, LoginForm
from django.contrib.auth.models import User
from core.models import UserProfile
from django.core.cache import cache
import requests
import json
from workout.models import WorkoutEntry
from nutrition.models import NutritionEntry
import random
import time

# Create your views here.

@login_required(login_url='/login/')
def home(request):
    work_count = 0
    nutrition_count = 0
    db_actual = []
    db_projected = []
    consumed = []
    goal = []
    url = 'https://zenquotes.io/api/quotes/'
    quote_library = requests.get(url).json()
    api_data = random.sample(quote_library, 1)
    workout_data = WorkoutEntry.objects.filter(user=request.user)
    nutrition_data = NutritionEntry.objects.filter(user=request.user)
    work_count = len(workout_data) / 2
    for x in workout_data:
        work_count = work_count + 1
        db_actual.append(str(x.actual))
        db_projected.append(str(x.projected))
    for idx in nutrition_data:
        nutrition_count = nutrition_count + 1
        consumed.append(str(idx.calories))
        goal.append(str(idx.calories_goal))
    context = {
        'api_data': api_data,
        'work_count': work_count,
        'nutrition_count': nutrition_count,
        'db_actual': db_actual,
        'db_projected': db_projected,
        'consumed': consumed,
        'goal': goal,
    }
    return render(request, 'core/home.html/', context)

def about(request):
    return render(request, 'core/about.html')

def nutrition(request):
    return render(request, 'nutrition/nutrition.html')

def workout(request):
    return render(request, 'workout/workout.html')


def join(request):
    if (request.method == "POST"):
        join_form = JoinForm(request.POST)
        if (join_form.is_valid()):
            # Save form data to DB
            user = join_form.save()
        # Encrypt the password
            user.set_password(user.password)
        # Save encrypted password to DB
            user.save()
        # Success! Redirect to home page.
            return redirect("/")
        else:
            # Form invalid, print errors to console
            page_data = {"join_form": join_form}
            return render(request, 'core/join.html', page_data)
    else:
        join_form = JoinForm()
        page_data = {"join_form": join_form}
        return render(request, 'core/join.html', page_data)


def user_login(request):
    if (request.method == 'POST'):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # First get the username and password supplied
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            # Django's built-in authentication function:
            user = authenticate(username=username, password=password)
            # If we have a user
            if user:
                # Check it the account is active
                if user.is_active:
                    # Log the user in.
                    login(request, user)
                    # Send the user back to homepage
                    return redirect("/")
                else:
                    # If account is not active:
                    return HttpResponse("Your account is not active.")
            else:
                print("Someone tried to login and failed.")
                print("They used username: {} and password: {}".format(username, password))
                return render(request, 'core/login.html', {"login_form": LoginForm})
    else:
        # Nothing has been provided for username or password.
        return render(request, 'core/login.html', {"login_form": LoginForm})

def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return redirect("/")