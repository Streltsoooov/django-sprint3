from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Post, Category
from django.db.models import Q
from django.utils import timezone


def index(request):
    post_list = Post.objects.select_related(
        'category', 'location', 'author'
    ).filter(
        Q(is_published=True) &
        Q(category__is_published=True) &
        Q(pub_date__lte=timezone.now())).order_by('-id')[0:5]
    return render(request, 'blog/index.html', {'post_list': post_list})


def post_detail(request, id):
    post = get_object_or_404(
        Post,
        pk=id,
        is_published=1,
        pub_date__lte=timezone.now(),
        category__is_published=1
    )
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    post_list = Post.objects.select_related('category').filter(
        Q(category__slug=category_slug) &
        Q(is_published=True) &
        Q(pub_date__lte=timezone.now())
    )
    category = get_object_or_404(Category, slug=category_slug, is_published=1)
    context = {
        'category': category,
        'post_list': post_list
    }
    return render(request, 'blog/category.html', context)
