from django.shortcuts import render, get_object_or_404
from .models import Post, Category
from django.utils import timezone


def index(request):  
    post_list = Post.objects.published().annotate_comments_index()
    return render(request, 'blog/index.html', {'post_list': post_list})


def post_detail(request, id):
    post = get_object_or_404(
        Post,
        pk=id,
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True
    )
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True)
    post_list = category.post_set.filter(is_published=True, pub_date__lte=timezone.now())
    context = {
        'category': category,
        'post_list': post_list
    }
    return render(request, 'blog/category.html', context)
