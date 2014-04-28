from django.conf.urls import patterns, include, url

urlpatterns = patterns('games.views',
    url(r'^create', 'create_slots'),
    url(r'^list', 'slots'),
    url(r'^apply/(?P<id>[a-z0-9]+)/(?P<kind>[a-z]+)/(?P<from_right>\d+)', 'apply_slot'),
)