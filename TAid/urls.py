"""TAid URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
import rest_framework_jwt.views as jwt

from apps import viewsets
from apps.views import schema_view


v0_patterns = [
    url(r'^', include(viewsets.router.urls)),
    url(r'^docs/', schema_view),
]

api_patterns = [
    url(r'^v0/', include(v0_patterns)),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^token-auth/', jwt.obtain_jwt_token),
    url(r'^token-refresh/', jwt.refresh_jwt_token),
    url(r'^token-verify/', jwt.verify_jwt_token),
]

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(api_patterns)),
]
