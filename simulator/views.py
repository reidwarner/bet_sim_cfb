from django.http import HttpResponse
from django.template import loader
from .models import Game
from .scripts import data_scrape


def simulator(request):
    data_scrape()
    upcoming_games = Game.objects.all().values()
    template = loader.get_template('simulator.html')
    context = {
        'upcoming_games': upcoming_games
    }
    return HttpResponse(template.render(context, request))