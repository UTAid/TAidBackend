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


class TutorialInline(admin.StackedInline):
    model = models.Tutorial


class PracticalInline(admin.StackedInline):
    model = models.Practical


class CourseAdmin(admin.ModelAdmin):
    inlines = (
            TutorialInline,
            PracticalInline,
            )


class TutorialAdmin(admin.ModelAdmin):
    pass


class PracticalAdmin(admin.ModelAdmin):
    pass


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
