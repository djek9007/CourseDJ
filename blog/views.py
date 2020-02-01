from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from .models import Category, Post


class HomeView(View):
    """Home page"""
    def get(self, request):

        category_list = Category.objects.all()
        post_list = Post.objects.filter(published=True, published_date__lte=datetime.now())
        context = {
            'categories': category_list,
            'post_list': post_list,
        }
        return render(request, 'blog/post_list.html', context)

    def post(self, request):
        pass

class PostDetailView(View):
    """Полная статья одного статьи"""
    def get(self, request, category, slug):
        category_list = Category.objects.all()
        post = Post.objects.get(slug=slug)
        context = {
            'categories': category_list,
            'post': post,
        }
        return render(request, post.template, context)

class CategoryView(View):
    """Вывод категории"""
    def get(self, request, category_name):
        category = Category.objects.get(slug=category_name)
        return render(request, 'blog/post_list.html', {'category': category} )

class PostView(View):
    """Вывод всех постов"""
    def get(self, request):
        posts = Post.objects.all()
        return render(request, 'blog/post_list.html', {'posts': posts})