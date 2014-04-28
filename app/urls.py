from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import app.settings as settings

urlpatterns = patterns('',
    (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'app/login.html'}),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
    url(r'game/', include('games.urls')),
    url(r'app/', include('frontend.urls')),

    url(r'games/', include('games.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

if True or settings.DEBUG:
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
    )
