from django.contrib import admin
from .models import Course, Enrollment, Material

# Register your models here.

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'credits', 'instructor', 'created_at']
    list_filter = ['credits', 'created_at']
    search_fields = ['code', 'name', 'description']
    

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'grade', 'enrolled_at']
    list_filter = ['grade', 'enrolled_at']
    search_fields = ['student__username', 'course__code', 'course__name']


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['course', 'title', 'order', 'created_at']
    list_filter = ['course', 'created_at']
    search_fields = ['title', 'content', 'course__code']
