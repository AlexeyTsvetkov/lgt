from django.conf.urls import patterns, include, url

urlpatterns = patterns('frontend.views',
    url(r'^room/(?P<game_id>[a-z0-9]+)', 'room'),
)
