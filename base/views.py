from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy, reverse
from .models import *
from .forms import *


# Create your views here.

def Home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    blogs = Blog.objects.filter(
        Q(topic__name__icontains=q) |
        Q(description__icontains=q)
    )[0:4]
    topics = Topic.objects.all()[0:20]

    context = {'blogs': blogs, 'topics': topics}
    return render(request, 'base/home.html', context)


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('bloglist')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('bloglist')
        else:
            messages.error(request, 'Username OR password does not exit')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('bloglist')


def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if not form.is_valid():
            messages.error(request, 'An error occured during registration')
        else:
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/login_register.html', context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    blogs = user.blog_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'blogs': blogs, 'topics': topics}
    return render(request, 'base/profile.html', context)


def blogList(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    blogs = Blog.objects.filter(
        Q(topic__name__icontains=q) |
        Q(description__icontains=q)
    )

    topics = Topic.objects.all()[0:20]
    blog_count = blogs.count()

    context = {'blogs': blogs, 'topics': topics,
               'blog_count': blog_count}
    return render(request, 'base/bloglist.html', context)


def blog(request, pk):
    blog = Blog.objects.get(id=pk)
    comments = blog.comment_set.all().order_by('-created')
    participants = blog.participants.all()

    if request.method == 'POST':
        if request.user.is_authenticated:
            comment = Comment.objects.create(
                user=request.user,
                blog=blog,
                body=request.POST.get('body')
            )
            blog.participants.add(request.user)
            return redirect('blog', pk=blog.id)
        else:
            return redirect('login')

    liked = False
    if blog.likes.filter(id=request.user.id).exists():
        liked = True

    total_likes = blog.likes.all()

    context = {'blog': blog,
               'comments': comments,
               'participants': participants,
               'liked': liked,
               'total_likes': total_likes}
    return render(request, 'base/blog.html', context)


@login_required(login_url='login')
def LikeView(request, pk):
    blog = get_object_or_404(Blog, id=request.POST.get('blog_id'))
    liked = False
    if blog.likes.filter(id=request.user.id).exists():
        blog.likes.remove(request.user)
        liked = False
    else:
        blog.likes.add(request.user)
        liked = True

    return redirect('blog', blog.id)


@login_required(login_url='login')
def createBlog(request):
    form = BlogForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Blog.objects.create(
            host=request.user,
            topic=topic,
            paragraph=request.POST.get('paragraph'),
            description=request.POST.get('description'),
        )
        return redirect('bloglist')

    context = {'form': form, 'topics': topics}
    return render(request, 'base/blog_form.html', context)


@login_required(login_url='login')
def updateBlog(request, pk):
    blog = Blog.objects.get(id=pk)
    form = BlogForm(instance=blog)
    topics = Topic.objects.all()
    if request.user != blog.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        blog.paragraph = request.POST.get('paragraph')
        blog.topic = topic
        blog.description = request.POST.get('description')
        blog.save()
        return redirect('bloglist')

    context = {'form': form, 'topics': topics, 'blog': blog}
    return render(request, 'base/blog_form.html', context)


@login_required(login_url='login')
def deleteBlog(request, pk):
    blog = Blog.objects.get(id=pk)

    if request.user != blog.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        blog.delete()
        return redirect('bloglist')
    return render(request, 'base/delete.html', {'obj': blog})


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/update-user.html', {'form': form})


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics': topics})


@login_required(login_url='login')
def deleteComment(request, pk):
    comment = Comment.objects.get(id=pk)

    if request.user != comment.user:
        return HttpResponse('You are not allowed here!!')

    if request.method == 'POST':
        comment.delete()
        return redirect('bloglist')

    context = {'obj': comment}
    return render(request, 'base/delete.html', context)