from django.views.generic import ListView
from django.shortcuts import render_to_response, get_object_or_404

from schedule.models import Calendar


class ListCalendarsView(ListView):
    model = Calendar
    template_name = 'calendar_list.html'
