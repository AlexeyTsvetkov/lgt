from django.conf.urls import patterns, url

urlpatterns = patterns('games.views',
    url(r'^create', 'create_game'),
    url(r'^(?P<game_id>[0-9a-z]+)/list', 'slots'),
    url(r'^cards', 'available_cards'),
    url(r'^(?P<game_id>[0-9a-z]+)/apply/(?P<slot_id>[0-9]+)/(?P<card>[a-z]+)/(?P<from_right>\d+)', 'apply_slot'),
)