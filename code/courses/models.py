from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Course(models.Model):
    """Model untuk menyimpan data mata kuliah"""
    code = models.CharField(max_length=10, unique=True, help_text="Kode mata kuliah")
    name = models.CharField(max_length=200, help_text="Nama mata kuliah")
    description = models.TextField(blank=True, help_text="Deskripsi mata kuliah")
    credits = models.IntegerField(default=3, help_text="Jumlah SKS")
    instructor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='courses_taught')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['code']
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class Enrollment(models.Model):
    """Model untuk menyimpan data pendaftaran mahasiswa ke mata kuliah"""
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    grade = models.CharField(max_length=2, blank=True, null=True, help_text="Nilai akhir (A, B, C, D, E)")
    
    class Meta:
        unique_together = ['student', 'course']
        ordering = ['-enrolled_at']
        verbose_name = 'Enrollment'
        verbose_name_plural = 'Enrollments'
    
    def __str__(self):
        return f"{self.student.username} - {self.course.code}"


class Material(models.Model):
    """Model untuk menyimpan materi pembelajaran"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='materials')
    title = models.CharField(max_length=200, help_text="Judul materi")
    content = models.TextField(help_text="Isi materi")
    order = models.IntegerField(default=0, help_text="Urutan materi")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = 'Material'
        verbose_name_plural = 'Materials'
    
    def __str__(self):
        return f"{self.course.code} - {self.title}"
