import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse

from .models import User, Post, Follow, Like


def index(request):
    posts = Post.objects.all().order_by("-timestamp")
    paginator = Paginator(posts, 10)
    pageNumber = request.GET.get("page")
    pageObj = paginator.get_page(pageNumber)
    postsWithLikes = []
    for post in pageObj:
        if request.user.is_authenticated:
            isLiked = Like.objects.filter(
                user=request.user,
                post=post
            ).exists()
        else:
            isLiked = False
        likes = Like.objects.filter(post=post).count()
        postsWithLikes.append({
            "post": post,
            "isLiked": isLiked,
            "likes": likes
        })
        
    return render(request, "network/index.html", {
        "pageObj": pageObj,
        "postsWithLikes": postsWithLikes
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
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def post(request):
    if request.method == "POST":
        content = request.POST["content"]
        user = request.user
        Post.objects.create(
            user = user,
            content = content
        )
        return HttpResponseRedirect(reverse("index"))

@login_required
def profile(request, username):
    loggedUser = request.user
    user = User.objects.get(username=username)
    if request.method == "POST":
        action = request.POST["action"]
        if action == "follow":
            Follow.objects.get_or_create(
                follower=loggedUser,
                following=user
            )
        elif action == "unfollow":
            Follow.objects.filter(
                follower=loggedUser,
                following=user
            ).delete()
    isFollowing = Follow.objects.filter(
        follower=loggedUser,
        following=user
    ).exists()
    posts = Post.objects.filter(
        user=user
    ).order_by("-timestamp")
    paginator = Paginator(posts, 10)
    pageNumber = request.GET.get("page")
    pageObj = paginator.get_page(pageNumber)
    followers = user.followers.count()
    following = user.following.count()
    return render(request, "network/profile.html", {
        "profile": user,
        "posts": pageObj,
        "followers": followers,
        "following": following,
        "isFollowing": isFollowing
    })

@login_required
def following(request):
    loggedUser = request.user
    followedUsers = loggedUser.following.values_list(
        "following",
        flat=True
    )
    posts = Post.objects.filter(user__in = followedUsers).order_by("-timestamp")
    paginator = Paginator(posts, 10)
    pageNumber = request.GET.get("page")
    pageObj = paginator.get_page(pageNumber)

    return render(request, "network/following.html", {
        "posts": pageObj
    })

def edit(request, postId):
    if request.method == "POST":
        post = Post.objects.get(id=postId)
        if request.user != post.user:
            return JsonResponse({
                "error": "You cannot edit this post."
            }, status=403)
        data = json.loads(request.body)
        post.content = data["content"]
        post.save()
        return JsonResponse({
            "message": "Post updated successfully"
        })

@login_required
def like(request, postId):
    if request.method == "POST":
        user = request.user
        post = Post.objects.get(id=postId)
        isLiked = Like.objects.filter(
            user=user,
            post=post
        ).exists()
        if isLiked:
            Like.objects.filter(
                user=user,
                post=post
            ).delete()
            isLiked = False
        else:
            Like.objects.create(
                user=user,
                post=post
            )
            isLiked = True
        return JsonResponse({
            "likes": Like.objects.filter(post=post).count(),
            "isLiked": isLiked
        })