from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from articles.views import home
from search.views import search

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('articles.urls')),
    path('search/', search, name='search'),
    path('recipes/', include('recipes.urls')),
    path('accounts/', include('accounts.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
