from django.conf.urls import patterns, include, url
from django.contrib import admin
import rest_framework_jwt.views as jwt

from TAid.settings import common
from apps.api import viewsets


urlpatterns = patterns('',
        # Examples:
        # url(r'^$', 'TAid.views.home', name='home'),
        # url(r'^blog/', include('blog.urls')),

        url(r'^api/v0/', include(viewsets.router.urls)),
        url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
        url(r'^api-token-auth/', jwt.obtain_jwt_token),
        url(r'^api-token-refresh/', jwt.refresh_jwt_token),
        url(r'^api-token-verify/', jwt.verify_jwt_token),
        url(r'^admin/', include(admin.site.urls)),
        # static files (images, css, javascript, etc.)
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': common.MEDIA_ROOT},
            ),
        )
