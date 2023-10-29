from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from .models import Article, Topic
from .forms import ArticleForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages


def loginPage(request):
  page ='login'
  
  if request.user.is_authenticated:
    return redirect('host') 
  if request.method == 'POST':
    username = request.POST.get('username').lower()
    password = request.POST.get('password')
    
    try:
      user = User.objects.get(username=username)
    except:
      messages.error(request, "User does not exist")
  
    user = authenticate(request, username=username, password=password)
  
    if user is not None:
      login(request, user)
      return redirect('home')
    else:
      messages.error(request, 'Username OR password does not exist')
    
  context={'page': page}
  
  return render(request, 'base/login_register.html', context)

def logoutUser(request):
  logout(request)
  return redirect('home')

def registerPage(request):
  form = UserCreationForm()
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save(commit=False)
      user.username = user.username.lower()
      user.save()
      login(request, user)
      return redirect('home')
    else:
      messages.error(request, 'An error occured during registration')
  context = {'form': form}
  return render(request, 'base/login_register.html', context)

def home(request):
  q = request.GET.get('q') if request.GET.get('q') != None else ''
  
  
  articles = Article.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q))
  
  topics = Topic.objects.all()
  article_count = articles.count()
    
  context = {'articles': articles, 'topics': topics, 'article_count':article_count}
  return render(request, 'base/home.html', context)


def article(request, pk):
  article = Article.objects.get(id=pk)
  context = {'article': article}
  return render(request, 'base/article.html', context)


@login_required(login_url='login')
def createArticle(request):
  form = ArticleForm()
  if request.method == 'POST':
    form = ArticleForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('home')
    
  context = {'form': form}
  return render(request, 'base/article_form.html', context)



@login_required(login_url='login')
def updateArticle(request, pk):
  article = Article.objects.get(id=pk)
  form = ArticleForm(instance=article)
  
  if request.user != article.author:
    return HttpResponse('You are not allowed here!!')
  
  if request.method == 'POST':
    form = ArticleForm(request.POST, instance=article)
    if form.is_valid():
      form.save()
      return redirect('home')
  context = {'form': form}
  return render(request, 'base/article_form.html', context)


@login_required(login_url='login')
def deleteArticle(request, pk):
  article = Article.objects.get(id=pk)
  
  if request.user != article.author:
    return HttpResponse('You are not allowed here!!')
  if request.method == 'POST':
    article.delete()
    return redirect('home')
  return render(request, 'base/delete.html', {'obj': article})
