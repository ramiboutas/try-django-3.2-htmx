import uuid
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.text import slugify
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .utils import slugify_instance_title

User = settings.AUTH_USER_MODEL


class ArticleQuerySet(models.QuerySet):
    def search(self, query=None):
        if query is None or query=="":
            return self.none()
        lookups = Q(title__icontains=query) | Q(content__icontains=query)
        return self.filter(lookups)


class ArticleManager(models.Manager):
    def get_queryset(self):
        return ArticleQuerySet(self.model, using=self._db)

    def search(self, query):
        return self.get_queryset().search(query=query)

class Article(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True, null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    published = models.DateField(auto_now_add=True, null=True, blank=True)

    objects = ArticleManager()

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('article_detail', kwargs={'slug' : self.slug})

    def __str__(self):
        return self.title


# signals -> when a instance of an article is created or updated

@receiver(pre_save, sender=Article)
def article_pre_save(sender, instance, *args, **kwargs):
    # print("Pre-save")
    if instance.slug is None:
        slugify_instance_title(instance, save=False)


@receiver(post_save, sender=Article)
def article_post_save(sender, instance, created, *args, **kwargs):
    # print("Post-save")
    if created:
        slugify_instance_title(instance, save=True)
