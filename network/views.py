import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse



from .models import User,Post, UserProfile, Like

class NewPostForm(forms.Form):

    New_Post = forms.CharField(widget = forms.Textarea(
        attrs = {
            'class': 'form-control','cols': 5, 'rows': 3
        }
    ))


def index(request):
    all_posts = Post.objects.all() #- means that its desceding order newer to older
    all_posts = all_posts.order_by('-created_at')

    #Takes care ot the likes
    for post in all_posts:
        post.likes = post.user_likes.count()



    page = request.GET.get('page', 1)

    #Only shows 10 posts per Page
    paginator = Paginator(all_posts, 10)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)


    return render(request, "network/index.html",{
        "posts":posts
    })

@login_required(login_url='index') #redirect when user is not logged in
def newPost(request):

    return render(request,"network/newPost.html",{
        "form":NewPostForm()
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

    #Paginates the posts

    page = request.GET.get('page', 1)

    #Only shows 10 posts per Page
    paginator = Paginator(user_posts, 10)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, "network/profile.html",{
        "posts":posts,"username":username,"following":following.count(),"followers":followers,"flag":flag
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

#ONly shows posts of the people that the user follows
@login_required(login_url='index') #redirect when user is not logged in
def following(request):


    # Following
    user_logged_in = User.objects.get(username = request.user.username)
    user_p_logged_in = UserProfile.objects.get(user = user_logged_in)

    following_list = user_p_logged_in.following.all()

    #Get all posts
    all_posts = Post.objects.all() #- means that its desceding order newer to older
    all_posts = all_posts.order_by('-created_at')

    following_posts = all_posts

    #Takes out the posts that belong to users that are not in the following list
    for post in all_posts.all():

        if(post.user not in following_list):
            following_posts = following_posts.all().exclude(user = post.user)


    #Paginates the posts

    page = request.GET.get('page', 1)

    #Only shows 10 posts per Page
    paginator = Paginator(following_posts, 10)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)


    return render(request, "network/following.html",{
        "posts":posts
    })


@csrf_exempt
def edit_posts(request,id):

    # Query for requested post
    try:
        post = Post.objects.get(pk=id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    #Prevents other users from editing someone else posts
    if(post.user != request.user):
        return JsonResponse({"error": "You are not authorized to edit other people posts."}, status=404)


    if request.method == "PUT":
        # Update whether email is read or should be archived
        data = json.loads(request.body)
        body = data.get("body", "")
        post.text = body
        post.save()
        return HttpResponse(status=204)

@csrf_exempt
def manage_likes(request,id):

    # Query for requested post
    try:
        post = Post.objects.get(pk=id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("like") == False:
            post.user_likes.remove(request.user)

        elif data.get("like") == True:
            post.user_likes.add(request.user)
        post.likes = post.user_likes.count()
        post.save()

        return JsonResponse({'likes':post.likes})
