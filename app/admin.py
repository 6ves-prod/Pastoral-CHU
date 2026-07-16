from django.contrib import admin
from django.http import JsonResponse
from django.urls import path
from unfold.admin import ModelAdmin, TabularInline

from app.models import (
    AccessInstruction,
    Article,
    BibleQuestion,
    BibleQuestionTag,
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
    LiturgicalSeasonItem,
    MeditationMethod,
    MeditationMethodStep,
    PageSection,
    PageSectionTag,
    RecurringActivity,
    Schedule,
    ScheduleSlot,
    ServiceOffering,
    ServiceOfferingItem,
    SiteSettings,
    SpiritualResource,
    TeamMember,
    Testimonial,
    Training,
    TrainingSkill,
    TrainingStep,
)


@admin.register(SiteSettings)
class SiteSettingsAdmin(ModelAdmin):
    list_display = ("site_name", "is_active", "contact_email", "updated_at")
    search_fields = ("site_name", "contact_email")
    list_filter = ("is_active",)


@admin.register(HeroSlide)
class HeroSlideAdmin(ModelAdmin):
    list_display = ("title", "slug", "is_active", "order")
    search_fields = ("title", "subtitle")
    list_filter = ("is_active",)
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ("name", "slug", "updated_at")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Father)
class FatherAdmin(ModelAdmin):
    list_display = ("full_name", "title", "is_active", "updated_at")
    search_fields = ("full_name", "title", "bio")
    list_filter = ("is_active",)


@admin.register(Article)
class ArticleAdmin(ModelAdmin):
    list_display = ("title", "category", "slug", "is_published", "published_at", "updated_at")
    search_fields = ("title", "content", "excerpt")
    list_filter = ("is_published", "published_at", "category")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"


@admin.register(Homily)
class HomilyAdmin(ModelAdmin):
    list_display = ("title", "gospel", "genre", "father", "is_published", "published_at", "updated_at")
    search_fields = ("title", "gospel", "content")
    list_filter = ("is_published", "genre", "father", "published_at")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"


class TrainingStepInline(TabularInline):
    model = TrainingStep
    extra = 1
    fields = ("title", "description", "duration_label", "order")
    ordering = ("order",)


class TrainingSkillInline(TabularInline):
    model = TrainingSkill
    extra = 1
    fields = ("text", "order")
    ordering = ("order",)


@admin.register(Training)
class TrainingAdmin(ModelAdmin):
    list_display = ("title", "type", "speaker", "start_date", "location", "is_published", "updated_at")
    search_fields = ("title", "summary", "description", "location", "speaker")
    list_filter = ("is_published", "type", "start_date")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "start_date"
    inlines = [TrainingSkillInline, TrainingStepInline]


@admin.register(SpiritualResource)
class SpiritualResourceAdmin(ModelAdmin):
    list_display = ("title", "resource_type", "author", "is_published", "published_at", "updated_at")
    search_fields = ("title", "summary", "content", "author")
    list_filter = ("is_published", "resource_type", "published_at")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"


@admin.register(Event)
class EventAdmin(ModelAdmin):
    list_display = ("title", "category", "start_date", "end_date", "location", "is_published")
    search_fields = ("title", "summary", "location")
    list_filter = ("is_published", "start_date", "category")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "start_date"


@admin.register(Testimonial)
class TestimonialAdmin(ModelAdmin):
    list_display = ("author", "role", "is_published", "updated_at")
    search_fields = ("author", "quote", "role")
    list_filter = ("is_published",)


class GalleryImageInline(TabularInline):
    model = GalleryImage
    extra = 1
    fields = ("title", "image", "image_url", "caption", "order", "is_published")
    ordering = ("order",)


@admin.register(GalleryAlbum)
class GalleryAlbumAdmin(ModelAdmin):
    list_display = ("title", "slug", "is_published", "order", "updated_at")
    search_fields = ("title", "description")
    list_filter = ("is_published",)
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("order", "title")
    inlines = [GalleryImageInline]


@admin.register(GalleryImage)
class GalleryImageAdmin(ModelAdmin):
    list_display = ("title", "album", "order", "is_published", "updated_at")
    search_fields = ("title", "caption")
    list_filter = ("is_published", "album")


@admin.register(ContactMessage)
class ContactMessageAdmin(ModelAdmin):
    list_display = ("full_name", "email", "subject", "is_read", "created_at")
    search_fields = ("full_name", "email", "subject", "message")
    list_filter = ("is_read", "created_at")
    readonly_fields = ("created_at", "updated_at")


class PageSectionTagInline(TabularInline):
    model = PageSectionTag
    extra = 1
    fields = ("label", "order")
    ordering = ("order",)


@admin.register(PageSection)
class PageSectionAdmin(ModelAdmin):
    change_list_template = "admin/app/pagesection/change_list.html"
    list_display = ("title", "page_key", "order", "is_published", "updated_at")
    search_fields = ("title", "subtitle", "body")
    list_filter = ("page_key", "is_published")
    ordering = ("page_key", "order", "title")
    inlines = [PageSectionTagInline]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("reorder/", self.admin_site.admin_view(self.reorder_view), name="app_pagesection_reorder"),
        ]
        return custom_urls + urls

    def changelist_view(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}

        queryset = self.get_queryset(request)
        grouped_sections = {}
        for section in queryset:
            grouped_sections.setdefault(section.page_key, []).append(section)

        extra_context["grouped_sections"] = grouped_sections
        extra_context["page_key_labels"] = dict(PageSection.PAGE_CHOICES)
        return super().changelist_view(request, extra_context=extra_context)

    def reorder_view(self, request):
        if request.method != "POST":
            return JsonResponse({"success": False, "error": "Method not allowed"}, status=405)

        page_key = request.POST.get("page_key", "").strip()
        ids_raw = request.POST.get("ids", "")
        ids = [item for item in ids_raw.split(",") if item]

        if not page_key or not ids:
            return JsonResponse({"success": False, "error": "Payload invalide"}, status=400)

        sections = list(PageSection.objects.filter(page_key=page_key).order_by("order", "title"))
        section_map = {section.pk: section for section in sections}

        for index, section_id in enumerate(ids):
            section_id = int(section_id)
            section = section_map.get(section_id)
            if section is not None:
                section.order = index
                section.save(update_fields=["order"])

        return JsonResponse({"success": True})


@admin.register(TeamMember)
class TeamMemberAdmin(ModelAdmin):
    list_display = ("full_name", "role_title", "category", "is_published", "order")
    search_fields = ("full_name", "role_title", "bio")
    list_filter = ("category", "is_published")
    ordering = ("order", "full_name")


class ScheduleSlotInline(TabularInline):
    model = ScheduleSlot
    extra = 1
    fields = ("day_label", "time_label", "order")
    ordering = ("order",)


@admin.register(Schedule)
class ScheduleAdmin(ModelAdmin):
    list_display = ("title", "key", "order")
    search_fields = ("title", "key")
    ordering = ("order", "title")
    inlines = [ScheduleSlotInline]


class ServiceOfferingItemInline(TabularInline):
    model = ServiceOfferingItem
    extra = 1
    fields = ("text", "order")
    ordering = ("order",)


@admin.register(ServiceOffering)
class ServiceOfferingAdmin(ModelAdmin):
    list_display = ("title", "icon", "is_published", "order")
    search_fields = ("title", "description")
    list_filter = ("is_published",)
    ordering = ("order", "title")
    inlines = [ServiceOfferingItemInline]


@admin.register(RecurringActivity)
class RecurringActivityAdmin(ModelAdmin):
    list_display = ("title", "schedule_label", "location", "is_published", "order")
    search_fields = ("title", "description", "location")
    list_filter = ("is_published",)
    ordering = ("order", "title")


class LiturgicalSeasonItemInline(TabularInline):
    model = LiturgicalSeasonItem
    extra = 1
    fields = ("text", "order")
    ordering = ("order",)


@admin.register(LiturgicalSeason)
class LiturgicalSeasonAdmin(ModelAdmin):
    list_display = ("title", "period_label", "is_published", "order")
    search_fields = ("title", "description")
    list_filter = ("is_published",)
    ordering = ("order", "title")
    inlines = [LiturgicalSeasonItemInline]


class MeditationMethodStepInline(TabularInline):
    model = MeditationMethodStep
    extra = 1
    fields = ("text", "order")
    ordering = ("order",)


@admin.register(MeditationMethod)
class MeditationMethodAdmin(ModelAdmin):
    list_display = ("title", "category", "duration_label", "is_published", "order")
    search_fields = ("title", "description")
    list_filter = ("category", "is_published")
    ordering = ("category", "order", "title")
    inlines = [MeditationMethodStepInline]


@admin.register(BibleVerse)
class BibleVerseAdmin(ModelAdmin):
    list_display = ("reference", "verse_type", "title", "is_published", "order")
    search_fields = ("reference", "title", "quote")
    list_filter = ("verse_type", "is_published")
    ordering = ("verse_type", "order", "reference")


class BibleQuestionTagInline(TabularInline):
    model = BibleQuestionTag
    extra = 1
    fields = ("label", "order")
    ordering = ("order",)


@admin.register(BibleQuestion)
class BibleQuestionAdmin(ModelAdmin):
    list_display = ("question", "category", "respondent", "is_published", "created_at")
    search_fields = ("question", "answer", "questioner_name")
    list_filter = ("category", "is_published", "respondent")
    ordering = ("-created_at",)
    inlines = [BibleQuestionTagInline]


@admin.register(ExternalLink)
class ExternalLinkAdmin(ModelAdmin):
    list_display = ("title", "url", "is_published", "order")
    search_fields = ("title", "description", "url")
    list_filter = ("is_published",)
    ordering = ("order", "title")


@admin.register(ContactChannel)
class ContactChannelAdmin(ModelAdmin):
    list_display = ("title", "section_key", "email", "phone", "is_published", "order")
    search_fields = ("title", "description", "section_key", "email")
    list_filter = ("section_key", "is_published")
    ordering = ("section_key", "order", "title")


@admin.register(AccessInstruction)
class AccessInstructionAdmin(ModelAdmin):
    list_display = ("label", "icon", "is_published", "order")
    search_fields = ("label", "text")
    list_filter = ("is_published",)
    ordering = ("order", "label")
