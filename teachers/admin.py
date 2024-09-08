from django.contrib import admin
from accounts.models import Teacher, Subject

class TeacherAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_email', 'user_name', 'hourly_price']
    search_fields = ['user__email', 'user__name']
    list_filter = ['hourly_price']

    def user_email(self, obj):
        return obj.user.email
    user_email.admin_order_field = 'user__email'  # Permite ordenar por este campo no admin
    user_email.short_description = 'Email'

    def user_name(self, obj):
        return obj.user.name
    user_name.admin_order_field = 'user__name'  # Permite ordenar por este campo no admin
    user_name.short_description = 'Name'

class SubjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']

admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Subject, SubjectAdmin)
