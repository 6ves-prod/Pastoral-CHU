from django.db.models import Count, Max
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from app.models import (
    AccessInstruction,
    Article,
    BibleQuestion,
    BibleVerse,
    ContactChannel,
    ContactMessage,
    Event,
    ExternalLink,
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


def _base_context():
    return {
        "site_settings": SiteSettings.objects.filter(is_active=True).first(),
        "hero_slides": HeroSlide.objects.filter(is_active=True).order_by("order", "title"),
        "articles": Article.objects.filter(is_published=True).order_by("-published_at", "-created_at")[:6],
        "events": Event.objects.filter(is_published=True).order_by("start_date")[:6],
        "testimonials": Testimonial.objects.filter(is_published=True)[:6],
        "gallery_images": GalleryImage.objects.filter(is_published=True).order_by("order", "title")[:8],
        "page_sections": PageSection.objects.filter(is_published=True).order_by("order", "title").prefetch_related("tags"),
    }


def _page_sections(page_key):
    return PageSection.objects.filter(page_key=page_key, is_published=True).order_by("order", "title")


def _schedule(key):
    return Schedule.objects.filter(key=key).prefetch_related("slots").first()


def index(request):
    context = _base_context()
    context["daily_homily"] = Homily.objects.filter(is_published=True, genre="homelie").order_by("-published_at", "-created_at").first()
    return render(request, "index.html", context)


def actualites(request):
    context = _base_context()
    context["articles"] = Article.objects.filter(is_published=True).order_by("-published_at", "-created_at")
    context["events"] = Event.objects.filter(is_published=True).order_by("start_date")
    return render(request, "actualites.html", context)


def services(request):
    context = _base_context()
    context["service_offerings"] = ServiceOffering.objects.filter(is_published=True).order_by("order", "title").prefetch_related("items")
    context["chapel_schedule"] = _schedule("chapel_hours")
    context["mass_schedule"] = _schedule("masses")
    context["emergency_channels"] = ContactChannel.objects.filter(section_key__in=["services_urgence", "services_visite"], is_published=True).order_by("order")
    return render(request, "services/services.html", context)


def evenements(request):
    context = _base_context()
    context["events"] = Event.objects.filter(is_published=True).order_by("start_date")
    context["recurring_activities"] = RecurringActivity.objects.filter(is_published=True).order_by("order", "title")
    context["liturgical_seasons"] = LiturgicalSeason.objects.filter(is_published=True).order_by("order", "title").prefetch_related("items")
    context["contact_channels"] = ContactChannel.objects.filter(section_key="evenements_inscriptions", is_published=True).order_by("order")
    return render(request, "services/evenements.html", context)


def formations(request):
    context = _base_context()
    context["trainings"] = Training.objects.filter(is_published=True).exclude(type="session_info").order_by("start_date", "title")
    context["volunteer_path"] = Training.objects.filter(is_published=True, slug="parcours-de-formation-des-benevoles").prefetch_related("steps").first()
    context["conferences"] = Training.objects.filter(is_published=True, type__in=["conference", "seminaire"]).order_by("start_date", "title")[:2]
    context["info_sessions"] = Training.objects.filter(is_published=True, type="session_info").order_by("start_date", "title")
    context["contact_channels"] = ContactChannel.objects.filter(section_key="formations_renseignements", is_published=True).order_by("order")
    context["conditions_sections"] = _page_sections("formations")
    return render(request, "services/formations.html", context)


def training_detail(request, slug):
    training = Training.objects.filter(is_published=True, slug=slug).first()
    if not training:
        return render(request, "404.html", status=404)
    context = _base_context()
    context["training"] = training
    context["related_trainings"] = Training.objects.filter(is_published=True).exclude(pk=training.pk).order_by("start_date", "title")[:3]
    return render(request, "services/training_detail.html", context)


def ressources(request):
    context = _base_context()
    context["resources"] = SpiritualResource.objects.filter(is_published=True, resource_type__in=["meditation", "reflection"]).order_by("-published_at", "-created_at")
    context["prayers"] = SpiritualResource.objects.filter(is_published=True, resource_type="prayer").order_by("-published_at", "-created_at")
    context["documents"] = SpiritualResource.objects.filter(is_published=True, resource_type="guide").order_by("-published_at", "-created_at")
    context["external_links"] = ExternalLink.objects.filter(is_published=True).order_by("order", "title")
    context["specialized_contacts"] = ContactChannel.objects.filter(section_key="ressources_contacts", is_published=True).order_by("order")
    return render(request, "services/ressources.html", context)


def spiritual_resource_detail(request, slug):
    resource = SpiritualResource.objects.filter(is_published=True, slug=slug).first()
    if not resource:
        return render(request, "404.html", status=404)
    context = _base_context()
    context["resource"] = resource
    context["related_resources"] = SpiritualResource.objects.filter(is_published=True).exclude(pk=resource.pk).order_by("-published_at", "-created_at")[:3]
    return render(request, "services/spiritual_resource_detail.html", context)


def galerie(request):
    context = _base_context()
    context["albums"] = GalleryAlbum.objects.filter(is_published=True).order_by("order", "title").prefetch_related("images")
    context["library_documents"] = SpiritualResource.objects.filter(is_published=True, resource_type="guide").order_by("-published_at", "-created_at")[:6]
    context["resources_count"] = SpiritualResource.objects.filter(is_published=True).count()
    return render(request, "galerie.html", context)


def gallery_album_detail(request, slug):
    album = GalleryAlbum.objects.filter(is_published=True, slug=slug).first()
    if not album:
        return render(request, "404.html", status=404)
    context = _base_context()
    context["album"] = album
    context["album_images"] = album.images.filter(is_published=True).order_by("order", "title")
    context["related_albums"] = GalleryAlbum.objects.filter(is_published=True).exclude(pk=album.pk).order_by("order", "title")[:3]
    return render(request, "gallery_album_detail.html", context)


def qui_sommes_nous(request):
    context = _base_context()
    context["team_members"] = TeamMember.objects.filter(is_published=True).order_by("order", "full_name")
    context["partners"] = ContactChannel.objects.filter(section_key="about_partners", is_published=True).order_by("order")
    context["presence_schedule"] = _schedule("about_presence")
    return render(request, "qui-sommes-nous.html", context)


def bible(request):
    context = _base_context()
    context["daily_verses"] = BibleVerse.objects.filter(is_published=True, verse_type="daily").order_by("order", "reference")
    context["featured_questions"] = BibleQuestion.objects.filter(is_published=True).order_by("-created_at")[:2]
    context["bible_courses"] = Training.objects.filter(is_published=True, type="formation").order_by("start_date", "title")[:2]
    return render(request, "bible/bible.html", context)


def bible_mediter(request):
    context = _base_context()
    daily_meditation = Homily.objects.filter(is_published=True, genre="meditation").order_by("-published_at", "-created_at").first()
    context["daily_meditation"] = daily_meditation
    guided_meditations = Homily.objects.filter(is_published=True, genre="meditation").order_by("-published_at", "-created_at")
    if daily_meditation:
        guided_meditations = guided_meditations.exclude(pk=daily_meditation.pk)
    context["guided_meditations"] = guided_meditations[:3]
    context["meditation_methods"] = MeditationMethod.objects.filter(is_published=True, category="method").order_by("order", "title").prefetch_related("steps")
    context["silence_practices"] = MeditationMethod.objects.filter(is_published=True, category="silence").order_by("order", "title").prefetch_related("steps")
    context["psalms"] = BibleVerse.objects.filter(is_published=True, verse_type="psalm").order_by("order", "reference")
    return render(request, "bible/bible-mediter.html", context)


def bible_reponses(request):
    context = _base_context()
    context["bible_questions"] = BibleQuestion.objects.filter(is_published=True).order_by("-created_at").prefetch_related("tags")
    context["contact_channels"] = ContactChannel.objects.filter(section_key="bible_questions", is_published=True).order_by("order")
    context["question_categories"] = (
        BibleQuestion.objects.filter(is_published=True)
        .values("category")
        .annotate(count=Count("id"), last_date=Max("created_at"))
        .order_by("category")
    )
    context["category_labels"] = dict(BibleQuestion.CATEGORY_CHOICES)
    return render(request, "bible/bible-reponses.html", context)


def article_detail(request, slug):
    article = Article.objects.filter(is_published=True, slug=slug).first()
    if not article:
        return render(request, "404.html", status=404)
    context = _base_context()
    context["article"] = article
    context["related_articles"] = Article.objects.filter(is_published=True).exclude(pk=article.pk).order_by("-published_at", "-created_at")[:3]
    return render(request, "article_detail.html", context)


def event_detail(request, slug):
    event = Event.objects.filter(is_published=True, slug=slug).first()
    if not event:
        return render(request, "404.html", status=404)
    context = _base_context()
    context["event"] = event
    context["related_events"] = Event.objects.filter(is_published=True).exclude(pk=event.pk).order_by("start_date")[:3]
    return render(request, "event_detail.html", context)


def contact(request):
    if request.method == "POST":
        ContactMessage.objects.create(
            full_name=request.POST.get("full_name", "").strip(),
            email=request.POST.get("email", "").strip(),
            phone=request.POST.get("phone", "").strip(),
            subject=request.POST.get("subject", "").strip(),
            message=request.POST.get("message", "").strip(),
        )
        return redirect(reverse("contact") + "?sent=1")

    context = _base_context()
    context["team_members"] = TeamMember.objects.filter(is_published=True).order_by("order", "full_name")
    context["permanence_schedule"] = _schedule("contact_permanences")
    context["access_instructions"] = AccessInstruction.objects.filter(is_published=True).order_by("order", "label")
    return render(request, "contact.html", context)


def robots_txt(request):
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        "",
        f"Sitemap: {request.scheme}://{request.get_host()}/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
