from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Category, Project, ProjectImage, Feedback, User

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    # design_loc ko display mein add kiya
    list_display = ('title', 'design_loc', 'design_type', 'interior_or_exterior')
    # Filters add kiye taaki admin panel easy ho jaye
    list_filter = ('design_type', 'interior_or_exterior', 'design_loc')
    filter_horizontal = ('categories',)
    search_fields = ('title', 'design_loc')
admin.site.register(Category)
admin.site.register(Feedback)
admin.site.register(ProjectImage)

class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets + ((None, {'fields': ('role',)}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {'fields': ('role',)}),)

admin.site.register(User, CustomUserAdmin)