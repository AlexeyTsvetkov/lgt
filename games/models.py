from mongoengine import *

connect('lgt')

from terms import *
from term_printer import pretty_print

class Slot(Document):
    slot_id = IntField()

    game_id = ObjectIdField()
    user_id = IntField()

    value = IntField()
    term = EmbeddedDocumentField(Term)

    def is_alive(self):
        return self.value > 0

    def as_dict(self):
        return {
            'id': str(self.slot_id),
            'is_alive': self.is_alive(),
            'vitality': self.value,
            'term': pretty_print(self.term)
        }

GAME_STATE_AWAITING = 0
GAME_STATE_RUNNING = 1
GAME_STATE_ENDED = 2

GAME_STATE_NAMES = ("awaiting", "running", "ended",)

GAME_RESULT_FIRST = 0
GAME_RESULT_SECOND = 1

def does_prefer_combinators(user_id):
    return user_id == 1

class Game(Document):
    first_user_id = IntField()
    second_user_id = IntField()

    winner = IntField()

    state = IntField(default=GAME_STATE_AWAITING)
    is_first_turn = BooleanField(default=True)

    first_slots = ListField(ReferenceField(Slot))
    second_slots = ListField(ReferenceField(Slot))

    def accept_opponent(self, opponent_id):
        self.second_user_id = opponent_id

        def add_slots(lst, user_id):
            is_comb = does_prefer_combinators(user_id)
            for i in range(10):
                slot = Slot()
                slot.slot_id = i+1
                slot.game_id = self.id
                slot.user_id = user_id
                slot.value = 100
                slot.term = create_identity(is_comb)
                slot.save()
                lst.append(slot)

        add_slots(self.first_slots, self.first_user_id)
        add_slots(self.second_slots, self.second_user_id)

        self.save()

    def update_state(self):
        state = self.state
        if state == GAME_STATE_AWAITING:
            if self.second_user_id is not None:
                self.state = GAME_STATE_RUNNING
            return
        if state == GAME_STATE_RUNNING:
            if len(filter(lambda s: s.is_alive(), self.first_slots)) == 0:
                self.state = GAME_STATE_ENDED
                self.winner = GAME_RESULT_FIRST
            elif len(filter(lambda s: s.is_alive(), self.second_slots)) == 0:
                self.state = GAME_STATE_ENDED
                self.winner = GAME_RESULT_SECOND

    def is_active(self):
        return self.state == GAME_STATE_RUNNING

    def save(self, force_insert=False, validate=True, clean=True, write_concern=None, cascade=None, cascade_kwargs=None,
             _refs=None, **kwargs):

        self.update_state()

        return super(Game, self).save(force_insert, validate, clean, write_concern, cascade, cascade_kwargs, _refs,
                                      **kwargs)


    def is_user_turn(self, user_id):
        if self.first_user_id == user_id and self.is_first_turn:
            return True
        if self.second_user_id == user_id and not self.is_first_turn:
            return True

        return False

    def flip_turn(self):
        pass
        #self.is_first_turn = not self.is_first_turn

    def as_dict(self, user_id=None):
        if user_id is None or (user_id != self.first_user_id and user_id != self.second_user_id):
            raise Exception("undefined")

        proponent_slots = self.first_slots
        opponent_slots = self.second_slots
        if user_id != self.first_user_id:
            proponent_slots, opponent_slots = opponent_slots, proponent_slots

        result = {
            'id': str(self.id),
            'state': GAME_STATE_NAMES[self.state],
            'proponent_slots': map(lambda s: s.as_dict(), proponent_slots),
            'opponent_slots' : map(lambda s: s.as_dict(), opponent_slots)
        }

        if self.state == GAME_STATE_ENDED:
            result['winner'] = self.winner

        if self.state == GAME_STATE_RUNNING:
            result['is_your_turn'] = self.is_user_turn(user_id)

        return result
