from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']

    def clean(self):
        data = self.cleaned_data
        title = data.get('title')
        content = data.get('content')
        qs = Article.objects.all().filter(title__icontains=title)
        if qs.exists():
            self.add_error('title', f"\"{title}\" is already in use.")
        return data
