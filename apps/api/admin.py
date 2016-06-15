from django.contrib import admin
from apps.api import models


class InstructorAdmin(admin.ModelAdmin):
    pass


class TeachingAssistantAdmin(admin.ModelAdmin):
    pass


class IdentificationInline(admin.StackedInline):
    model = models.Identification


class StudentAdmin(admin.ModelAdmin):
    inlines = (
        IdentificationInline,
    )


class IdentificationAdmin(admin.ModelAdmin):
    pass


class TutorialInline(admin.StackedInline):
    model = models.Tutorial


class PracticalInline(admin.StackedInline):
    model = models.Practical


class LectureAdmin(admin.ModelAdmin):
    pass


class TutorialAdmin(admin.ModelAdmin):
    pass


class PracticalAdmin(admin.ModelAdmin):
    pass

class MarkAdmin(admin.ModelAdmin):
    pass


class MarkInline(admin.StackedInline):
    model = models.Mark


class RubricInline(admin.StackedInline):
    model = models.Rubric


class AssignmentAdmin(admin.ModelAdmin):
    inlines = (
            RubricInline,
            )


class RubricAdmin(admin.ModelAdmin):
    model = models.Rubric
    inlines = (
            MarkInline,
            )


class StudentListFileAdmin(admin.ModelAdmin):
    pass


class EnrollmentListFileAdmin(admin.ModelAdmin):
    pass


class MarkFileAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Instructor, InstructorAdmin)
admin.site.register(models.TeachingAssistant, TeachingAssistantAdmin)
admin.site.register(models.Student, StudentAdmin)
admin.site.register(models.Identification, IdentificationAdmin)
admin.site.register(models.Lecture, LectureAdmin)
admin.site.register(models.Tutorial, TutorialAdmin)
admin.site.register(models.Practical, PracticalAdmin)
admin.site.register(models.Mark, MarkAdmin)
admin.site.register(models.Assignment, AssignmentAdmin)
admin.site.register(models.Rubric, RubricAdmin)
admin.site.register(models.StudentListFile, StudentListFileAdmin)
admin.site.register(models.EnrollmentListFile, StudentListFileAdmin)
admin.site.register(models.MarkFile, StudentListFileAdmin)
