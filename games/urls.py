from django.conf.urls import patterns, url

urlpatterns = patterns('games.views',
    url(r'^create', 'create_game'),
    url(r'^$', 'my_games'),
    url(r'^new$', 'new_game'),
    url(r'^wait/(?P<game_id>[0-9a-z]+)$', 'wait_opponent'),
    url(r'^(?P<game_id>[0-9a-z]+)/game_state', 'game_state'),
    url(r'^cards', 'available_cards'),
    url(r'^(?P<game_id>[0-9a-z]+)/apply/(?P<slot_id>[0-9]+)/(?P<second_slot_id>[0-9]+)/(?P<from_right>\d+)', 'apply_slot'),
    url(r'^(?P<game_id>[0-9a-z]+)/apply/(?P<slot_id>[0-9]+)/(?P<card>[a-z]+)/(?P<from_right>\d+)', 'apply_card'),
)
