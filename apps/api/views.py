'''Provides a visual of everything available to the rest api'''

from rest_framework import response, schemas
from rest_framework.decorators import api_view, renderer_classes
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer

from django.views.generic import ListView
from django.shortcuts import render_to_response, get_object_or_404

from schedule.models import Calendar


@api_view()
@renderer_classes([OpenAPIRenderer, SwaggerUIRenderer])
def schema_view(request):
    generator = schemas.SchemaGenerator(title='TAid API')
    return response.Response(generator.get_schema(request=request))

class ListCalendarsView(ListView):
    model = Calendar
    template_name = 'calendar_list.html'
