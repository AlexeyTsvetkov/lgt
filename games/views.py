from functools import wraps
from annoying.decorators import ajax_request, render_to
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response

from models import *
from reduction import *
from exceptions import GameException

def game_request(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):

        if 'game_id' not in kwargs:
            raise Exception("game_id expected")

        game_id = kwargs['game_id']

        game = Game.objects(id=game_id)[0]

        request.game = game
        request.slots = Slot.objects(game_id=game_id)

        if request.user is not None:
            user_id = request.user.id

            is_first_user = game.first_user_id == user_id

            request.proponent_id = user_id
            request.opponent_id = game.second_user_id if is_first_user else game.first_user_id
            request.my_slots = request.slots.filter(user_id=user_id)
            request.opponent_slots = request.slots.filter(user_id=request.opponent_id)

        del kwargs['game_id']

        return func(request, *args, **kwargs)

    return wrapper

@login_required
def create_game(request):

    Slot.drop_collection()
    Game.drop_collection()

    game = Game(first_user_id=1)
    game.save()

    game.accept_opponent(2)

    return redirect_to_room(game.id)

@ajax_request
@login_required
@game_request
def game_state(request):

    return {'data': request.game.as_dict(request.user.id) }

CARDS = {
    'id': create_identity,
    'zero': create_zero,
    'scomb': create_s_comb,
    'kcomb': create_k_comb,
    'succ': Succ,
    'dbl': Dbl,
    'get': Get,
    'inc': Inc,
    'dec': Dec,
}

@ajax_request
def available_cards(request):
    return {'cards': CARDS.keys()}

def game_assert(expr, message="Error"):
    if not expr:
        raise GameException(message)

def apply_term_to_slot(request, slot_id, term, from_right):
    try:
        game_assert(request.game.is_active(), "Game is not active")
        game_assert(request.game.is_user_turn(request.user.id), "It's not your turn")

        slot = request.my_slots.filter(slot_id=slot_id)[0]

        game_assert(slot.is_alive(), "Slot is not active")

        if int(from_right) == 1:
            application = Application(first_term=slot.term, second_term=term)
        else:
            application = Application(second_term=slot.term, first_term=term)

        new_slot_term = make_reduction(application, request)
    except Exception as e:
        return {'error': str(e)}

    slot.term = new_slot_term
    slot.save()

    request.game.flip_turn()
    request.game.save()

    return {'data': request.game.as_dict(request.user.id)}

@ajax_request
@login_required
@game_request
def apply_card(request, slot_id, card, from_right):
    term = CARDS[card]()

    return apply_term_to_slot(request, slot_id, term, from_right)

@ajax_request
@login_required
@game_request
def apply_slot(request, slot_id, second_slot_id, from_right):
    game_assert(slot_id != second_slot_id, "Don't apply to the same slot")

    second_slot = request.my_slots.filter(slot_id=second_slot_id)[0]
    game_assert(second_slot.is_alive(), "Slot is not alive")

    return apply_term_to_slot(request, slot_id, second_slot.term, from_right)

@login_required
@render_to('games/my_games.html')
def my_games(request):
    games = Game.\
        objects(Q(first_user_id=request.user.id) | Q (second_user_id=request.user.id)).\
        filter(second_user_id__exists=True)
    return {'games': games}

def redirect_to_room(game_id):
   return HttpResponseRedirect(reverse('frontend.views.room', kwargs={'game_id': game_id}))

@login_required
def new_game(request):

    game = Game.objects(second_user_id__exists=False).filter(first_user_id__ne=request.user.id).first()
    my_game = Game.objects(second_user_id__exists=False).filter(first_user_id=request.user.id).first()

    if game is None or my_game is not None:
        game = my_game if my_game is not None else Game(first_user_id=request.user.id).save()
        return HttpResponseRedirect(reverse('games.views.wait_opponent', kwargs={'game_id': game.id}))
    else:
        game.accept_opponent(request.user.id)
        return redirect_to_room(game.id)


@login_required
def wait_opponent(request, game_id):
    game = Game.objects(id=game_id)[0]
    if game.second_user_id is None:
        return render_to_response('games/wait.html')
    else:
        return redirect_to_room(game.id)
