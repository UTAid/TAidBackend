from django.contrib import admin
from apps.taid import models


class InstructorAdmin(admin.ModelAdmin):
    pass


class TeachingAssistantAdmin(admin.ModelAdmin):
    pass


class StudentAdmin(admin.ModelAdmin):
    pass


class IdentificationAdmin(admin.ModelAdmin):
    pass


class CourseAdmin(admin.ModelAdmin):
    pass


class TutorialAdmin(admin.ModelAdmin):
    pass


class PracticalAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Instructor, InstructorAdmin)
admin.site.register(models.TeachingAssistant, TeachingAssistantAdmin)
admin.site.register(models.Student, StudentAdmin)
admin.site.register(models.Identification, IdentificationAdmin)
admin.site.register(models.Course, CourseAdmin)
admin.site.register(models.Tutorial, TutorialAdmin)
admin.site.register(models.Practical, PracticalAdmin)
