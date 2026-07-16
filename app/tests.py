from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from app.models import (
    Article,
    BibleQuestion,
    BibleQuestionTag,
    Category,
    ContactChannel,
    ContactMessage,
    Event,
    Father,
    HeroSlide,
    Homily,
    PageSection,
    PageSectionTag,
    Schedule,
    ScheduleSlot,
    ServiceOffering,
    ServiceOfferingItem,
    SiteSettings,
    SpiritualResource,
    TeamMember,
    Training,
    TrainingStep,
)


class ContentModelTests(TestCase):
    def test_hero_slide_slug_is_generated_from_title(self):
        slide = HeroSlide.objects.create(title="Accueil pastoral", subtitle="Bienvenue")

        self.assertEqual(slide.slug, "accueil-pastoral")

    def test_event_end_date_must_not_be_before_start_date(self):
        event = Event(
            title="Veillée",
            summary="Résumé",
            start_date="2026-07-10T18:00:00Z",
            end_date="2026-07-09T18:00:00Z",
        )

        with self.assertRaises(ValidationError):
            event.full_clean()

    def test_article_slug_is_generated_from_title(self):
        article = Article.objects.create(title="Méditation du jour", content="Contenu")

        self.assertEqual(article.slug, "meditation-du-jour")

    def test_site_settings_enforce_single_active_instance(self):
        SiteSettings.objects.create(site_name="Pastoral CHU", is_active=True)
        second = SiteSettings(site_name="Second", is_active=True)

        with self.assertRaises(ValidationError):
            second.full_clean()

    def test_article_detail_page_is_available(self):
        article = Article.objects.create(title="Méditation du jour", content="Contenu", slug="meditation-du-jour")

        response = self.client.get(reverse("article_detail", args=[article.slug]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, article.title)

    def test_contact_form_saves_message(self):
        response = self.client.post(
            reverse("contact"),
            {
                "full_name": "Jean Dupont",
                "email": "jean@example.com",
                "phone": "0123456789",
                "subject": "Question",
                "message": "Bonjour, j'aimerais en savoir plus.",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(ContactMessage.objects.count(), 1)
        self.assertEqual(ContactMessage.objects.first().full_name, "Jean Dupont")

    def test_article_can_belong_to_category(self):
        category = Category.objects.create(name="Spiritualité", slug="spiritualite")
        article = Article.objects.create(title="Méditation", content="Contenu", category=category)

        self.assertEqual(article.category, category)

    def test_image_upload_field_stores_file(self):
        from django.core.files.uploadedfile import SimpleUploadedFile

        image = SimpleUploadedFile("test.png", b"fake-image-content", content_type="image/png")
        event = Event.objects.create(
            title="Formation",
            summary="Résumé",
            start_date="2026-07-10T18:00:00Z",
            end_date="2026-07-10T19:00:00Z",
            image=image,
        )

        self.assertTrue(event.image.name.startswith("uploads/"))

    def test_home_page_displays_admin_sections(self):
        PageSection.objects.create(
            page_key="home",
            title="Section depuis l’admin",
            subtitle="Sous-titre",
            body="Contenu administrable",
            order=1,
            is_published=True,
        )

        response = self.client.get(reverse("index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Section depuis l’admin")
        self.assertContains(response, "Contenu administrable")

    def test_admin_can_reorder_page_sections(self):
        user = get_user_model().objects.create_superuser("admin", "admin@example.com", "password")
        first = PageSection.objects.create(page_key="home", title="Première section", order=0, is_published=True)
        second = PageSection.objects.create(page_key="home", title="Deuxième section", order=1, is_published=True)

        self.client.force_login(user)
        response = self.client.post(
            reverse("admin:app_pagesection_reorder"),
            {"page_key": "home", "ids": f"{second.pk},{first.pk}"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(PageSection.objects.filter(page_key="home").order_by("order", "title").values_list("pk", flat=True)),
            [second.pk, first.pk],
        )

    def test_service_gallery_and_bible_pages_render(self):
        urls = [
            reverse("services"),
            reverse("evenements"),
            reverse("formations"),
            reverse("ressources"),
            reverse("galerie"),
            reverse("bible"),
            reverse("bible_mediter"),
            reverse("bible_reponses"),
        ]

        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, msg=f"La page {url} ne rend pas correctement")

    def test_events_public_page_shows_dashboard_events(self):
        event = Event.objects.create(
            title="Veillée de prière",
            slug="veillée-de-prière",
            summary="Un temps de prière",
            description="Description complète",
            start_date="2026-07-20T18:00:00Z",
            end_date="2026-07-20T20:00:00Z",
            location="Chapelle",
            is_published=True,
        )

        response = self.client.get(reverse("evenements"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, event.title)
        self.assertContains(response, reverse("event_detail", args=[event.slug]))

    def test_training_can_have_steps_and_types(self):
        training = Training.objects.create(
            title="Séminaire de formation",
            slug="seminaire-de-formation",
            type="seminaire",
            summary="Résumé",
            description="Description",
            is_published=True,
        )
        TrainingStep.objects.create(training=training, title="Étape 1", description="Présentation", order=1)
        TrainingStep.objects.create(training=training, title="Étape 2", description="Pratique", order=2)

        self.assertEqual(training.type, "seminaire")
        self.assertEqual(training.steps.count(), 2)

    def test_formations_page_shows_public_training_cards(self):
        Training.objects.create(
            title="Conférence de sensibilisation",
            slug="conference-de-sensibilisation",
            type="conference",
            summary="Résumé",
            description="Description",
            is_published=True,
        )

        response = self.client.get(reverse("formations"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Conférence de sensibilisation")

    def test_spiritual_resources_page_shows_public_cards(self):
        resource = SpiritualResource.objects.create(
            title="Méditation du jeudi",
            slug="meditation-du-jeudi",
            summary="Résumé",
            content="Contenu détaillé",
            resource_type="meditation",
            is_published=True,
        )

        response = self.client.get(reverse("ressources"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, resource.title)
        self.assertContains(response, reverse("spiritual_resource_detail", args=[resource.slug]))

    def test_father_profile_enables_admin_access(self):
        user = get_user_model().objects.create_user(username="perejean", email="pere@example.com", password="password")

        father = Father.objects.create(user=user, full_name="Père Jean", title="Prêtre")

        user.refresh_from_db()
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_active)
        self.assertEqual(father.full_name, "Père Jean")

    def test_homily_can_be_linked_to_a_father_with_media(self):
        user = get_user_model().objects.create_user(username="perepaul", email="paul@example.com", password="password")
        father = Father.objects.create(user=user, full_name="Père Paul", title="Prêtre")

        homily = Homily.objects.create(
            title="Homélie du dimanche",
            gospel="Jean 1, 1-14",
            genre="homelie",
            content="Texte de l’homélie",
            audio_url="https://example.com/audio.mp3",
            father=father,
            is_published=True,
        )

        self.assertEqual(homily.slug, "homelie-du-dimanche")
        self.assertEqual(homily.father, father)
        self.assertEqual(homily.genre, "homelie")

    def test_schedule_slots_are_ordered_under_their_schedule(self):
        schedule = Schedule.objects.create(key="chapel_hours", title="Horaires d'ouverture")
        ScheduleSlot.objects.create(schedule=schedule, day_label="Samedi", time_label="8h-12h", order=1)
        ScheduleSlot.objects.create(schedule=schedule, day_label="Lundi - Vendredi", time_label="8h-18h", order=0)

        self.assertEqual(
            list(schedule.slots.values_list("day_label", flat=True)),
            ["Lundi - Vendredi", "Samedi"],
        )

    def test_service_offering_items_are_linked_to_their_service(self):
        service = ServiceOffering.objects.create(title="Sacrements", description="Description", is_published=True)
        ServiceOfferingItem.objects.create(service=service, text="Eucharistie", order=0)
        ServiceOfferingItem.objects.create(service=service, text="Confession", order=1)

        self.assertEqual(service.items.count(), 2)

    def test_services_page_shows_service_offerings_from_admin(self):
        service = ServiceOffering.objects.create(title="Accompagnement spirituel", description="Écoute et présence", is_published=True)
        ServiceOfferingItem.objects.create(service=service, text="Visites aux patients", order=0)

        response = self.client.get(reverse("services"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Accompagnement spirituel")
        self.assertContains(response, "Visites aux patients")

    def test_team_member_appears_on_about_and_contact_pages(self):
        TeamMember.objects.create(full_name="Sœur Marie-Claire", role_title="Accompagnement", category="sister", is_published=True)

        about_response = self.client.get(reverse("qui-sommes-nous"))
        contact_response = self.client.get(reverse("contact"))

        self.assertContains(about_response, "Sœur Marie-Claire")
        self.assertContains(contact_response, "Sœur Marie-Claire")

    def test_bible_question_tags_and_category_counts_are_computed_not_stored(self):
        question = BibleQuestion.objects.create(
            question="Pourquoi la souffrance ?",
            answer="Réponse détaillée.",
            category="souffrance",
            is_published=True,
        )
        BibleQuestionTag.objects.create(question=question, label="1 Jean 4,8", order=0)

        response = self.client.get(reverse("bible_reponses"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pourquoi la souffrance ?")
        self.assertContains(response, "1 Jean 4,8")
        self.assertContains(response, "1 question")

    def test_contact_channel_is_scoped_by_section_key(self):
        ContactChannel.objects.create(section_key="services_urgence", title="Urgences", phone="0123456789", is_published=True)
        ContactChannel.objects.create(section_key="formations_renseignements", title="Renseignements", email="formations@chu.exemple", is_published=True)

        response = self.client.get(reverse("services"))

        self.assertContains(response, "Urgences")
        self.assertNotContains(response, "formations@chu.exemple")

    def test_page_section_tags_render_on_the_page(self):
        section = PageSection.objects.create(page_key="home", title="Message de la Pastorale", order=0, is_published=True)
        PageSectionTag.objects.create(section=section, label="Solidarité", order=0)

        response = self.client.get(reverse("index"))

        self.assertContains(response, "Solidarité")

    def test_training_supports_speaker_and_information_session_type(self):
        training = Training.objects.create(
            title="Session d'information",
            type="session_info",
            speaker="Père Emmanuel",
            summary="Présentation générale",
            is_published=True,
        )

        self.assertEqual(training.get_type_display(), "Session d'information")
        self.assertEqual(training.speaker, "Père Emmanuel")
