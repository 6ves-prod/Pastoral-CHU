from django.db import migrations

PRETRE_MODELS = [
    "homily",
    "biblequestion",
    "biblequestiontag",
    "bibleverse",
    "meditationmethod",
    "meditationmethodstep",
    "liturgicalseason",
    "liturgicalseasonitem",
    "spiritualresource",
    "father",
]

CM_MODELS = [
    "article",
    "category",
    "event",
    "training",
    "trainingstep",
    "trainingskill",
    "galleryalbum",
    "galleryimage",
    "heroslide",
    "pagesection",
    "pagesectiontag",
    "teammember",
    "externallink",
    "testimonial",
    "serviceoffering",
    "serviceofferingitem",
    "recurringactivity",
    "contactchannel",
    "accessinstruction",
    "schedule",
    "scheduleslot",
]

CM_READONLY_MODELS = [
    "contactmessage",
]


def _permissions_for(Permission, ContentType, app_label, model_names, actions=("add", "change", "delete", "view")):
    content_types = ContentType.objects.filter(app_label=app_label, model__in=model_names)
    return Permission.objects.filter(content_type__in=content_types, codename__regex=r"^(%s)_" % "|".join(actions))


def create_role_groups(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    ContentType = apps.get_model("contenttypes", "ContentType")

    pretre, _ = Group.objects.get_or_create(name="Prêtre")
    pretre.permissions.set(_permissions_for(Permission, ContentType, "app", PRETRE_MODELS))

    cm, _ = Group.objects.get_or_create(name="Community Manager")
    cm_permissions = list(_permissions_for(Permission, ContentType, "app", CM_MODELS))
    cm_permissions += list(_permissions_for(Permission, ContentType, "app", CM_READONLY_MODELS, actions=("change", "view")))
    cm.permissions.set(cm_permissions)


def remove_role_groups(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Group.objects.filter(name__in=["Prêtre", "Community Manager"]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0011_galleryalbum_cover_image_galleryimage_image_and_more"),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.RunPython(create_role_groups, remove_role_groups),
    ]
