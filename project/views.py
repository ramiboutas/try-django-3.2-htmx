from django.shortcuts import render, get_object_or_404

from articles.models import Article

# Create your views here.


def home(request):
    context = {'articles': Article.objects.all() }
    return render(request, 'home.html', context)
