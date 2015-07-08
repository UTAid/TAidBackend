from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView, ListView
from schedule.models import Calendar
from schedule.periods import Year, Month, Week, Day

import schedule.urls

urlpatterns = patterns('',
        # Examples:
        # url(r'^$', 'TAid.views.home', name='home'),
        # url(r'^blog/', include('blog.urls')),

        url(r'^admin/', include(admin.site.urls)),

        # Calendar views
    	url(r'^calendar-list/$',
        ListView.as_view(queryset=Calendar.objects.all(),
                         template_name='schedule/calendar_list.html'),
        name="calendar_list"),

    	# Demo that came with the plugin
        url(r'^calendar-demo/', include(schedule.urls))

        )
