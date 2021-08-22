from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Article
from .forms import ArticleForm
# Create your views here.



def article_search(request):
    print(request.GET)
    query_dict = request.GET
    query = query_dict.get('q')
    if query is not None:
        article_obj = get_object_or_404(Article, id=query)
    context = {'article': article_obj}
    return render(request, 'articles/search.html', context)



def article_detail(request, id):
    context = {'article': get_object_or_404(Article, id=id) }
    return render(request, 'articles/detail.html', context)

@login_required
def article_create(request):
    form = ArticleForm(request.POST or None)
    if form.is_valid():
        article_obj = form.save()
        form = ArticleForm(None)
        # context['article'] = article_obj
    context = {"form": form }
    return render(request, 'articles/create.html', context)
