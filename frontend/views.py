from annoying.decorators import render_to
from django.contrib.auth.decorators import login_required
from games.views import game_request


@login_required
@game_request
@render_to('frontend/index.html')
def room(request):
    return {'game': request.game}
