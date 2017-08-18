'''Representation of the models in the admin interface'''

from django.contrib import admin
from apps.api import models


class InstructorAdmin(admin.ModelAdmin):
    '''Adds instructor model to the admin interface

    list_display: shows the columns that are present in the intructor interface
    search_fields: shows the columns that can be searched for
    ordering: how the information is sorted
    '''
    list_display = ['last_name', 'first_name', 'university_id', 'email']
    search_fields = ['last_name', 'first_name', 'university_id', 'email']
    ordering = ['last_name']


class TeachingAssistantAdmin(admin.ModelAdmin):
    '''Adds teaching assistant model to the admin interface

    list_display: shows the columns that are present in the teaching assistant
        interface
    search_fields: shows the columns that can be searched for
    ordering: how the information is sorted
    '''
    list_display = ['last_name', 'first_name', 'university_id', 'email']
    search_fields = ['last_name', 'first_name', 'university_id', 'email']
    ordering = ['last_name']


class IdentificationInline(admin.StackedInline):
    '''Making it StackedInline means that this interface can also be
    edited by other interfaces
    '''
    model = models.Identification

class IdentificationAdmin(admin.ModelAdmin):
    '''Adds identitfication model to the admin interface
    '''
    pass

class TAidEventAdmin(admin.ModelAdmin):
    '''Adds event model to the admin interface

    exclude: takes away those fields from the interface
    '''
    exclude = ('creator', 'description')


class StudentAdmin(admin.ModelAdmin):
    '''Adds student model to the admin interface

    list_display: shows the columns that are present in the student interface
    search_fields: shows the columns that can be searched for
    ordering: how the information is sorted
    inlines: models other than this that can be edited in this interface
    '''
    list_display = ['last_name', 'first_name',
                    'university_id', 'student_number', 'email']
    search_fields = ['last_name', 'first_name',
                     'university_id', 'student_number', 'email']
    ordering = ['last_name']
    inlines = (
        IdentificationInline,
    )


class TutorialInline(admin.StackedInline):
    '''Making it StackedInline means that this interface can also be
    edited by other interfaces
    '''
    model = models.Tutorial

class TutorialAdmin(admin.ModelAdmin):
    '''Adds tutorial model to the admin interface
    '''
    pass


class PracticalInline(admin.StackedInline):
    '''Making it StackedInline means that this interface can also be
    edited by other interfaces
    '''
    model = models.Practical


class LectureAdmin(admin.ModelAdmin):
    '''Adds lecture model to the admin interface
    '''
    pass


class PracticalAdmin(admin.ModelAdmin):
    '''Adds practical model to the admin interface
    '''
    pass


class MarkAdmin(admin.ModelAdmin):
    '''Adds mark model to the admin interface
    '''
    pass


class MarkInline(admin.StackedInline):
    '''Making it StackedInline means that this interface can also be
    edited by other interfaces
    '''
    model = models.Mark


class RubricInline(admin.StackedInline):
    '''Making it StackedInline means that this interface can also be
    edited by other interfaces
    '''
    model = models.Rubric


class AssignmentAdmin(admin.ModelAdmin):
    '''Adds assignment model to the admin interface

    inlines: models other than this that can be edited in this interface
    '''
    inlines = (
        RubricInline,
    )


class RubricAdmin(admin.ModelAdmin):
    '''Adds rubric model to the admin interface

    inlines: models other than this that can be edited in this interface
    '''
    inlines = (
        MarkInline,
    )


class StudentListFileAdmin(admin.ModelAdmin):
    '''Adds student list file model to the admin interface
    '''
    pass


class EnrollmentListFileAdmin(admin.ModelAdmin):
    '''Adds enrollment list file model to the admin interface
    '''
    pass


class MarkFileAdmin(admin.ModelAdmin):
    '''Adds mark file model to the admin interface
    '''
    pass


class TAListAdmin(admin.ModelAdmin):
    '''Adds ta list model to the admin interface
    '''
    pass


# maps all the models to its corresponding admin functions to create admin page
admin.site.register(models.Instructor, InstructorAdmin)
admin.site.register(models.TeachingAssistant, TeachingAssistantAdmin)
admin.site.register(models.Student, StudentAdmin)
admin.site.register(models.Identification, IdentificationAdmin)
admin.site.register(models.Lecture, LectureAdmin)
admin.site.register(models.Tutorial, TutorialAdmin)
admin.site.register(models.Practical, PracticalAdmin)
admin.site.register(models.Mark, MarkAdmin)
admin.site.register(models.Assignment, AssignmentAdmin)
admin.site.register(models.TaidEvent, TAidEventAdmin)
admin.site.register(models.Rubric, RubricAdmin)
admin.site.register(models.StudentListFile, StudentListFileAdmin)
admin.site.register(models.EnrollmentListFile, EnrollmentListFileAdmin)
admin.site.register(models.MarkFile, MarkFileAdmin)
admin.site.register(models.TAListFile, TAListAdmin)
