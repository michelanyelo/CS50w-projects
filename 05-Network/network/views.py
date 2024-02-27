from datetime import datetime, timezone
import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages


from .models import User, Post, Follow, Like


def index(request):
    if request.user.is_authenticated:
        current_user = request.user
        user_likes = Like.objects.filter(user=current_user)
        liked_posts_ids = [like.post.id for like in user_likes]
    else:
        liked_posts_ids = []

    all_posts = Post.objects.all().order_by("-id")
    paginator = Paginator(all_posts, 5)
    page_number = request.GET.get('page')
    posts_page = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "posts_page": posts_page,
        "liked_posts_ids": liked_posts_ids
    })

@login_required
def new_post(request):
    if request.method == "POST":
        content = request.POST.get('new_post_content')
        if content:
            user = request.user
            post = Post.objects.create(content=content, user=user)
            post.save()
            return HttpResponseRedirect(reverse(index))
        else:
            messages.error(
                request, 'El contenido del post está vacío. Por favor, escribe algo.')
    return HttpResponseRedirect(reverse(index))


# profile
def profile(request, user_id):
    user = User.objects.get(pk=user_id)
    all_posts = Post.objects.filter(user=user).order_by("id").reverse()
    following = Follow.objects.filter(user=user)
    followers = Follow.objects.filter(user_followed=user)

    try:
        check_follow = followers.filter(
            user=User.objects.get(pk=request.user.id))
        if len(check_follow) != 0:
            is_following = True
        else:
            is_following = False
    except:
        is_following = False

    # pagination
    paginator = Paginator(all_posts, 5)
    page_number = request.GET.get('page')
    posts_page = paginator.get_page(page_number)
    return render(request, "network/profile.html", {
        "posts_page": posts_page,
        "username": user.username,
        "following": following,
        "followers": followers,
        "is_following": is_following,
        "current_user": user
    })

@login_required
def follow(request):
    user_follow_username = request.POST['userfollow']
    current_user = User.objects.get(pk=request.user.id)
    user_to_follow = User.objects.get(username=user_follow_username)
    follow_instance = Follow(user=current_user, user_followed=user_to_follow)
    follow_instance.save()
    user_id = user_to_follow.id
    return HttpResponseRedirect(reverse(profile, kwargs={'user_id': user_id}))

@login_required
def unfollow(request):
    user_unfollow_username = request.POST['userunfollow']
    current_user = User.objects.get(pk=request.user.id)
    user_unfollow_data = User.objects.get(username=user_unfollow_username)

    Follow.objects.filter(
        user=current_user, user_followed=user_unfollow_data).delete()

    user_id = user_unfollow_data.id
    return HttpResponseRedirect(reverse('profile', kwargs={'user_id': user_id}))


def posts_following(request):
    current_user = request.user
    users_followed = Follow.objects.filter(
        user=current_user).values('user_followed')
    posts_from_following = Post.objects.filter(
        user__in=users_followed).order_by("id").reverse()

    # all likes
    current_user = request.user
    user_likes = Like.objects.filter(user=current_user)
    liked_posts_ids = [like.post.id for like in user_likes]

    # pagination
    paginator = Paginator(posts_from_following, 5)
    page_number = request.GET.get('page')
    posts_page = paginator.get_page(page_number)
    return render(request, "network/following.html", {
        "posts_page": posts_page,
        "liked_posts_ids": liked_posts_ids
    })


def add_like(request, post_id):
    post = Post.objects.get(pk=post_id)
    user = User.objects.get(pk=request.user.id)
    new_like = Like(user=user, post=post)
    new_like.save()
    return JsonResponse({
        "message": "Like added!"
    })


def remove_like(request, post_id):
    post = Post.objects.get(pk=post_id)
    user = User.objects.get(pk=request.user.id)
    remove_like = Like.objects.filter(user=user, post=post)
    remove_like.delete()
    return JsonResponse({
        "message": "Like removed"
    })


def edit(request, post_id):
    if request.method == "POST":
        data = json.loads(request.body)
        edit_post = Post.objects.get(pk=post_id)
        edit_post.content = data["content"]
        edit_post.modified = datetime.now(timezone.utc)
        edit_post.save()
        return JsonResponse({
            "message": "Change Successful",
            "data": data["content"],
            "modified": edit_post.modified.strftime("%d %b %Y %H:%M:%S")
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
