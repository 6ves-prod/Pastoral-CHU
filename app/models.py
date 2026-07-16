from django.contrib.auth import get_user_model
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify


class SiteSettings(models.Model):
    site_name = models.CharField(max_length=150, verbose_name="Nom du site")
    tagline = models.TextField(blank=True, verbose_name="Slogan")
    contact_email = models.EmailField(blank=True, verbose_name="Email de contact")
    phone = models.CharField(max_length=50, blank=True, verbose_name="Téléphone")
    address = models.TextField(blank=True, verbose_name="Adresse")
    is_active = models.BooleanField(default=True, verbose_name="Site actif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    emergency_phone = models.CharField(max_length=50, blank=True, verbose_name="Téléphone d'urgence")
    emergency_note = models.TextField(blank=True, verbose_name="Note d'urgence")

    class Meta:
        verbose_name = "Paramètre du site"
        verbose_name_plural = "Paramètres du site"
        constraints = [
            models.UniqueConstraint(fields=["is_active"], condition=models.Q(is_active=True), name="unique_active_site_settings")
        ]

    def clean(self):
        super().clean()
        if self.is_active and SiteSettings.objects.filter(is_active=True).exclude(pk=self.pk).exists():
            raise ValidationError({"is_active": "Un seul réglage actif peut exister à la fois."})

    def __str__(self):
        return self.site_name or "Paramètres du site"


class HeroSlide(models.Model):
    title = models.CharField(max_length=150, verbose_name="Titre")
    subtitle = models.CharField(max_length=250, blank=True, verbose_name="Sous-titre")
    image_url = models.URLField(blank=True, verbose_name="Image URL")
    image = models.ImageField(upload_to="uploads/hero_slides/", blank=True, null=True, verbose_name="Image")
    slug = models.SlugField(unique=True, blank=True, verbose_name="Slug")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "title"]
        verbose_name = "Slide d’accueil"
        verbose_name_plural = "Slides d’accueil"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom")
    slug = models.SlugField(unique=True, verbose_name="Slug")
    description = models.TextField(blank=True, verbose_name="Description")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Father(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name="father_profile", verbose_name="Compte utilisateur")
    full_name = models.CharField(max_length=150, verbose_name="Nom complet")
    title = models.CharField(max_length=150, blank=True, verbose_name="Titre / fonction")
    bio = models.TextField(blank=True, verbose_name="Biographie")
    image = models.ImageField(upload_to="uploads/fathers/", blank=True, null=True, verbose_name="Photo")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Père"
        verbose_name_plural = "Pères"
        ordering = ["full_name"]

    def save(self, *args, **kwargs):
        if self.user and not self.user.is_staff:
            self.user.is_staff = True
            self.user.is_active = True
            self.user.save(update_fields=["is_staff", "is_active"])
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name or self.user.username


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name="Titre")
    slug = models.SlugField(unique=True, blank=True, verbose_name="Slug")
    content = models.TextField(verbose_name="Contenu")
    excerpt = models.TextField(blank=True, verbose_name="Résumé")
    image_url = models.URLField(blank=True, verbose_name="Image URL")
    image = models.ImageField(upload_to="uploads/articles/", blank=True, null=True, verbose_name="Image")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="articles", verbose_name="Catégorie")
    is_published = models.BooleanField(default=True, verbose_name="Publié")
    published_at = models.DateTimeField(blank=True, null=True, verbose_name="Date de publication")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at", "-created_at"]
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Homily(models.Model):
    GENRE_CHOICES = [
        ("homelie", "Homélie"),
        ("meditation", "Méditation"),
        ("conference", "Conférence"),
    ]

    title = models.CharField(max_length=200, verbose_name="Titre")
    slug = models.SlugField(unique=True, blank=True, verbose_name="Slug")
    gospel = models.CharField(max_length=200, blank=True, verbose_name="Évangile")
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES, default="homelie", verbose_name="Genre")
    content = models.TextField(blank=True, verbose_name="Texte")
    audio_url = models.URLField(blank=True, verbose_name="Audio URL")
    audio_file = models.FileField(upload_to="uploads/homilies/audio/", blank=True, null=True, verbose_name="Fichier audio")
    duration_label = models.CharField(max_length=50, blank=True, verbose_name="Durée")
    pdf_file = models.FileField(upload_to="uploads/homilies/pdf/", blank=True, null=True, verbose_name="PDF")
    father = models.ForeignKey(Father, on_delete=models.SET_NULL, null=True, blank=True, related_name="homilies", verbose_name="Père")
    is_published = models.BooleanField(default=True, verbose_name="Publié")
    published_at = models.DateTimeField(blank=True, null=True, verbose_name="Date de publication")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at", "-created_at"]
        verbose_name = "Homélie"
        verbose_name_plural = "Homélies"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.slug or self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Training(models.Model):
    TYPE_CHOICES = [
        ("conference", "Conférence"),
        ("seminaire", "Séminaire"),
        ("atelier", "Atelier"),
        ("formation", "Formation"),
        ("session_info", "Session d'information"),
        ("autre", "Autre"),
    ]

    title = models.CharField(max_length=200, verbose_name="Titre")
    slug = models.SlugField(unique=True, blank=True, verbose_name="Slug")
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default="formation", verbose_name="Type")
    summary = models.TextField(verbose_name="Résumé")
    description = models.TextField(blank=True, verbose_name="Description")
    speaker = models.CharField(max_length=150, blank=True, verbose_name="Intervenant")
    location = models.CharField(max_length=200, blank=True, verbose_name="Lieu")
    start_date = models.DateField(blank=True, null=True, verbose_name="Date de début")
    duration = models.CharField(max_length=100, blank=True, verbose_name="Durée")
    capacity = models.CharField(max_length=100, blank=True, verbose_name="Capacité / public")
    image_url = models.URLField(blank=True, verbose_name="Image URL")
    image = models.ImageField(upload_to="uploads/trainings/", blank=True, null=True, verbose_name="Image")
    is_published = models.BooleanField(default=True, verbose_name="Publié")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["start_date", "title"]
        verbose_name = "Formation"
        verbose_name_plural = "Formations"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.slug or self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class TrainingStep(models.Model):
    training = models.ForeignKey(Training, on_delete=models.CASCADE, related_name="steps", verbose_name="Formation")
    title = models.CharField(max_length=200, verbose_name="Titre de l’étape")
    description = models.TextField(blank=True, verbose_name="Description")
    duration_label = models.CharField(max_length=100, blank=True, verbose_name="Durée / détail")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "title"]
        verbose_name = "Étape de formation"
        verbose_name_plural = "Étapes de formation"

    def __str__(self):
        return f"{self.training.title} - {self.title}"


class TrainingSkill(models.Model):
    training = models.ForeignKey(Training, on_delete=models.CASCADE, related_name="skills", verbose_name="Formation")
    text = models.CharField(max_length=200, verbose_name="Compétence acquise")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre")

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Compétence de formation"
        verbose_name_plural = "Compétences de formation"

    def __str__(self):
        return f"{self.training.title} - {self.text}"


class SpiritualResource(models.Model):
    RESOURCE_TYPE_CHOICES = [
        ("meditation", "Méditation"),
        ("reflection", "Réflexion"),
        ("prayer", "Prière"),
        ("guide", "Guide"),
        ("other", "Autre"),
    ]

    title = models.CharField(max_length=200, verbose_name="Titre")
    slug = models.SlugField(unique=True, blank=True, verbose_name="Slug")
    resource_type = models.CharField(max_length=50, choices=RESOURCE_TYPE_CHOICES, default="meditation", verbose_name="Type")
    summary = models.TextField(verbose_name="Résumé")
    content = models.TextField(blank=True, verbose_name="Contenu")
    author = models.CharField(max_length=150, blank=True, verbose_name="Auteur")
    audio_url = models.URLField(blank=True, verbose_name="Audio URL")
    pdf_file = models.FileField(upload_to="uploads/resources/pdf/", blank=True, null=True, verbose_name="PDF")
    file_size_label = models.CharField(max_length=50, blank=True, verbose_name="Taille du fichier")
    external_url = models.URLField(blank=True, verbose_name="Lien externe (app, site...)")
    image_url = models.URLField(blank=True, verbose_name="Image URL")
    image = models.ImageField(upload_to="uploads/resources/", blank=True, null=True, verbose_name="Image")
    is_published = models.BooleanField(default=True, verbose_name="Publié")
    published_at = models.DateTimeField(blank=True, null=True, verbose_name="Date de publication")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at", "-created_at"]
        verbose_name = "Ressource spirituelle"
        verbose_name_plural = "Ressources spirituelles"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.slug or self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Event(models.Model):
    title = models.CharField(max_length=200, verbose_name="Titre")
    slug = models.SlugField(unique=True, blank=True, verbose_name="Slug")
    summary = models.TextField(verbose_name="Résumé")
    description = models.TextField(blank=True, verbose_name="Description")
    start_date = models.DateTimeField(verbose_name="Date de début")
    end_date = models.DateTimeField(verbose_name="Date de fin")
    location = models.CharField(max_length=200, blank=True, verbose_name="Lieu")
    image_url = models.URLField(blank=True, verbose_name="Image URL")
    image = models.ImageField(upload_to="uploads/events/", blank=True, null=True, verbose_name="Image")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="events", verbose_name="Catégorie")
    is_published = models.BooleanField(default=True, verbose_name="Publié")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["start_date"]
        verbose_name = "Événement"
        verbose_name_plural = "Événements"

    def clean(self):
        super().clean()
        if self.end_date and self.start_date and self.end_date < self.start_date:
            raise ValidationError({"end_date": "La date de fin ne peut pas être antérieure à la date de début."})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.slug or self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    author = models.CharField(max_length=150, verbose_name="Auteur")
    role = models.CharField(max_length=150, blank=True, verbose_name="Fonction")
    quote = models.TextField(verbose_name="Témoignage")
    is_published = models.BooleanField(default=True, verbose_name="Publié")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["author"]
        verbose_name = "Témoignage"
        verbose_name_plural = "Témoignages"

    def __str__(self):
        return self.author


class GalleryAlbum(models.Model):
    title = models.CharField(max_length=150, verbose_name="Titre")
    slug = models.SlugField(unique=True, blank=True, verbose_name="Slug")
    description = models.TextField(blank=True, verbose_name="Description")
    cover_image_url = models.URLField(blank=True, verbose_name="Image de couverture URL")
    cover_image = models.ImageField(upload_to="uploads/gallery_albums/", blank=True, null=True, verbose_name="Image de couverture")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre")
    is_published = models.BooleanField(default=True, verbose_name="Publié")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "title"]
        verbose_name = "Album photo"
        verbose_name_plural = "Albums photo"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def cover(self):
        if self.cover_image:
            return self.cover_image.url
        if self.cover_image_url:
            return self.cover_image_url
        first_image = self.images.filter(is_published=True).first()
        return first_image.image.url if first_image and first_image.image else first_image.image_url if first_image else ""

    def __str__(self):
        return self.title


class GalleryImage(models.Model):
    album = models.ForeignKey(GalleryAlbum, on_delete=models.CASCADE, null=True, blank=True, related_name="images", verbose_name="Album")
    title = models.CharField(max_length=150, verbose_name="Titre")
    image_url = models.URLField(blank=True, verbose_name="Image URL")
    image = models.ImageField(upload_to="uploads/gallery_images/", blank=True, null=True, verbose_name="Image")
    caption = models.TextField(blank=True, verbose_name="Légende")
    is_published = models.BooleanField(default=True, verbose_name="Publié")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "title"]
        verbose_name = "Image de galerie"
        verbose_name_plural = "Images de galerie"

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    full_name = models.CharField(max_length=150, verbose_name="Nom complet")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=50, blank=True, verbose_name="Téléphone")
    subject = models.CharField(max_length=200, verbose_name="Sujet")
    message = models.TextField(verbose_name="Message")
    is_read = models.BooleanField(default=False, verbose_name="Lu")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Message de contact"
        verbose_name_plural = "Messages de contact"

    def __str__(self):
        return f"{self.full_name} - {self.subject}"


class PageSection(models.Model):
    PAGE_CHOICES = [
        ("home", "Accueil"),
        ("about", "À propos"),
        ("gallery", "Galerie"),
        ("contact", "Contact"),
        ("formations", "Formations"),
    ]

    page_key = models.CharField(max_length=50, choices=PAGE_CHOICES, verbose_name="Page")
    title = models.CharField(max_length=200, verbose_name="Titre")
    subtitle = models.CharField(max_length=250, blank=True, verbose_name="Sous-titre")
    body = models.TextField(blank=True, verbose_name="Contenu")
    image_url = models.URLField(blank=True, verbose_name="Image URL")
    image = models.ImageField(upload_to="uploads/page_sections/", blank=True, null=True, verbose_name="Image")
    button_text = models.CharField(max_length=100, blank=True, verbose_name="Texte du bouton")
    button_url = models.CharField(max_length=250, blank=True, verbose_name="Lien du bouton")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre")
    is_published = models.BooleanField(default=True, verbose_name="Publié")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "title"]
        verbose_name = "Section de page"
        verbose_name_plural = "Sections de page"

    def __str__(self):
        return f"{self.get_page_key_display()} - {self.title}"


class PageSectionTag(models.Model):
    section = models.ForeignKey(PageSection, on_delete=models.CASCADE, related_name="tags", verbose_name="Section")
    label = models.CharField(max_length=100, verbose_name="Libellé")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre")

    class Meta:
        ordering = ["order", "label"]
        verbose_name = "Pastille de section"
        verbose_name_plural = "Pastilles de section"

    def __str__(self):
        return self.label


class TeamMember(models.Model):
    CATEGORY_CHOICES = [
        ("father", "Père"),
        ("sister", "Sœur"),
        ("staff", "Employé"),
        ("volunteer", "Bénévole"),
    ]

    full_name = models.CharField(max_length=150, verbose_name="Nom complet")
    role_title = models.CharField(max_length=150, blank=True, verbose_name="Fonction")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="staff", verbose_name="Catégorie")
    email = models.EmailField(blank=True, verbose_name="Email")
    phone = models.CharField(max_length=50, blank=True, verbose_name="Téléphone")
    photo = models.ImageField(upload_to="uploads/team/", blank=True, null=True, verbose_name="Photo")
    bio = models.TextField(blank=True, verbose_name="Biographie")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre")
    is_published = models.BooleanField(default=True, verbose_name="Publié")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "full_name"]
        verbose_name = "Membre de l'équipe"
        verbose_name_plural = "Membres de l'équipe"

    def __str__(self):
        return self.full_name


class Schedule(models.Model):
    key = models.SlugField(unique=True, verbose_name="Clé")
    title = models.CharField(max_length=150, verbose_name="Titre")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre")

    class Meta:
        ordering = ["order", "title"]
        verbose_name = "Horaire"
        verbose_name_plural = "Horaires"

    def __str__(self):
        return self.title


class ScheduleSlot(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name="slots", verbose_name="Horaire")
    day_label = models.CharField(max_length=100, verbose_name="Jour(s)")
    time_label = models.CharField(max_length=100, verbose_name="Plage horaire")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre")

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Créneau"
        verbose_name_plural = "Créneaux"

    def __str__(self):
        return f"{self.schedule.title} - {self.day_label}"


class ServiceOffering(models.Model):
    icon = models.CharField(max_length=10, blank=True, verbose_name="Icône (emoji)")
    title = models.CharField(max_length=150, verbose_name="Titre")
    description = models.TextField(blank=True, verbose_name="Description")
    link_text = models.CharField(max_length=100, blank=True, verbose_name="Texte du lien")
    link_url = models.CharField(max_length=250, blank=True, verbose_name="Lien")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre")
    is_published = models.BooleanField(default=True, verbose_name="Publié")

    class Meta:
        ordering = ["order", "title"]
        verbose_name = "Service proposé"
        verbose_name_plural = "Services proposés"

    def __str__(self):
        return self.title


class ServiceOfferingItem(models.Model):
    service = models.ForeignKey(ServiceOffering, on_delete=models.CASCADE, related_name="items", verbose_name="Service")
    text = models.CharField(max_length=200, verbose_name="Texte")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre")

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Détail de service"
        verbose_name_plural = "Détails de service"

    def __str__(self):
        return self.text


class RecurringActivity(models.Model):
    icon = models.CharField(max_length=10, blank=True, verbose_name="Icône (emoji)")
    title = models.CharField(max_length=150, verbose_name="Titre")
    schedule_label = models.CharField(max_length=150, blank=True, verbose_name="Horaire")
    location = models.CharField(max_length=150, blank=True, verbose_name="Lieu")
    description = models.TextField(blank=True, verbose_name="Description")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre")
    is_published = models.BooleanField(default=True, verbose_name="Publié")

    class Meta:
        ordering = ["order", "title"]
        verbose_name = "Activité régulière"
        verbose_name_plural = "Activités régulières"

    def __str__(self):
        return self.title


class LiturgicalSeason(models.Model):
    title = models.CharField(max_length=150, verbose_name="Titre")
    period_label = models.CharField(max_length=150, blank=True, verbose_name="Période")
    description = models.TextField(blank=True, verbose_name="Description")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre")
    is_published = models.BooleanField(default=True, verbose_name="Publié")

    class Meta:
        ordering = ["order", "title"]
        verbose_name = "Temps liturgique fort"
        verbose_name_plural = "Temps liturgiques forts"

    def __str__(self):
        return self.title


class LiturgicalSeasonItem(models.Model):
    season = models.ForeignKey(LiturgicalSeason, on_delete=models.CASCADE, related_name="items", verbose_name="Temps liturgique")
    text = models.CharField(max_length=200, verbose_name="Texte")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre")

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Détail de temps liturgique"
        verbose_name_plural = "Détails de temps liturgique"

    def __str__(self):
        return self.text


class MeditationMethod(models.Model):
    CATEGORY_CHOICES = [
        ("method", "Méthode de méditation"),
        ("silence", "Temps de silence"),
    ]

    title = models.CharField(max_length=150, verbose_name="Titre")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="method", verbose_name="Catégorie")
    description = models.TextField(blank=True, verbose_name="Description")
    duration_label = models.CharField(max_length=50, blank=True, verbose_name="Durée")
    tip = models.TextField(blank=True, verbose_name="Conseil (« Pour débuter »)")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre")
    is_published = models.BooleanField(default=True, verbose_name="Publié")

    class Meta:
        ordering = ["category", "order", "title"]
        verbose_name = "Méthode / temps de méditation"
        verbose_name_plural = "Méthodes / temps de méditation"

    def __str__(self):
        return self.title


class MeditationMethodStep(models.Model):
    method = models.ForeignKey(MeditationMethod, on_delete=models.CASCADE, related_name="steps", verbose_name="Méthode")
    text = models.CharField(max_length=200, verbose_name="Texte")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre")

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Étape de méditation"
        verbose_name_plural = "Étapes de méditation"

    def __str__(self):
        return self.text


class BibleVerse(models.Model):
    VERSE_TYPE_CHOICES = [
        ("daily", "Verset du jour"),
        ("psalm", "Psaume"),
    ]

    verse_type = models.CharField(max_length=20, choices=VERSE_TYPE_CHOICES, default="daily", verbose_name="Type")
    reference = models.CharField(max_length=100, verbose_name="Référence")
    title = models.CharField(max_length=150, blank=True, verbose_name="Titre")
    context = models.TextField(blank=True, verbose_name="Contexte")
    quote = models.TextField(verbose_name="Texte")
    tag_label = models.CharField(max_length=100, blank=True, verbose_name="Étiquette")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre")
    is_published = models.BooleanField(default=True, verbose_name="Publié")

    class Meta:
        ordering = ["verse_type", "order", "reference"]
        verbose_name = "Verset biblique"
        verbose_name_plural = "Versets bibliques"

    def __str__(self):
        return f"{self.get_verse_type_display()} - {self.reference}"


class BibleQuestion(models.Model):
    CATEGORY_CHOICES = [
        ("souffrance", "Souffrance & Providence"),
        ("priere", "Prière & Spiritualité"),
        ("vie_eternelle", "Vie après la mort"),
        ("sacrements", "Sacrements"),
        ("ethique", "Éthique & Morale"),
        ("famille", "Famille & Relations"),
    ]

    question = models.CharField(max_length=250, verbose_name="Question")
    questioner_name = models.CharField(max_length=150, blank=True, verbose_name="Nom du/de la questionneur(se)")
    questioner_context = models.CharField(max_length=200, blank=True, verbose_name="Contexte (service, situation...)")
    respondent = models.ForeignKey(Father, on_delete=models.SET_NULL, null=True, blank=True, related_name="bible_answers", verbose_name="Répondant")
    answer = models.TextField(verbose_name="Réponse")
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default="priere", verbose_name="Catégorie")
    is_published = models.BooleanField(default=True, verbose_name="Publié")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Question biblique"
        verbose_name_plural = "Questions bibliques"

    def __str__(self):
        return self.question


class BibleQuestionTag(models.Model):
    question = models.ForeignKey(BibleQuestion, on_delete=models.CASCADE, related_name="tags", verbose_name="Question")
    label = models.CharField(max_length=100, verbose_name="Référence")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre")

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Référence biblique"
        verbose_name_plural = "Références bibliques"

    def __str__(self):
        return self.label


class ExternalLink(models.Model):
    title = models.CharField(max_length=150, verbose_name="Titre")
    url = models.URLField(verbose_name="Lien")
    description = models.CharField(max_length=250, blank=True, verbose_name="Description")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre")
    is_published = models.BooleanField(default=True, verbose_name="Publié")

    class Meta:
        ordering = ["order", "title"]
        verbose_name = "Lien externe"
        verbose_name_plural = "Liens externes"

    def __str__(self):
        return self.title


class ContactChannel(models.Model):
    section_key = models.CharField(max_length=50, verbose_name="Section", help_text="Identifie le bloc de la page qui affiche cette carte (ex. services_urgence).")
    title = models.CharField(max_length=150, verbose_name="Titre")
    description = models.TextField(blank=True, verbose_name="Description")
    email = models.EmailField(blank=True, verbose_name="Email")
    phone = models.CharField(max_length=50, blank=True, verbose_name="Téléphone")
    extension = models.CharField(max_length=20, blank=True, verbose_name="Poste")
    note = models.CharField(max_length=250, blank=True, verbose_name="Note")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre")
    is_published = models.BooleanField(default=True, verbose_name="Publié")

    class Meta:
        ordering = ["section_key", "order", "title"]
        verbose_name = "Carte de contact"
        verbose_name_plural = "Cartes de contact"

    def __str__(self):
        return f"{self.section_key} - {self.title}"


class AccessInstruction(models.Model):
    icon = models.CharField(max_length=10, blank=True, verbose_name="Icône (emoji)")
    label = models.CharField(max_length=100, verbose_name="Libellé")
    text = models.TextField(verbose_name="Texte")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre")
    is_published = models.BooleanField(default=True, verbose_name="Publié")

    class Meta:
        ordering = ["order", "label"]
        verbose_name = "Instruction d'accès"
        verbose_name_plural = "Instructions d'accès"

    def __str__(self):
        return self.label