from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from app.models import Article, Event, GalleryAlbum, SpiritualResource, Training


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = "weekly"

    def items(self):
        return [
            "index",
            "actualites",
            "services",
            "evenements",
            "formations",
            "ressources",
            "galerie",
            "qui-sommes-nous",
            "bible",
            "bible_mediter",
            "bible_reponses",
            "contact",
        ]

    def location(self, item):
        return reverse(item)


class ArticleSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return Article.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse("article_detail", args=[obj.slug])


class EventSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return Event.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse("event_detail", args=[obj.slug])


class TrainingSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return Training.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse("training_detail", args=[obj.slug])


class SpiritualResourceSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return SpiritualResource.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse("spiritual_resource_detail", args=[obj.slug])


class GalleryAlbumSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.4

    def items(self):
        return GalleryAlbum.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse("gallery_album_detail", args=[obj.slug])
