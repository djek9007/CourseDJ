from datetime import datetime

from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.views import View

from .forms import CommentForm
from .models import Category, Post, Comment


class PostListView(View):
    """Вывод категории и вывод стати"""

    # запрос к базе по полю публикации на true и по дате на сегодня которые должны выводится
    def get_queryset(self):
        return Post.objects.filter(published=True, published_date__lte=datetime.now())

    def get(self, request, category_slug=None, tag_slug=None):
        # category_list = Category.objects.filter(published=True)
        if category_slug is not None:
            posts = self.get_queryset().filter(category__slug=category_slug, category__published=True)
        elif tag_slug is not None:
            posts = self.get_queryset().filter(tags__slug=tag_slug, tags__published=True)
        else:
            posts = self.get_queryset()
        if posts.exists():
            template = posts.first().get_category_template()
        else:
            # template = 'blog/post_list.html'
            raise Http404()
        context = {
            # 'categories': category_list,
            'post_list': posts,
        }
        return render(request, template, context)


class PostDetailView(View):
    """Полная статья одного статьи"""
    def get(self, request, **kwargs):
        # category_list = Category.objects.filter(published=True)
        post = get_object_or_404(Post, slug=kwargs.get('slug'))
        form = CommentForm()
        context = {
            # 'categories': category_list,
            'post': post,
            'form': form
        }
        return render(request, post.template, context)

    def post(self, request, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.post = Post.objects.get(slug=kwargs.get('slug'))
            form.author = request.user
            form.save()
        return redirect(request.path)

