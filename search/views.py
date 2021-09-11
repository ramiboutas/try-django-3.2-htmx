from django.shortcuts import render

def search(request):
    query = request.GET.get('q')
    context = {'queryset': query}
    template = "search/results.html"
    if request.htmx:
        template = "search/partials/hx-results.html"
    return render(request, template, context)
