from django.db import models

# Create your models here.

class Article(models.Model):
    title = models.TextField()
    content = models.TextField()

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('article_detail', kwargs={'id' : self.id})

    def __str__(self):
        return self.title
