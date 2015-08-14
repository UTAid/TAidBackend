from django.conf.urls import patterns, include, url
from django.contrib import admin

from apps.taid import viewsets

from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'instructor', viewsets.InstructorViewSet)
router.register(r'teaching_assistant', viewsets.TeachingAssistantViewSet)
router.register(r'student', viewsets.StudentViewSet)
router.register(r'course', viewsets.CourseViewSet)
router.register(r'tutorial', viewsets.TutorialViewSet)
router.register(r'Practical', viewsets.PracticalViewSet)

urlpatterns = patterns('',
        # Examples:
        # url(r'^$', 'TAid.views.home', name='home'),
        # url(r'^blog/', include('blog.urls')),

        url(r'^api/v1/', include(router.urls)),
        url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
        url(r'^admin/', include(admin.site.urls)),
        )
