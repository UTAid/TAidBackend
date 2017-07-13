'''Provides a visual of everything available to the rest api'''

from django.shortcuts import render
from rest_framework import response, schemas
from rest_framework.decorators import api_view, renderer_classes
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer


@api_view()
@renderer_classes([OpenAPIRenderer, SwaggerUIRenderer])
def schema_view(request):
    generator = schemas.SchemaGenerator(title='TAid API')
    return response.Response(generator.get_schema(request=request))
