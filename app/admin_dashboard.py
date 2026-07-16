from django.contrib.auth.models import Group, User
from django.urls import reverse
from django.utils import timezone

from app.models import (
    AccessInstruction,
    Article,
    BibleQuestion,
    BibleVerse,
    Category,
    ContactChannel,
    ContactMessage,
    Event,
    ExternalLink,
    Father,
    GalleryAlbum,
    GalleryImage,
    HeroSlide,
    Homily,
    LiturgicalSeason,
    MeditationMethod,
    PageSection,
    RecurringActivity,
    Schedule,
    ServiceOffering,
    SiteSettings,
    SpiritualResource,
    TeamMember,
    Testimonial,
    Training,
)


def _app_link(model_name):
    return reverse(f"admin:app_{model_name}_changelist")


def _auth_link(model_name):
    return reverse(f"admin:auth_{model_name}_changelist")


def dashboard_callback(request, context):
    now = timezone.now()

    context.update(
        {
            "kpi_cards": [
                {
                    "title": "Messages non lus",
                    "value": ContactMessage.objects.filter(is_read=False).count(),
                    "icon": "mail",
                    "link": _app_link("contactmessage") + "?is_read__exact=0",
                },
                {
                    "title": "Événements à venir",
                    "value": Event.objects.filter(is_published=True, start_date__gte=now).count(),
                    "icon": "event",
                    "link": _app_link("event"),
                },
                {
                    "title": "Formations publiées",
                    "value": Training.objects.filter(is_published=True).count(),
                    "icon": "school",
                    "link": _app_link("training"),
                },
                {
                    "title": "Articles publiés",
                    "value": Article.objects.filter(is_published=True).count(),
                    "icon": "article",
                    "link": _app_link("article"),
                },
                {
                    "title": "Ressources spirituelles",
                    "value": SpiritualResource.objects.filter(is_published=True).count(),
                    "icon": "library_books",
                    "link": _app_link("spiritualresource"),
                },
                {
                    "title": "Albums photo",
                    "value": GalleryAlbum.objects.filter(is_published=True).count(),
                    "icon": "photo_library",
                    "link": _app_link("galleryalbum"),
                },
            ],
            "recent_messages": ContactMessage.objects.order_by("-created_at")[:5],
            "dashboard_groups": [
                {
                    "title": "Général",
                    "items": [
                        {"title": "Paramètres du site", "icon": "settings", "link": _app_link("sitesettings"), "count": SiteSettings.objects.count()},
                        {"title": "Sections de page", "icon": "dashboard_customize", "link": _app_link("pagesection"), "count": PageSection.objects.count()},
                        {"title": "Slides d'accueil", "icon": "view_carousel", "link": _app_link("heroslide"), "count": HeroSlide.objects.count()},
                        {"title": "Équipe", "icon": "groups", "link": _app_link("teammember"), "count": TeamMember.objects.count()},
                        {"title": "Liens externes", "icon": "link", "link": _app_link("externallink"), "count": ExternalLink.objects.count()},
                    ],
                },
                {
                    "title": "Actualités & Homélies",
                    "items": [
                        {"title": "Articles", "icon": "article", "link": _app_link("article"), "count": Article.objects.count()},
                        {"title": "Catégories", "icon": "category", "link": _app_link("category"), "count": Category.objects.count()},
                        {"title": "Pères", "icon": "person", "link": _app_link("father"), "count": Father.objects.count()},
                        {"title": "Homélies", "icon": "menu_book", "link": _app_link("homily"), "count": Homily.objects.count()},
                    ],
                },
                {
                    "title": "Bible & Méditation",
                    "items": [
                        {"title": "Versets bibliques", "icon": "auto_stories", "link": _app_link("bibleverse"), "count": BibleVerse.objects.count()},
                        {"title": "Questions bibliques", "icon": "quiz", "link": _app_link("biblequestion"), "count": BibleQuestion.objects.count()},
                        {"title": "Méditations", "icon": "self_improvement", "link": _app_link("meditationmethod"), "count": MeditationMethod.objects.count()},
                        {"title": "Temps liturgiques", "icon": "calendar_month", "link": _app_link("liturgicalseason"), "count": LiturgicalSeason.objects.count()},
                    ],
                },
                {
                    "title": "Événements & Formations",
                    "items": [
                        {"title": "Événements", "icon": "event", "link": _app_link("event"), "count": Event.objects.count()},
                        {"title": "Formations", "icon": "school", "link": _app_link("training"), "count": Training.objects.count()},
                    ],
                },
                {
                    "title": "Ressources spirituelles",
                    "items": [
                        {"title": "Ressources", "icon": "library_books", "link": _app_link("spiritualresource"), "count": SpiritualResource.objects.count()},
                    ],
                },
                {
                    "title": "Galerie photo",
                    "items": [
                        {"title": "Albums", "icon": "photo_library", "link": _app_link("galleryalbum"), "count": GalleryAlbum.objects.count()},
                        {"title": "Images", "icon": "image", "link": _app_link("galleryimage"), "count": GalleryImage.objects.count()},
                    ],
                },
                {
                    "title": "Services & Vie paroissiale",
                    "items": [
                        {"title": "Services proposés", "icon": "volunteer_activism", "link": _app_link("serviceoffering"), "count": ServiceOffering.objects.count()},
                        {"title": "Horaires", "icon": "schedule", "link": _app_link("schedule"), "count": Schedule.objects.count()},
                        {"title": "Activités régulières", "icon": "event_repeat", "link": _app_link("recurringactivity"), "count": RecurringActivity.objects.count()},
                        {"title": "Instructions d'accès", "icon": "directions", "link": _app_link("accessinstruction"), "count": AccessInstruction.objects.count()},
                    ],
                },
                {
                    "title": "Contact",
                    "items": [
                        {"title": "Messages reçus", "icon": "mail", "link": _app_link("contactmessage"), "count": ContactMessage.objects.count()},
                        {"title": "Cartes de contact", "icon": "call", "link": _app_link("contactchannel"), "count": ContactChannel.objects.count()},
                    ],
                },
                {
                    "title": "Témoignages",
                    "items": [
                        {"title": "Témoignages", "icon": "format_quote", "link": _app_link("testimonial"), "count": Testimonial.objects.count()},
                    ],
                },
                {
                    "title": "Utilisateurs & Rôles",
                    "items": [
                        {"title": "Utilisateurs", "icon": "person", "link": _auth_link("user"), "count": User.objects.count()},
                        {"title": "Rôles & permissions", "icon": "admin_panel_settings", "link": _auth_link("group"), "count": Group.objects.count()},
                    ],
                },
            ],
        }
    )

    return context
