from django.test import TestCase
from django.utils.text import slugify

from .models import Article
from .utils import slugify_instance_title

class  ArticleTestCase(TestCase):
    def setUp(self):
        self.number_of_articles = 500
        for i in range(0, self.number_of_articles):
            Article.objects.create(title='hello world', content='this is something about hello world')

    def test_queryset_exists(self):
        qs = Article.objects.all()
        self.assertTrue(qs.exists())

    def test_queryset_count(self):
        qs = Article.objects.all()
        self.assertEqual(qs.count(), self.number_of_articles)

    def test_hello_world_slug(self):
        obj = Article.objects.all().order_by("id").first()
        title = obj.title
        slug = obj.slug
        slugified_title = slugify(title)
        self.assertEqual(slug, slugified_title)

    def test_hello_world_unique_slug(self):
        qs = Article.objects.exclude(slug__iexact='hello-world')
        for obj in qs:
            title = obj.title
            slug = obj.slug
            slugified_title = slugify(title)
            self.assertNotEqual(slug, slugified_title)

    def test_slugify_instance_title(self):
        obj = Article.objects.all().last()
        new_slugs = []
        for i in range(0, 25):
            instance = slugify_instance_title(obj, save=False)
            new_slugs.append(instance.slug)

        unique_slugs = list(set(new_slugs)) # set will remove all of the duplicates of the lists
        self.assertEqual(len(new_slugs), len(unique_slugs))

    def test_slugify_instance_title_redux(self):
        slugs = Article.objects.all().values_list('slug', flat=True)
        unique_slugs = list(set(slugs))
        self.assertEqual(len(slugs), len(unique_slugs))

    def test_article_search_manager(self):
        qs1 = Article.objects.search(query='hello world')
        self.assertEqual(qs1.count(), self.number_of_articles)

        qs2 = Article.objects.search(query='hello')
        self.assertEqual(qs2.count(), self.number_of_articles)

        qs3 = Article.objects.search(query='something')
        self.assertEqual(qs3.count(), self.number_of_articles)
