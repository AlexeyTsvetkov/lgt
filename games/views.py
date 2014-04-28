from annoying.decorators import ajax_request

from models import *

@ajax_request
def create_slots(request):

    Slot.drop_collection()

    for i in range(10):
        slot = Slot()
        slot.slot_id = i+1
        slot.value = 100
        slot.term = create_identity()
        slot.save()

    return {'result': '1'}

@ajax_request
def slots(request):

    result = [slot.as_dict() for slot in Slot.objects]

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
def apply_slot(request, id, card, from_right):

    slot = Slot.objects(slot_id=id)[0]

    term = CARDS[card]()

    if int(from_right) == 1:
        application = Application(first_term=slot.term, second_term=term)
    else:
        application = Application(second_term=slot.term, first_term=term)

    try:
        new_slot_term = make_reduction(application)
    except ReductionException as e:
        return {'error': str(e)}

    slot.term = new_slot_term

    slot.save()

    return { 'slot': slot.as_dict() }