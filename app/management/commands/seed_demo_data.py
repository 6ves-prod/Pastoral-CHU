from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils import timezone

from app.models import (
    AccessInstruction,
    Article,
    BibleQuestion,
    BibleQuestionTag,
    BibleVerse,
    Category,
    ContactChannel,
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

FAKE_PDF = b"%PDF-1.4\n% Fichier de demonstration pour les tests.\n"
FAKE_AUDIO = b"ID3 demo audio placeholder for testing."


class Command(BaseCommand):
    help = "Peuple la base avec des donnees credibles pour tester toutes les pages (y compris les pages de detail)."

    def handle(self, *args, **options):
        now = timezone.now()

        self.stdout.write("Paramètres du site…")
        SiteSettings.objects.update_or_create(
            site_name="Pastorale du CHU",
            defaults=dict(
                tagline="Un lieu d'écoute, de prière et de service au cœur du soin.",
                contact_email="pastorale@chu-exemple.fr",
                phone="01 23 45 67 89",
                address="Pastorale du CHU\nChapelle - Bâtiment A, Niveau 0\n123 Avenue de la Santé\n75000 Paris",
                is_active=True,
                emergency_phone="01 23 45 67 90",
                emergency_note="En cas d'urgence pastorale (derniers sacrements, accompagnement urgent), appelez directement le 01 23 45 67 90 ou demandez l'aumônier de garde à l'accueil.",
            ),
        )

        self.stdout.write("Slides d'accueil…")
        for title, subtitle, image, order in [
            ("Accueillir, écouter, accompagner", "Pastorale hospitalière", "https://images.unsplash.com/photo-1517832207067-4c4d58f0cc94?auto=format&fit=crop&w=1400&q=80", 0),
            ("Une présence à vos côtés", "24h/24, 7j/7", "https://images.unsplash.com/photo-1509099836639-18ba02e2e1ba?auto=format&fit=crop&w=1400&q=80", 1),
            ("Célébrer ensemble l'espérance", "Messes et temps de prière", "https://images.unsplash.com/photo-1529156069898-49953e39b3ac?auto=format&fit=crop&w=1400&q=80", 2),
        ]:
            HeroSlide.objects.update_or_create(title=title, defaults=dict(subtitle=subtitle, image_url=image, order=order, is_active=True))

        self.stdout.write("Catégories…")
        cat_spirituelle, _ = Category.objects.update_or_create(slug="vie-spirituelle", defaults=dict(name="Vie spirituelle", description="Prière, sacrements et accompagnement spirituel."))
        cat_solidarite, _ = Category.objects.update_or_create(slug="solidarite", defaults=dict(name="Solidarité", description="Actions caritatives et collectes."))
        cat_formation, _ = Category.objects.update_or_create(slug="formation", defaults=dict(name="Formation", description="Formations et enseignements pastoraux."))

        self.stdout.write("Pères (comptes admin)…")
        User = get_user_model()
        user_jean, _ = User.objects.get_or_create(username="pere.jean", defaults=dict(email="jean.dupont@chu-exemple.fr", first_name="Jean", last_name="Dupont"))
        user_martin, _ = User.objects.get_or_create(username="pere.martin", defaults=dict(email="martin.lefevre@chu-exemple.fr", first_name="Martin", last_name="Lefèvre"))
        father_jean, _ = Father.objects.update_or_create(
            user=user_jean,
            defaults=dict(full_name="Père Jean Dupont", title="Aumônier responsable", bio="Coordination sacramentelle, homélies et direction pastorale depuis douze ans au sein du CHU.", is_active=True),
        )
        father_martin, _ = Father.objects.update_or_create(
            user=user_martin,
            defaults=dict(full_name="Père Martin Lefèvre", title="Aumônier", bio="Visites quotidiennes, confessions et préparation aux sacrements.", is_active=True),
        )

        self.stdout.write("Articles…")
        Article.objects.update_or_create(
            slug="temps-avent-vecu-a-l-hopital",
            defaults=dict(
                title="Un temps de l'Avent vécu à l'hôpital",
                content=(
                    "Le temps de l'Avent invite chacun à se préparer intérieurement à la venue du Christ. "
                    "Dans les couloirs du CHU, cette préparation prend une couleur particulière : elle se vit "
                    "au rythme des soins, des attentes et des espérances de chacun.\n\n"
                    "Cette année encore, la pastorale propose des temps de prière courts chaque matin dans la chapelle, "
                    "ainsi que la distribution de petites bougies aux patients qui le souhaitent. « C'est une manière "
                    "simple de rappeler que la lumière ne s'éteint jamais tout à fait », confie le Père Jean Dupont.\n\n"
                    "Les bénévoles seront également présents dans les services pour proposer un temps d'écoute ou "
                    "simplement une présence silencieuse auprès de ceux qui le désirent."
                ),
                excerpt="La pastorale propose des temps de prière quotidiens et une présence renforcée pendant l'Avent.",
                image_url="https://images.unsplash.com/photo-1512389142860-9c449e58a543?auto=format&fit=crop&w=800&q=80",
                category=cat_spirituelle,
                is_published=True,
                published_at=now - timedelta(days=2),
            ),
        )
        Article.objects.update_or_create(
            slug="grande-collecte-solidaire-fin-annee",
            defaults=dict(
                title="Grande collecte solidaire pour les familles",
                content=(
                    "Chaque année, la pastorale organise une collecte au profit des familles les plus démunies "
                    "accompagnées par le service social du CHU. Vêtements chauds, produits d'hygiène et jouets "
                    "seront récoltés dans le hall principal jusqu'à la fin du mois.\n\n"
                    "L'an dernier, plus de deux cents familles avaient pu bénéficier de cette générosité. "
                    "« Chaque don, même modeste, compte énormément pour les personnes que nous accompagnons », "
                    "rappelle la responsable solidarité de la pastorale.\n\n"
                    "Un point de collecte est également disponible à l'accueil de chaque bâtiment."
                ),
                excerpt="Une collecte de vêtements, produits d'hygiène et jouets est organisée jusqu'à la fin du mois.",
                image_url="https://images.unsplash.com/photo-1593113630400-ea4288922497?auto=format&fit=crop&w=800&q=80",
                category=cat_solidarite,
                is_published=True,
                published_at=now - timedelta(days=6),
            ),
        )
        Article.objects.update_or_create(
            slug="retour-formation-benevoles",
            defaults=dict(
                title="Retour sur la formation des bénévoles",
                content=(
                    "Une nouvelle promotion de bénévoles accompagnants a achevé son parcours de formation initiale. "
                    "Pendant six semaines, ils ont appris l'écoute active, la gestion des situations difficiles "
                    "et la déontologie propre au bénévolat hospitalier.\n\n"
                    "« Cette formation m'a donné les outils pour être présent sans être envahissant, pour "
                    "accueillir la souffrance sans chercher à la résoudre à tout prix », témoigne l'un des "
                    "nouveaux bénévoles à l'issue de la session.\n\n"
                    "Une nouvelle session débutera au premier trimestre pour les personnes intéressées."
                ),
                excerpt="Six semaines de formation à l'écoute et à l'accompagnement pour une nouvelle promotion de bénévoles.",
                image_url="https://images.unsplash.com/photo-1521737711867-e3b97375f902?auto=format&fit=crop&w=800&q=80",
                category=cat_formation,
                is_published=True,
                published_at=now - timedelta(days=10),
            ),
        )

        self.stdout.write("Homélies et méditations…")
        Homily.objects.update_or_create(
            slug="heureux-les-artisans-de-paix",
            defaults=dict(
                title="Heureux les artisans de paix",
                gospel="Matthieu 5, 1-12",
                genre="homelie",
                content=(
                    "« Réjouissez-vous, soyez dans l'allégresse : votre récompense est grande dans les cieux. » "
                    "Ces mots de Jésus résonnent particulièrement dans un lieu de soin, où la fragilité côtoie "
                    "chaque jour l'espérance. Être artisan de paix, ici, c'est parfois simplement s'asseoir "
                    "quelques minutes auprès d'un patient, sans rien dire, sans rien attendre.\n\n"
                    "Que cette Parole nous invite aujourd'hui à semer, à notre échelle, un peu de cette paix "
                    "que le monde ne peut pas donner."
                ),
                father=father_jean,
                duration_label="6 min",
                is_published=True,
                published_at=now,
            ),
        )
        Homily.objects.update_or_create(
            slug="le-verbe-sest-fait-chair",
            defaults=dict(
                title="Le Verbe s'est fait chair",
                gospel="Jean 1, 1-14",
                genre="meditation",
                content=(
                    "Entrer dans la méditation : prendre quelques instants de silence, respirer calmement et "
                    "offrir ce temps à Dieu.\n\n"
                    "Contempler : « Le Verbe s'est fait chair ». Mystère de l'Incarnation, Dieu qui se fait homme "
                    "et prend notre condition humaine avec ses joies et ses souffrances. Dans cette chambre "
                    "d'hôpital, dans cette situation de fragilité, Dieu lui-même s'est rendu vulnérable pour "
                    "être proche de nous.\n\n"
                    "Méditer : « Il a habité parmi nous ». Jésus a planté sa tente au milieu de nos tentes "
                    "humaines. Il partage notre précarité, nos peurs, nos espérances.\n\n"
                    "Prier : Seigneur Jésus, aide-moi à découvrir ta présence dans les moments difficiles que "
                    "je traverse. Amen."
                ),
                father=father_martin,
                is_published=True,
                published_at=now - timedelta(days=1),
            ),
        )
        Homily.objects.update_or_create(
            slug="le-bon-berger",
            defaults=dict(
                title="Le Bon Berger",
                gospel="Jean 10, 11-16",
                genre="meditation",
                content=(
                    "Une méditation sur Jésus Bon Berger, particulièrement adaptée pour les moments d'inquiétude. "
                    "Découvrir la tendresse et la protection de Dieu dans les passages difficiles de la vie, "
                    "et se laisser conduire vers des eaux tranquilles même au cœur de l'épreuve."
                ),
                father=father_jean,
                duration_label="12 min",
                audio_url="https://example.com/audio/bon-berger.mp3",
                is_published=True,
                published_at=now - timedelta(days=4),
            ),
        )
        beatitudes, _ = Homily.objects.update_or_create(
            slug="les-beatitudes",
            defaults=dict(
                title="Les Béatitudes",
                gospel="Matthieu 5, 1-12",
                genre="meditation",
                content=(
                    "Méditation sur les Béatitudes, chemin de bonheur proposé par Jésus. Comment vivre ces "
                    "paroles dans notre quotidien, même dans l'épreuve ? Une invitation à la confiance et à "
                    "l'espérance, portée ici par Sœur Marie-Claire."
                ),
                duration_label="15 min",
                is_published=True,
                published_at=now - timedelta(days=8),
            ),
        )
        if not beatitudes.audio_file:
            beatitudes.audio_file.save("les-beatitudes.mp3", ContentFile(FAKE_AUDIO), save=True)

        self.stdout.write("Formations…")
        volunteer_path, _ = Training.objects.update_or_create(
            slug="parcours-de-formation-des-benevoles",
            defaults=dict(
                title="Parcours de formation des bénévoles",
                type="formation",
                summary="Le parcours complet pour devenir accompagnant bénévole au sein de la pastorale du CHU.",
                description="Quatre étapes progressives, de la découverte à l'engagement, pour accompagner les patients et leurs familles.",
                location="Pastorale du CHU",
                is_published=True,
            ),
        )
        steps = [
            ("Journée de découverte", "Présentation de la mission pastorale, visite des lieux, rencontre avec l'équipe et temps de discernement.", "1 journée"),
            ("Formation initiale", "Écoute, présence, gestion des situations difficiles, déontologie et secret professionnel.", "6 sessions de 2h"),
            ("Accompagnement supervisé", "Intégration progressive avec un bénévole expérimenté, visites en binôme et debriefing régulier.", "3 mois"),
            ("Engagement et formation continue", "Engagement pour une durée minimale, formations complémentaires et retraites spirituelles annuelles.", "2 ans minimum"),
        ]
        for order, (title, description, duration_label) in enumerate(steps):
            TrainingStep.objects.update_or_create(training=volunteer_path, title=title, defaults=dict(description=description, duration_label=duration_label, order=order))

        volunteer_skills = [
            "Écoute active et bienveillante",
            "Gestion des situations émotionnellement difficiles",
            "Repères de déontologie et secret professionnel",
            "Posture d'accompagnement sans jugement",
            "Travail en binôme et transmission d'informations",
            "Reconnaissance des limites de son rôle de bénévole",
        ]
        for order, text in enumerate(volunteer_skills):
            TrainingSkill.objects.update_or_create(training=volunteer_path, text=text, defaults=dict(order=order))

        Training.objects.update_or_create(
            slug="conference-spiritualite-et-medecine-moderne",
            defaults=dict(
                title="Spiritualité et médecine moderne",
                type="conference",
                speaker="Dr Sophie Meunier & Père Jean Dupont",
                summary="Conférence-débat sur l'articulation entre science médicale et dimension spirituelle du soin.",
                description="Une soirée d'échange ouverte à tous, professionnels de santé, patients, familles et bénévoles, autour de la place du spirituel dans le parcours de soin.",
                location="Amphithéâtre du CHU",
                start_date=(now + timedelta(days=14)).date(),
                capacity="Ouvert au public, entrée libre",
                is_published=True,
            ),
        )
        Training.objects.update_or_create(
            slug="seminaire-accompagner-familles-en-deuil",
            defaults=dict(
                title="Accompagner les familles en deuil",
                type="seminaire",
                speaker="Père Martin Lefèvre",
                summary="Séminaire de formation pour les professionnels et bénévoles sur l'accompagnement du deuil.",
                description="Apports théoriques et mises en situation pour mieux accompagner les familles endeuillées, en lien avec l'équipe de psychologie du CHU.",
                location="Salle de formation, Bâtiment A",
                start_date=(now + timedelta(days=28)).date(),
                capacity="Professionnels et bénévoles, sur inscription",
                is_published=True,
            ),
        )
        Training.objects.update_or_create(
            slug="session-information-benevolat",
            defaults=dict(
                title="Session d'information bénévolat",
                type="session_info",
                summary="Présentation générale de l'engagement bénévole à la pastorale du CHU.",
                description="Une rencontre sans engagement pour découvrir les différentes formes de bénévolat possibles.",
                location="Bureau pastoral, Bâtiment A",
                start_date=(now + timedelta(days=5)).date(),
                is_published=True,
            ),
        )
        evangile_marc, _ = Training.objects.update_or_create(
            slug="evangile-selon-marc",
            defaults=dict(
                title="L'Évangile selon Marc",
                type="formation",
                summary="Six rencontres mensuelles pour une lecture continue et un partage en petits groupes.",
                description="Un parcours de lecture suivie de l'Évangile de Marc, accessible à tous, croyants ou en recherche.",
                duration="6 rencontres mensuelles",
                capacity="6 séances · groupe limité",
                is_published=True,
            ),
        )
        for order, text in enumerate(["Repères de lecture exégétique", "Contextualisation historique et culturelle", "Partage et prise de parole en petit groupe"]):
            TrainingSkill.objects.update_or_create(training=evangile_marc, text=text, defaults=dict(order=order))

        psaumes, _ = Training.objects.update_or_create(
            slug="psaumes-de-consolation",
            defaults=dict(
                title="Psaumes de consolation",
                type="atelier",
                summary="Découvrir les psaumes pour prier dans l'épreuve et accompagner ceux qui souffrent.",
                description="Un atelier pratique pour apprendre à prier les psaumes, seul ou en accompagnement d'un proche malade.",
                duration="3h d'atelier",
                capacity="Tous publics",
                is_published=True,
            ),
        )
        for order, text in enumerate(["Choisir un psaume adapté à une situation", "Prier un psaume avec un proche malade", "Accueillir la plainte et l'espérance dans la prière"]):
            TrainingSkill.objects.update_or_create(training=psaumes, text=text, defaults=dict(order=order))

        self.stdout.write("Ressources spirituelles…")
        SpiritualResource.objects.update_or_create(
            slug="habiter-lattente",
            defaults=dict(
                title="Habiter l'attente",
                resource_type="meditation",
                summary="Une méditation sur les temps d'attente qui rythment la vie hospitalière.",
                content="L'attente d'un résultat, l'attente d'une visite, l'attente de la guérison... Ce texte propose de relire ces attentes à la lumière de l'espérance chrétienne.",
                author="Père Jean Dupont",
                is_published=True,
                published_at=now - timedelta(days=3),
            ),
        )
        SpiritualResource.objects.update_or_create(
            slug="le-sens-du-service",
            defaults=dict(
                title="Le sens du service",
                resource_type="reflection",
                summary="Une réflexion sur le service comme chemin spirituel, pour les soignants et les bénévoles.",
                content="Servir l'autre dans sa fragilité est une des formes les plus concrètes de l'amour évangélique. Ce texte invite les soignants et bénévoles à relire leur engagement quotidien.",
                author="Sœur Marie-Claire Petit",
                is_published=True,
                published_at=now - timedelta(days=7),
            ),
        )
        prayers = [
            ("priere-du-matin", "Prière du matin", "Seigneur, en commençant cette journée,\nje confie entre tes mains tous ceux qui souffrent,\ntous ceux qui soignent, tous ceux qui accompagnent.\nQue ta lumière guide nos pas et nos gestes,\nque ta paix habite nos cœurs inquiets.\nDonne-nous la force d'être des instruments de ton amour.\nAmen.", "Prière composée par la Pastorale du CHU"),
            ("priere-du-soir", "Prière du soir", "Seigneur, la journée s'achève,\nmerci pour ta présence fidèle à nos côtés.\nNous te confions les joies et les peines de ce jour,\nles guérisons et les souffrances,\nles espoirs et les inquiétudes.\nVeille sur notre sommeil et donne-nous ta paix.\nAmen.", "Adaptée des Complies"),
            ("priere-pour-les-malades", "Prière pour les malades", "Père de miséricorde,\ntu connais la souffrance de tes enfants.\nDonne à ceux qui sont malades\nla certitude de ton amour et de ta proximité.\nAccompagne les familles dans l'épreuve,\nsoutiens les soignants dans leur dévouement.\nAmen.", "Inspirée du rituel des sacrements"),
            ("priere-pour-les-soignants", "Prière pour les soignants", "Seigneur Jésus,\ntoi qui as guéri les malades et consolé les affligés,\nbénis tous ceux qui se consacrent au soin.\nDonne-leur sagesse dans leurs décisions,\ncompassion dans leurs gestes,\nforce dans les moments difficiles.\nAmen.", "Bénédiction des soignants"),
        ]
        for slug, title, content, author in prayers:
            SpiritualResource.objects.update_or_create(
                slug=slug,
                defaults=dict(title=title, resource_type="prayer", summary=content.split("\n")[0], content=content, author=author, is_published=True, published_at=now - timedelta(days=1)),
            )

        guide1, _ = SpiritualResource.objects.update_or_create(
            slug="guide-de-laccompagnement",
            defaults=dict(
                title="Guide de l'accompagnement",
                resource_type="guide",
                summary="Manuel pratique pour l'accompagnement spirituel en milieu hospitalier.",
                content="Ce guide rassemble les repères essentiels pour accompagner les patients et leurs familles : posture d'écoute, gestes de prière, ressources pour les situations difficiles.",
                author="Pastorale du CHU",
                file_size_label="2.1 MB",
                is_published=True,
                published_at=now - timedelta(days=15),
            ),
        )
        if not guide1.pdf_file:
            guide1.pdf_file.save("guide-accompagnement.pdf", ContentFile(FAKE_PDF), save=True)

        guide2, _ = SpiritualResource.objects.update_or_create(
            slug="recueil-de-chants",
            defaults=dict(
                title="Recueil de chants",
                resource_type="guide",
                summary="Chants liturgiques adaptés aux célébrations hospitalières.",
                content="Une sélection de chants pour accompagner les célébrations et les temps de prière au sein du CHU.",
                file_size_label="1.8 MB",
                is_published=True,
                published_at=now - timedelta(days=20),
            ),
        )
        if not guide2.pdf_file:
            guide2.pdf_file.save("recueil-de-chants.pdf", ContentFile(FAKE_PDF), save=True)

        SpiritualResource.objects.update_or_create(
            slug="meditations-audio",
            defaults=dict(
                title="Méditations audio",
                resource_type="guide",
                summary="Méditations guidées pour la détente et la prière.",
                content="Une playlist de méditations guidées, disponible en écoute libre pour les patients et leurs proches.",
                audio_url="https://example.com/audio/meditations-playlist.mp3",
                is_published=True,
                published_at=now - timedelta(days=25),
            ),
        )
        SpiritualResource.objects.update_or_create(
            slug="app-priere-hospitaliere",
            defaults=dict(
                title="App « Prière Hospitalière »",
                resource_type="guide",
                summary="Application mobile avec prières quotidiennes et lectionnaire.",
                content="Une application gratuite pour prier chaque jour, avec les lectures du jour et un espace de méditation personnelle.",
                external_url="https://apps.example.com/priere-hospitaliere",
                is_published=True,
                published_at=now - timedelta(days=30),
            ),
        )

        self.stdout.write("Événements…")
        Event.objects.update_or_create(
            slug="veillee-de-noel-a-la-chapelle",
            defaults=dict(
                title="Veillée de Noël à la chapelle",
                summary="Une veillée de prière et de chants pour accueillir la nuit de Noël.",
                description="Ouverte à tous, patients, familles et soignants, cette veillée propose un temps de recueillement suivi d'un moment convivial.",
                start_date=now + timedelta(days=12, hours=2),
                end_date=now + timedelta(days=12, hours=3, minutes=30),
                location="Chapelle du CHU",
                image_url="https://images.unsplash.com/photo-1482517967863-00e15c9b44be?auto=format&fit=crop&w=800&q=80",
                category=cat_spirituelle,
                is_published=True,
            ),
        )
        Event.objects.update_or_create(
            slug="collecte-solidaire-de-fin-dannee",
            defaults=dict(
                title="Collecte solidaire de fin d'année",
                summary="Collecte de vêtements chauds et de produits d'hygiène pour les familles en difficulté.",
                description="Un stand sera installé dans le hall principal pour recueillir les dons tout au long de la semaine.",
                start_date=now + timedelta(days=3, hours=9),
                end_date=now + timedelta(days=10, hours=18),
                location="Hall principal",
                image_url="https://images.unsplash.com/photo-1593113630400-ea4288922497?auto=format&fit=crop&w=800&q=80",
                category=cat_solidarite,
                is_published=True,
            ),
        )
        Event.objects.update_or_create(
            slug="journee-portes-ouvertes-benevolat",
            defaults=dict(
                title="Journée portes ouvertes bénévolat",
                summary="Venez découvrir les missions de bénévolat proposées par la pastorale du CHU.",
                description="Rencontres avec des bénévoles actuels, présentation du parcours de formation et échanges informels.",
                start_date=now + timedelta(days=20, hours=10),
                end_date=now + timedelta(days=20, hours=13),
                location="Bureau pastoral, Bâtiment A",
                image_url="https://images.unsplash.com/photo-1521737711867-e3b97375f902?auto=format&fit=crop&w=800&q=80",
                category=cat_formation,
                is_published=True,
            ),
        )

        self.stdout.write("Témoignages…")
        for author, role, quote in [
            ("Famille Bernard", "Proches d'un patient", "Merci pour votre présence discrète et réconfortante dans les moments difficiles. Vous nous avez aidés à traverser l'épreuve avec plus de sérénité."),
            ("Camille, infirmière", "Service de soins palliatifs", "Pouvoir échanger avec l'équipe pastorale m'a beaucoup aidée dans les moments les plus difficiles de mon métier."),
            ("Monsieur Aziz", "Ancien patient", "La visite du Père Jean chaque semaine était un vrai moment de paix au milieu de mon hospitalisation."),
        ]:
            Testimonial.objects.update_or_create(author=author, defaults=dict(role=role, quote=quote, is_published=True))

        self.stdout.write("Galerie (albums photo)…")
        GalleryImage.objects.filter(album__isnull=True).delete()
        albums = [
            (
                "celebrations-et-messes", "Célébrations & messes",
                "Messes dominicales, temps de prière et célébrations dans la chapelle du CHU.",
                [
                    ("Messe à la chapelle du CHU", "https://images.unsplash.com/photo-1529156069898-49953e39b3ac?auto=format&fit=crop&w=800&q=80", "Célébrations dominicales et temps de prière communautaire."),
                    ("Chorale hospitalière", "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=800&q=80", "Répétition hebdomadaire ouverte à tous."),
                    ("Décoration de l'Avent", "https://images.unsplash.com/photo-1482517967863-00e15c9b44be?auto=format&fit=crop&w=800&q=80", "Préparation de la chapelle pour le temps de l'Avent."),
                    ("Temps de prière silencieuse", "https://images.unsplash.com/photo-1490730141103-6cac27aaab94?auto=format&fit=crop&w=800&q=80", "Un moment de recueillement partagé le jeudi après-midi."),
                ],
            ),
            (
                "formation-des-benevoles", "Formation des bénévoles",
                "Les temps forts du parcours de formation des accompagnants bénévoles.",
                [
                    ("Journée de découverte", "https://images.unsplash.com/photo-1521737711867-e3b97375f902?auto=format&fit=crop&w=800&q=80", "Accueil de la nouvelle promotion de bénévoles."),
                    ("Atelier d'écoute active", "https://images.unsplash.com/photo-1543269865-cbf427effbad?auto=format&fit=crop&w=800&q=80", "Mise en situation lors de la formation initiale."),
                    ("Remise des attestations", "https://images.unsplash.com/photo-1523240795612-9a054b0db644?auto=format&fit=crop&w=800&q=80", "Fin de parcours pour la promotion de printemps."),
                ],
            ),
            (
                "actions-solidaires", "Actions solidaires",
                "Collectes et actions de solidarité menées avec les familles accompagnées.",
                [
                    ("Collecte solidaire", "https://images.unsplash.com/photo-1593113630400-ea4288922497?auto=format&fit=crop&w=800&q=80", "Distribution de dons aux familles accompagnées."),
                    ("Tri des dons", "https://images.unsplash.com/photo-1593113646773-028c64a8f1b8?auto=format&fit=crop&w=800&q=80", "Préparation des colis avant distribution."),
                    ("Accueil des familles", "https://images.unsplash.com/photo-1469474968028-56623f02e42e?auto=format&fit=crop&w=800&q=80", "Présence bienveillante au chevet des malades et de leurs proches."),
                ],
            ),
            (
                "vie-quotidienne-a-la-chapelle", "Vie quotidienne à la chapelle",
                "Portraits et instants de la vie pastorale au fil des jours.",
                [
                    ("Atelier avec les enfants hospitalisés", "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=800&q=80", "Activités pastorales adaptées pour les plus jeunes."),
                    ("Visite pastorale", "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=800&q=80", "Un temps d'échange dans les couloirs du service."),
                    ("Lecture méditative", "https://images.unsplash.com/photo-1544947950-fa07a98d237f?auto=format&fit=crop&w=800&q=80", "Temps de lecture et de méditation personnelle."),
                    ("La chapelle en soirée", "https://images.unsplash.com/photo-1517832207067-4c4d58f0cc94?auto=format&fit=crop&w=800&q=80", "La chapelle du CHU à la tombée du jour."),
                ],
            ),
        ]
        for order, (slug, title, description, images) in enumerate(albums):
            album, _ = GalleryAlbum.objects.update_or_create(slug=slug, defaults=dict(title=title, description=description, order=order, is_published=True))
            for image_order, (image_title, url, caption) in enumerate(images):
                GalleryImage.objects.update_or_create(album=album, title=image_title, defaults=dict(image_url=url, caption=caption, order=image_order, is_published=True))

        self.stdout.write("Sections de page…")
        home_section, _ = PageSection.objects.update_or_create(
            page_key="home", title="Message de la Pastorale",
            defaults=dict(subtitle="Au cœur du soin, une présence", body="Notre mission est de porter la lumière de l'Évangile auprès de chaque personne accueillie au CHU : écoute, sacrements, prières, soutien des équipes et accompagnement des familles.", order=0, is_published=True),
        )
        about_mission, _ = PageSection.objects.update_or_create(
            page_key="about", title="Présence, prière, soutien",
            defaults=dict(subtitle="Mission & Valeurs", body="Accueillir chacun avec bienveillance, offrir les sacrements, accompagner les moments décisifs de la vie, soutenir les équipes soignantes et développer la solidarité au sein du CHU.", order=0, is_published=True),
        )
        for order, label in enumerate(["Écoute", "Sacrements", "Formation", "Solidarité"]):
            PageSectionTag.objects.update_or_create(section=home_section, label=label, defaults=dict(order=order))
            PageSectionTag.objects.update_or_create(section=about_mission, label=label, defaults=dict(order=order))

        PageSection.objects.update_or_create(
            page_key="gallery", title="Une mémoire en images",
            defaults=dict(subtitle="Galerie", body="Retrouvez les temps forts de la vie pastorale du CHU : célébrations, formations et actions solidaires.", order=0, is_published=True),
        )
        PageSection.objects.update_or_create(
            page_key="contact", title="Nous sommes là pour vous",
            defaults=dict(subtitle="Contact", body="Une question, une demande d'accompagnement, un besoin spirituel ? L'équipe pastorale vous répond dans les meilleurs délais.", order=0, is_published=True),
        )
        PageSection.objects.update_or_create(
            page_key="formations", title="Conditions & Prérequis",
            defaults=dict(body="• Engagement sur la durée complète\n• Entretien de motivation obligatoire\n• Respect du secret professionnel\n• Assiduité aux formations", order=0, is_published=True),
        )

        self.stdout.write("Équipe…")
        team = [
            ("Père Jean Dupont", "Aumônier responsable", "father", "jean.dupont@chu-exemple.fr", "Coordination sacramentelle, homélies, accompagnement des familles et direction pastorale."),
            ("Père Martin Lefèvre", "Aumônier des services pédiatriques", "father", "martin.lefevre@chu-exemple.fr", "Visites quotidiennes, confessions, bénédictions et préparation aux sacrements."),
            ("Sœur Marie-Claire Petit", "Accompagnement et formations", "sister", "marie-claire.petit@chu-exemple.fr", "Accompagnement spirituel, formation des bénévoles et coordination des groupes de parole."),
            ("Camille Rousseau", "Responsable solidarité", "staff", "camille.rousseau@chu-exemple.fr", "Collectes, soutien matériel, coordination des bénévoles et actions caritatives."),
            ("Équipe des visiteurs hospitaliers", "Bénévoles", "volunteer", "", "Présence quotidienne auprès des patients, formation continue et écoute."),
        ]
        for order, (name, role, category, email, bio) in enumerate(team):
            TeamMember.objects.update_or_create(full_name=name, defaults=dict(role_title=role, category=category, email=email, bio=bio, order=order, is_published=True))

        self.stdout.write("Horaires…")
        schedules = [
            ("chapel_hours", "Chapelle du CHU", [("Lundi - Vendredi", "8h00 - 18h00"), ("Samedi", "8h00 - 12h00"), ("Dimanche", "9h00 - 11h00")]),
            ("masses", "Messes", [("Du lundi au vendredi", "12h15"), ("Dimanche", "10h00")]),
            ("contact_permanences", "Horaires des permanences", [("Lundi - Vendredi", "8h00 - 18h00"), ("Samedi", "9h00 - 17h00"), ("Dimanche", "10h00 - 16h00")]),
            ("about_presence", "Horaires de présence", [("Lundi - Vendredi", "8h - 19h"), ("Samedi", "9h - 12h"), ("Messe dominicale", "Dimanche 10h")]),
        ]
        for order, (key, title, slots) in enumerate(schedules):
            schedule, _ = Schedule.objects.update_or_create(key=key, defaults=dict(title=title, order=order))
            for slot_order, (day_label, time_label) in enumerate(slots):
                ScheduleSlot.objects.update_or_create(schedule=schedule, day_label=day_label, defaults=dict(time_label=time_label, order=slot_order))

        self.stdout.write("Services proposés…")
        services = [
            ("🤝", "Accompagnement spirituel", "Écoute bienveillante et accompagnement des patients, familles et personnel soignant dans les moments difficiles.", ["Visites aux patients", "Soutien aux familles", "Accompagnement en fin de vie", "Écoute confidentielle"], "", ""),
            ("⛪", "Sacrements", "Administration des sacrements selon les besoins et demandes des patients et familles.", ["Eucharistie", "Sacrement des malades", "Confession", "Baptême d'urgence"], "", ""),
            ("🙏", "Célébrations", "Organisation de messes et célébrations dans la chapelle du CHU et les services.", ["Messe quotidienne", "Célébrations festives", "Temps de prière", "Bénédictions"], "", ""),
            ("📞", "Permanence d'écoute", "Disponibilité 24h/24 pour les urgences spirituelles et l'accompagnement.", ["Urgences jour et nuit", "Écoute téléphonique", "Intervention rapide", "Soutien d'urgence"], "", ""),
            ("👨‍⚕️", "Soutien aux soignants", "Accompagnement et soutien psychologique et spirituel du personnel hospitalier.", ["Groupes de parole", "Temps de ressourcement", "Accompagnement individuel", "Formation à l'écoute"], "", ""),
            ("🎓", "Formation & Enseignement", "Formations spirituelles et théologiques pour tous les publics.", ["Cours bibliques", "Conférences", "Formation à l'accompagnement", "Retraites spirituelles"], "Voir toutes nos formations", "/formations/"),
        ]
        for order, (icon, title, description, items, link_text, link_url) in enumerate(services):
            service, _ = ServiceOffering.objects.update_or_create(title=title, defaults=dict(icon=icon, description=description, link_text=link_text, link_url=link_url, order=order, is_published=True))
            for item_order, text in enumerate(items):
                ServiceOfferingItem.objects.update_or_create(service=service, text=text, defaults=dict(order=item_order))

        self.stdout.write("Activités régulières…")
        activities = [
            ("⛪", "Messes quotidiennes", "Du lundi au vendredi à 12h15, dimanche à 10h00", "Chapelle du CHU", ""),
            ("📖", "Groupe biblique", "Tous les mardis à 18h30", "Salle pastorale", "Étude et partage autour des Écritures."),
            ("🕯️", "Temps de silence", "Jeudi 13h00 - 13h30", "Chapelle du CHU", "Temps de prière silencieuse."),
            ("👥", "Groupe de parole", "Dernier vendredi du mois à 17h00", "Salle de réunion C", "Pour le personnel soignant."),
            ("🎵", "Chorale hospitalière", "Répétitions le mercredi à 19h00", "Chapelle du CHU", "Ouverte à tous."),
            ("🤲", "Collecte solidaire", "Premier dimanche du mois", "Hall principal", "Pour les familles en difficulté."),
        ]
        for order, (icon, title, schedule_label, location, description) in enumerate(activities):
            RecurringActivity.objects.update_or_create(title=title, defaults=dict(icon=icon, schedule_label=schedule_label, location=location, description=description, order=order, is_published=True))

        self.stdout.write("Temps liturgiques forts…")
        avent, _ = LiturgicalSeason.objects.update_or_create(
            title="Temps de l'Avent",
            defaults=dict(period_label="Décembre", description="Préparation à Noël avec des temps de prière spéciaux et des animations dans les services.", order=0, is_published=True),
        )
        semaine_sainte, _ = LiturgicalSeason.objects.update_or_create(
            title="Semaine Sainte",
            defaults=dict(period_label="Avril", description="Célébrations de la Passion avec chemin de croix et veillée pascale adaptés au milieu hospitalier.", order=1, is_published=True),
        )
        for order, text in enumerate(["Couronnes de l'Avent dans les services", "Chants de Noël avec la chorale", "Distribution de calendriers de l'Avent"]):
            LiturgicalSeasonItem.objects.update_or_create(season=avent, text=text, defaults=dict(order=order))
        for order, text in enumerate(["Chemin de croix dans les couloirs", "Célébration du Jeudi Saint", "Veillée pascale simplifiée"]):
            LiturgicalSeasonItem.objects.update_or_create(season=semaine_sainte, text=text, defaults=dict(order=order))

        self.stdout.write("Méthodes de méditation…")
        methods = [
            ("Lectio Divina", "method", "Méthode traditionnelle en quatre étapes pour goûter la Parole de Dieu.", "15-30 minutes", "", ["Lectio : Lire attentivement", "Meditatio : Ruminer le texte", "Oratio : Prier spontanément", "Contemplatio : Se reposer en Dieu"]),
            ("Méditation ignatienne", "method", "Entrer dans une scène d'Évangile en imagination, se placer aux côtés de Jésus.", "20-45 minutes", "", ["Composition de lieu", "Application des sens", "Colloque avec Jésus"]),
            ("Méditation d'un verset", "method", "Choisir un verset court et le répéter doucement, laisser un mot résonner en nous.", "5-15 minutes", "", ["Choisir un verset court", "Répéter lentement", "Goûter chaque mot"]),
            ("Méditation du souffle", "silence", "S'installer confortablement et laisser une courte prière rythmer la respiration.", "5-10 minutes", "", ["S'installer confortablement", "Respirer calmement et profondément", "À l'inspiration : « Jésus »", "À l'expiration : « j'ai confiance en toi »"]),
            ("Contemplation de la Présence", "silence", "Se rappeler que Dieu est là, maintenant, et rester dans cette communion simple.", "10-20 minutes", "Commencer par 5 minutes par jour. L'important n'est pas la durée mais la régularité. Dieu accueille notre prière telle qu'elle est, dans nos limites et notre fragilité.", ["Fermer les yeux et se centrer", "Se rappeler que Dieu est là", "Accueillir paix ou agitation sans jugement", "Conclure par un « merci » du cœur"]),
        ]
        for order, (title, category, description, duration_label, tip, method_steps) in enumerate(methods):
            method, _ = MeditationMethod.objects.update_or_create(title=title, defaults=dict(category=category, description=description, duration_label=duration_label, tip=tip, order=order, is_published=True))
            for step_order, text in enumerate(method_steps):
                MeditationMethodStep.objects.update_or_create(method=method, text=text, defaults=dict(order=step_order))

        self.stdout.write("Versets et psaumes…")
        daily_verses = [
            ("Isaïe 43, 1", "Je t'ai appelé par ton nom", "Dieu présent dans l'épreuve, proche de chacun personnellement."),
            ("Mt 11, 28", "Venez à moi, vous tous qui peinez", "Repos et consolation en Christ pour les soignants et les patients."),
            ("Lc 10, 33", "Le Bon Samaritain", "Modèle de proximité, de compassion et de soin pour autrui."),
        ]
        for order, (reference, quote, context) in enumerate(daily_verses):
            BibleVerse.objects.update_or_create(verse_type="daily", reference=reference, defaults=dict(quote=quote, context=context, order=order, is_published=True))

        psalms = [
            ("Psaume 23 - Le Bon Berger", "Ps 23", "Pour la confiance et la protection", "Le Seigneur est mon berger : je ne manque de rien...", "Réconfort"),
            ("Psaume 46 - Dieu notre refuge", "Ps 46", "Dans les moments d'épreuve", "Dieu est pour nous un refuge et un appui...", "Force"),
            ("Psaume 139 - Dieu me connaît", "Ps 139", "Pour se sentir aimé de Dieu", "Seigneur, tu me sondes et tu sais...", "Amour"),
            ("Psaume 91 - Sous ses ailes", "Ps 91", "Protection et sécurité en Dieu", "Qui habite à l'abri du Très-Haut...", "Protection"),
            ("Psaume 130 - Du fond de l'abîme", "Ps 130", "Dans la souffrance et l'espérance", "Du fond de l'abîme, je crie vers toi...", "Espérance"),
            ("Psaume 103 - Bénis le Seigneur", "Ps 103", "Action de grâce et louange", "Bénis le Seigneur, ô mon âme...", "Louange"),
        ]
        for order, (title, reference, context, quote, tag_label) in enumerate(psalms):
            BibleVerse.objects.update_or_create(verse_type="psalm", reference=reference, defaults=dict(title=title, context=context, quote=quote, tag_label=tag_label, order=order, is_published=True))

        self.stdout.write("Questions bibliques…")
        questions = [
            (
                "Que signifie « Dieu est amour » dans notre souffrance ?", "Marie", "Service oncologie", father_jean, "souffrance",
                "Cette question touche au cœur du mystère de la souffrance humaine. Quand saint Jean écrit « Dieu est amour » (1 Jn 4,8), il ne nie pas la réalité de la souffrance, mais révèle que même dans l'épreuve, Dieu demeure présent et fidèle.\n\nL'amour de Dieu ne nous épargne pas toujours la souffrance, mais il la transforme. Jésus lui-même a souffert sur la croix, montrant que Dieu n'est pas étranger à notre condition humaine.\n\nDans la maladie, l'amour de Dieu se manifeste par sa proximité, par la paix qu'il donne, et souvent par l'amour des autres qui nous entourent.",
                ["1 Jean 4,8", "Matthieu 11,28", "Romains 8,28"],
            ),
            (
                "Comment prier quand on n'arrive plus à croire ?", "Jean", "Famille d'un patient", None, "priere",
                "Les périodes de doute et de sécheresse spirituelle font partie du cheminement de foi de beaucoup de croyants. Jésus lui-même a crié sur la croix : « Mon Dieu, pourquoi m'as-tu abandonné ? » (Mt 27,46).\n\nQuand les mots manquent, la prière peut être simplement un cri du cœur, un silence offert à Dieu, ou la répétition d'une phrase simple comme « Jésus, j'ai confiance en toi ».\n\nParfois, il est bon de prier avec les mots des autres : les Psaumes, le Notre Père, ou de demander à d'autres de prier pour nous.",
                ["Psaume 22", "Matthieu 6,9-13", "Romains 8,26"],
            ),
            (
                "Que devient-on après la mort selon la Bible ?", "Famille Dubois", "Soins palliatifs", father_martin, "vie_eternelle",
                "La Bible nous enseigne que la mort n'est pas une fin, mais un passage vers la vie éternelle avec Dieu. Jésus a dit : « Je suis la résurrection et la vie. Celui qui croit en moi, même s'il meurt, vivra » (Jn 11,25).\n\nSaint Paul nous rappelle que nous avons « une demeure éternelle dans les cieux » (2 Co 5,1). La mort du corps n'est donc pas la mort de la personne.\n\nL'espérance chrétienne affirme la résurrection des morts et la vie éternelle, dans l'attente de la résurrection finale.",
                ["Jean 11,25", "2 Corinthiens 5,1", "1 Thessaloniciens 4,13"],
            ),
            (
                "Pourquoi recevoir le sacrement des malades ?", "Robert", "Cardiologie", father_jean, "sacrements",
                "Le sacrement des malades n'est pas réservé aux derniers instants de la vie. Il peut être reçu dès qu'une maladie grave ou une intervention importante fragilise une personne.\n\nCe sacrement apporte réconfort, paix et force spirituelle. Il unit la souffrance du malade à celle du Christ et rappelle que l'Église tout entière porte cette épreuve avec lui.\n\nN'hésitez pas à en faire la demande auprès de l'équipe pastorale.",
                ["Jacques 5,14-15"],
            ),
            (
                "L'euthanasie est-elle compatible avec la foi chrétienne ?", "Anonyme", "Soins palliatifs", father_martin, "ethique",
                "L'Église catholique distingue nettement l'euthanasie, qui vise à provoquer la mort, des soins palliatifs, qui visent à soulager la souffrance sans hâter la mort.\n\nLa dignité de toute vie humaine, y compris dans la grande fragilité, appelle à un accompagnement respectueux jusqu'au bout, plutôt qu'à une réponse qui supprimerait la personne pour supprimer la souffrance.\n\nCette question mérite un dialogue personnel avec l'équipe pastorale, dans le respect de chaque situation.",
                ["Évangile de la Vie"],
            ),
            (
                "Comment continuer à prier en famille malgré l'éloignement ?", "Famille Nguyen", "Pédiatrie", None, "famille",
                "L'éloignement dû à l'hospitalisation ne rompt pas les liens de prière familiale. De nombreuses familles choisissent de prier au même moment, chacune de son côté, en pensée les unes avec les autres.\n\nLes appels ou messages peuvent aussi porter une intention de prière commune, comme un « Notre Père » partagé à distance.\n\nL'équipe pastorale peut aussi transmettre des nouvelles et des mots de réconfort entre le patient et sa famille.",
                ["Matthieu 18,20"],
            ),
        ]
        for question, questioner_name, questioner_context, respondent, category, answer, tags in questions:
            bible_question, _ = BibleQuestion.objects.update_or_create(
                question=question,
                defaults=dict(questioner_name=questioner_name, questioner_context=questioner_context, respondent=respondent, category=category, answer=answer, is_published=True),
            )
            for order, label in enumerate(tags):
                BibleQuestionTag.objects.update_or_create(question=bible_question, label=label, defaults=dict(order=order))

        self.stdout.write("Liens externes…")
        for order, (title, url, description) in enumerate([
            ("Vatican.va", "https://www.vatican.va", "Textes officiels du Vatican"),
            ("Aelf.org", "https://www.aelf.org", "Lectures liturgiques quotidiennes"),
            ("Prionseneglise.fr", "https://www.prionseneglise.fr", "Prières et méditations quotidiennes"),
        ]):
            ExternalLink.objects.update_or_create(title=title, defaults=dict(url=url, description=description, order=order, is_published=True))

        self.stdout.write("Cartes de contact…")
        contact_channels = [
            ("services_urgence", "Urgences spirituelles", "Pour toute urgence spirituelle, 24h/24 et 7j/7", "", "01 23 45 67 90", "", "Demander l'aumônier de garde"),
            ("services_visite", "Demande de visite", "Pour programmer une visite pastorale", "pastorale@chu-exemple.fr", "", "", "Réponse sous 24h"),
            ("evenements_inscriptions", "Contact et inscriptions", "", "evenements@chu-exemple.fr", "01 23 45 67 89", "2156", "Bureau pastoral - Bâtiment A, niveau 0"),
            ("formations_renseignements", "Inscriptions & Renseignements", "", "formations@chu-exemple.fr", "01 23 45 67 89", "2158", "Bureau formation - Pastorale CHU"),
            ("bible_questions", "Comment nous contacter ?", "Toutes vos questions sont traitées avec la plus stricte confidentialité. Les réponses publiées le sont toujours de manière anonyme, après accord de la personne.", "questions.bible@chu-exemple.fr", "01 23 45 67 89", "2159", "Bureau pastoral - Bâtiment A, niveau 0"),
            ("about_partners", "Pôle Soins Palliatifs", "Présence rituelle, accompagnement spirituel et soutien des familles en fin de vie.", "", "", "", ""),
            ("about_partners", "Service de Psychologie", "Accompagnement croisé, groupes de parole et travail en complémentarité.", "", "", "", ""),
            ("about_partners", "Formation des soignants", "Interventions sur l'éthique, la spiritualité et l'approche globale du soin.", "", "", "", ""),
            ("ressources_contacts", "Pastorale de la Santé diocésaine", "Accompagnement et formation", "", "01 23 45 67 91", "", ""),
            ("ressources_contacts", "Service d'écoute téléphonique", "SOS Amitié · 24h/24", "", "09 72 39 40 50", "", ""),
            ("ressources_contacts", "Centre spirituel régional", "Retraites et accompagnement", "accueil@centre-spirituel.fr", "", "", ""),
        ]
        for order, (section_key, title, description, email, phone, extension, note) in enumerate(contact_channels):
            ContactChannel.objects.update_or_create(section_key=section_key, title=title, defaults=dict(description=description, email=email, phone=phone, extension=extension, note=note, order=order, is_published=True))

        self.stdout.write("Accès & stationnement…")
        for order, (icon, label, text) in enumerate([
            ("🚗", "En voiture", "Parking visiteurs gratuit les 2 premières heures, puis 2€/heure."),
            ("🚌", "En transport public", "Métro ligne 4, arrêt « CHU Centre », bus 12 et 34."),
            ("🚶", "À pied", "La chapelle est accessible depuis l'entrée principale, suivre la signalétique « Chapelle/Aumônerie »."),
        ]):
            AccessInstruction.objects.update_or_create(label=label, defaults=dict(icon=icon, text=text, order=order, is_published=True))

        self.stdout.write(self.style.SUCCESS("Données de démonstration créées avec succès."))
