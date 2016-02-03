from django.conf.urls import patterns, include, url
from django.contrib import admin
from TAid.settings import common

from apps.taid import viewsets

urlpatterns = patterns('',
        # Examples:
        # url(r'^$', 'TAid.views.home', name='home'),
        # url(r'^blog/', include('blog.urls')),

        url(r'^api/v0/', include(viewsets.router.urls)),
        url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
        url(r'^admin/', include(admin.site.urls)),
        # static files (images, css, javascript, etc.)
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': common.MEDIA_ROOT},
            ),
        )
