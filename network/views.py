import json
import logging
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,HttpResponseBadRequest, HttpResponseServerError
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


from .models import User, Post

def index(request):
    user = request.user
    #get all posts by reverse chronological order
    post_list = Post.objects.all().order_by('-timestamp')
    
    #paginator django system
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "network/index.html",{
       "posts": page_obj,
       "user": user,
    })

@login_required
def following_posts(request):
    user = request.user
    followed_users = user.following_users.all()
    post_list = Post.objects.filter(creator__in=followed_users).order_by('-timestamp')
    
    #paginator django system
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "network/following.html",{
       "posts": page_obj,
    })
    
@login_required 
def new_post(request):
    user = request.user
    post_content = request.POST["postContent"]
    
    post_list = Post.objects.all().order_by('-timestamp')
    
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # checks if the post content return has a value
    if post_content:
        add_post = Post(
            creator = user,
            content = post_content,
        )
        add_post.save()
        
        return HttpResponseRedirect(reverse(index)) 
    else:
        return HttpResponseRedirect(reverse(index)) 
    

def view_profile(request, id):
    user = request.user
    profile_user = get_object_or_404(User, pk=id)
    post_list = Post.objects.filter(creator=profile_user).order_by('-timestamp')
    is_followed = user in profile_user.follower_users.all()
    
    #paginator django system
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "network/profile.html",{ 
    "profile": profile_user,
    "posts": page_obj,
    "user": user,
    "is_followed": is_followed,                          
    })

@login_required
def follow_user(request,id):
    profile_user = get_object_or_404(User, pk=id)
    
    user = request.user
    
    
    profile_user.follower_users.add(user)
    user.following_users.add(profile_user)
        
    return HttpResponseRedirect(reverse("viewProfile", args=(id, )))

@login_required
def unfollow_user(request,id):
    profile_user = get_object_or_404(User, pk=id)
    
    user = request.user
    
    
    profile_user.follower_users.remove(user)
    user.following_users.remove(profile_user)
    
    return HttpResponseRedirect(reverse("viewProfile", args=(id, )))

@login_required
def editPost(request,id):
    post = Post.objects.get(pk=id)
    user = request.user
    
    # checks if it's a put method and the user is the same as the post creator
    # if so, save edit
    if request.method == "PUT" and user == post.creator:
        data = json.loads(request.body)
        post.content = data["content"]
        post.save()
        return HttpResponse(status=204)
    
   
        
@login_required
def likePost(request, id):
    post = Post.objects.get(pk=id)
    user = request.user
    
    if request.method == "PUT":
        data = json.loads(request.body)
        # checks if the user is in the likes array
        if not post.likes.filter(pk=user.pk).exists():
            post.likes.add(user)
            post.save()
            like_count = post.likes.count()
            return JsonResponse({'like_count': like_count}, status=201)
        else:
            post.likes.remove(user)
            post.save()
            like_count = post.likes.count()
            return JsonResponse({'like_count': like_count}, status=201)
    else:
        return HttpResponseBadRequest('Invalid request method')
        
        
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
