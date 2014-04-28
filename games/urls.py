from django.conf.urls import patterns, include, url

urlpatterns = patterns('games.views',
    url(r'^create', 'create_slots'),
    url(r'^list', 'slots'),
    url(r'^cards', 'available_cards'),
    url(r'^apply/(?P<id>[0-9]+)/(?P<card>[a-z]+)/(?P<from_right>\d+)', 'apply_slot'),
)