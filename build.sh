#!/usr/bin/env bash

set -o errexit

pip install -r requirements.txt

python manage.py makemigrations --noinput

python manage.py migrate

echo "=== Vérification du superutilisateur ==="

python manage.py shell <<EOF
from django.contrib.auth import get_user_model
import os

User = get_user_model()

username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

print(f"Nom d'utilisateur : {username}")
print(f"Email : {email}")

if not username:
    print("❌ DJANGO_SUPERUSER_USERNAME n'est pas défini.")
elif not password:
    print("❌ DJANGO_SUPERUSER_PASSWORD n'est pas défini.")
else:
    print("Recherche du superutilisateur...")

    if User.objects.filter(username=username).exists():
        print(f"ℹ️ Le superutilisateur '{username}' existe déjà.")
    else:
        print(f"Création du superutilisateur '{username}'...")
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print("✅ Superutilisateur créé avec succès.")
EOF

echo "=== Collecte des fichiers statiques ==="
python manage.py collectstatic --noinput