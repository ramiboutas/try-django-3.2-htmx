from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required


from .models import Article
from .forms import ArticleForm
# Create your views here.


def home(request):
    context = {'articles': Article.objects.all() }
    return render(request, 'home.html', context)


def article_search(request):
    query = request.GET.get('q')
    qs = Article.objects.search(query)
    context = {'articles': qs}
    return render(request, 'articles/search.html', context)


def article_detail(request, slug):
    obj = get_object_or_404(Article, slug=slug)
    context = {'article': obj }
    return render(request, 'articles/detail.html', context)

@login_required
def article_create(request):
    form = ArticleForm(request.POST or None)
    if form.is_valid():
        article_obj = form.save()
        form = ArticleForm(None)
        return redirect(article_obj.get_absolute_url())
        # context['article'] = article_obj
    context = {"form": form }
    return render(request, 'articles/create.html', context)
