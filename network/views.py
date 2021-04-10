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
            #create a user profile for that user
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
    # If there is an error the site should present error message
    return render(request,"network/error.html",{
        "message": "Some problem happened while you submited your Post"
    })

def profile(request,username):

    flag = 2 # 0 - user doesnt follow the profile that is visited 1 - user follow the profile that is visited 2 - default

    #number of followers
    followers = 0

    #User of the profile that is visited
    user = User.objects.get(username = username)

    #Posts of that user
    user_posts = Post.objects.filter(user = user)

    #Reverse Chronological Order
    user_posts = user_posts.order_by('-created_at')

    #get profile of the user
    profile_user = UserProfile.objects.get(user = user)

    #List of people following
    following = profile_user.following

    #list of profiles except the one that is being visited
    profiles = UserProfile.objects.all().exclude(user = user)

    #Gets the number of followers
    for profile in profiles:

        list_following = profile.following
        if(user in list_following.all()):
            followers += 1

    # if the profile visited is not from the person's that is logged in

    if(username != request.user.username):

        user_logged_in = User.objects.get(username = request.user.username)
        user_p_logged_in = UserProfile.objects.get(user = user_logged_in)

        #Check if the user that is visiting another profile alreadys follows that profile

        if(user in user_p_logged_in.following.all()):
            flag = 1

        else:
            flag = 0

    return render(request, "network/profile.html",{
        "posts":user_posts,"username":username,"following":following.count(),"followers":followers,"flag":flag
    })


def handleFollow(request,username,flag):

    #User that will unfollow or unfollow the user with username that comes in the function
    user_logged_in = User.objects.get(username = request.user.username)
    user_p_logged_in = UserProfile.objects.get(user = user_logged_in)

    #User that will be followed or unfollowed
    user_f = User.objects.get(username = username)

    #Unfollow
    if flag == 1:

        user_p_logged_in.following.remove(user_f)
        user_p_logged_in.save()

    #Follow
    elif flag == 0:

        user_p_logged_in.following.add(user_f)
        user_p_logged_in.save()

    #Redirects back to the profile view
    return redirect("profile",username)
