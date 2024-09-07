from django.contrib import admin
from .models import Teacher, Subject

class TeacherAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'is_active']
    list_filter = ['is_active']

admin.site.register(Teacher, TeacherAdmin)

class SubjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'code']
    search_fields = ['name']

admin.site.register(Subject, SubjectAdmin)
