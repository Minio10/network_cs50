from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from django import forms


from .models import User,Post, UserProfile

class NewPostForm(forms.Form):

    New_Post = forms.CharField(widget = forms.Textarea(
        attrs = {
            'class': 'form-control','cols': 5, 'rows': 3
        }
    ))


def index(request):
    all_posts = Post.objects.all() #- means that its desceding order newer to older
    all_posts = all_posts.order_by('-created_at')
    return render(request, "network/index.html",{
        "posts":all_posts,"form":NewPostForm()
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            userp = UserProfile()
            userp.user = user
            user.save()
            userp.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def new_post(request):

    if request.method == "POST":
        form = NewPostForm(request.POST)

        #Saves the post on the DB
        if form.is_valid():
            text = form.cleaned_data["New_Post"]


            post = Post()
            post.text = text
            post.user = request.user

            post.save()
            return redirect("index")
    #If there is an error the site should present error message
    # return render(request,"auctions/error.html",{
    #     "message": "Some problem happened while you submited your Comment"
    # })

def profile(request,username):

    #User of the profile that is visited
    user = User.objects.get(username = username)

    #Posts of that user
    user_posts = Post.objects.filter(user = user)

    #Reverse Chronological Order
    user_posts = user_posts.order_by('-created_at')

    #get profile of the user
    profile_user = UserProfile.objects.get(user = user)

    following = profile_user.following


    return render(request, "network/profile.html",{
        "posts":user_posts,"username":username,"following":following.count()
    })
