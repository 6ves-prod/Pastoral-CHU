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
from django.conf import settings
from django.urls import path, include
from app.views import index, actualites, services, evenements, formations, ressources, galerie, qui_sommes_nous, bible, bible_mediter, bible_reponses, contact


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index, name="index"),
    path("actualites/", actualites, name="actualites"),
    path("services/", services, name="services"),
    path("evenements/", evenements, name="evenements"),
    path("formations/", formations, name="formations"),
    path("ressources/", ressources, name="ressources"),
    path("galerie/", galerie, name="galerie"),
    path("qui-sommes-nous/", qui_sommes_nous, name="qui-sommes-nous"),
    path("bible/", bible, name="bible"),
    path("bible-mediter/", bible_mediter, name="bible-mediter"),
    path("bible-reponses/", bible_reponses, name="bible-reponses"),
    path("contact/", contact, name="contact"),
]

if settings.DEBUG:
    # Include django_browser_reload URLs only in DEBUG mode
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]