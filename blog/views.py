from django.shortcuts import render

from django.shortcuts import render, get_object_or_404
from .models import Blogpost



def blog_home(request):
    """Fetches all blog posts to display on the main blog page."""
    posts = Blogpost.objects.all()
    return render(request, 'blog/blog_home.html', {'myposts': posts})


def blog_detail(request):
    """Fetches all blog posts to display on the detail blog page."""
    posts = Blogpost.objects.all()
    return render(request, 'blog/blog_detail.html', {'myposts': posts})
