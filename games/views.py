from functools import wraps
from annoying.decorators import ajax_request
from django.contrib.auth.decorators import login_required

from models import *

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

        del kwargs['game_id']

        return func(request, *args, **kwargs)

    return wrapper

@ajax_request
def create_game(request):

    Slot.drop_collection()
    Game.drop_collection()

    game = Game(first_user_id=1, second_user_id=2)
    game.save()

    def add_slots(lst, user_id):
        for i in range(10):
            slot = Slot()
            slot.slot_id = i+1
            slot.game_id = game.id
            slot.user_id = user_id
            slot.value = 100
            slot.term = create_identity()
            slot.save()
            lst.append(slot)

    add_slots(game.first_slots, game.first_user_id)
    add_slots(game.second_slots, game.second_user_id)

    game.save()

    return {'result': '1'}

@ajax_request
@login_required
@game_request
def slots(request):

    result = [slot.as_dict() for slot in request.my_slots]

    return {'slots': result}

CARDS = {
    'id': create_identity,
    'zero': create_zero,
    'succ': Succ,
    'dbl': Dbl,
    'get': Get,
    'inc': Inc,
}

@ajax_request
def available_cards(request):
    return {'cards': CARDS.keys()}

@ajax_request
@login_required
@game_request
def apply_slot(request, slot_id, card, from_right):

    slot = request.my_slots.filter(slot_id=slot_id)[0]

    term = CARDS[card]()

    if int(from_right) == 1:
        application = Application(first_term=slot.term, second_term=term)
    else:
        application = Application(second_term=slot.term, first_term=term)

    try:
        new_slot_term = make_reduction(application, request)
    except ReductionException as e:
        return {'error': str(e)}

    slot.term = new_slot_term

    slot.save()

    return { 'slot': slot.as_dict() }