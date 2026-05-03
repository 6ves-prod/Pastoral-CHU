from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "index.html")

def actualites(request):
    return render(request, "actualites.html")

def services(request):
    return render(request, "services/services.html")

def evenements(request):
    return render(request, "services/evenements.html")

def formations(request):
    return render(request, "services/formations.html")

def ressources(request):
    return render(request, "services/ressources.html")

def galerie(request):
    return render(request, "galerie.html")

def qui_sommes_nous(request):
    return render(request, "qui-sommes-nous.html")

def bible(request):
    return render(request, "bible/bible.html")

def bible_mediter(request):
    return render(request, "bible/bible-mediter.html")

def bible_reponses(request):
    return render(request, "bible/bible-reponses.html")

def contact(request):
    return render(request, "contact.html")