"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from app.views import article_detail, contact, event_detail, gallery_album_detail, index, actualites, services, evenements, formations, ressources, galerie, qui_sommes_nous, bible, bible_mediter, bible_reponses, spiritual_resource_detail, training_detail, robots_txt
from app.sitemaps import ArticleSitemap, EventSitemap, GalleryAlbumSitemap, SpiritualResourceSitemap, StaticViewSitemap, TrainingSitemap

sitemaps = {
    "static": StaticViewSitemap,
    "articles": ArticleSitemap,
    "events": EventSitemap,
    "trainings": TrainingSitemap,
    "resources": SpiritualResourceSitemap,
    "gallery": GalleryAlbumSitemap,
}


urlpatterns = [
    path("admin/", admin.site.urls),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    path("robots.txt", robots_txt, name="robots_txt"),
    path("", index, name="index"),
    path("actualites/", actualites, name="actualites"),
    path("services/", services, name="services"),
    path("evenements/", evenements, name="evenements"),
    path("formations/", formations, name="formations"),
    path("formation/<slug:slug>/", training_detail, name="training_detail"),
    path("ressources/", ressources, name="ressources"),
    path("ressource/<slug:slug>/", spiritual_resource_detail, name="spiritual_resource_detail"),
    path("galerie/", galerie, name="galerie"),
    path("galerie/album/<slug:slug>/", gallery_album_detail, name="gallery_album_detail"),
    path("qui-sommes-nous/", qui_sommes_nous, name="qui-sommes-nous"),
    path("bible/", bible, name="bible"),
    path("bible-mediter/", bible_mediter, name="bible_mediter"),
    path("bible-reponses/", bible_reponses, name="bible_reponses"),
    path("contact/", contact, name="contact"),
    path("article/<slug:slug>/", article_detail, name="article_detail"),
    path("event/<slug:slug>/", event_detail, name="event_detail"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Include django_browser_reload URLs only in DEBUG mode
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]