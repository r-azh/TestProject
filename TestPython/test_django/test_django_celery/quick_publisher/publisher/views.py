from django.shortcuts import render
from django.http import Http404
from .models import Post


def view_post(request, slug):
    try:
        post = Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        raise Http404('Post does not exists')

    post.view_count += 1
    post.save()

    return render(request, 'post.html', context={'post': post})
