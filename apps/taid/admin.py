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
    exclude = (
            'students',
            'instructors',
            'tuts',
            'pracs'
            )

class LectureAdmin(admin.ModelAdmin):
    exclude = (
            'creator', 
            'title',
            'description'
            )

class TutorialAdmin(admin.ModelAdmin):
    exclude = (
            'creator', 
            'title',
            'description'
            )


class PracticalAdmin(admin.ModelAdmin):
    exclude = (
            'creator', 
            'title',
            'description'
            )


class AssignmentInline(admin.StackedInline):
    model = models.Assignment

    exclude = (
            "marks",
            )


class MarkInline(admin.StackedInline):
    model = models.Mark


class AssignmentAdmin(admin.ModelAdmin):
    exclude = (
            "marks",
            )
    inlines = (
            AssignmentInline,
            MarkInline,
            )


admin.site.register(models.Instructor, InstructorAdmin)
admin.site.register(models.TeachingAssistant, TeachingAssistantAdmin)
admin.site.register(models.Student, StudentAdmin)
admin.site.register(models.Identification, IdentificationAdmin)
admin.site.register(models.Course, CourseAdmin)
admin.site.register(models.Tutorial, TutorialAdmin)
admin.site.register(models.Practical, PracticalAdmin)
admin.site.register(models.Assignment, AssignmentAdmin)
admin.site.register(models.Lecture, LectureAdmin)
