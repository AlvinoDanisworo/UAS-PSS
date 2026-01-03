from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Course(models.Model):
    """Model untuk menyimpan data mata kuliah"""
    code = models.CharField(max_length=10, unique=True, help_text="Kode mata kuliah")
    name = models.CharField(max_length=200, help_text="Nama mata kuliah")
    description = models.TextField(blank=True, help_text="Deskripsi mata kuliah")
    credits = models.IntegerField(default=3, help_text="Jumlah SKS")
    price = models.IntegerField(default=0, help_text="Harga course")
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='courses_taught')
    instructor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='courses_instructed')
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


class CourseMember(models.Model):
    """Model untuk menyimpan member dari course"""
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_memberships')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='members')
    roles = models.CharField(max_length=50, help_text="Role member (student, instructor, etc)")
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user_id', 'course']
        ordering = ['-joined_at']
        verbose_name = 'Course Member'
        verbose_name_plural = 'Course Members'
    
    def __str__(self):
        return f"{self.user_id.username} - {self.course.name} ({self.roles})"


class CourseContent(models.Model):
    """Model untuk menyimpan konten pembelajaran"""
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='contents')
    name = models.CharField(max_length=200, help_text="Nama konten")
    description = models.TextField(help_text="Deskripsi konten")
    video_url = models.URLField(blank=True, help_text="URL video")
    file_attachment = models.CharField(max_length=500, blank=True, help_text="File attachment path")
    order = models.IntegerField(default=0, help_text="Urutan konten")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = 'Course Content'
        verbose_name_plural = 'Course Contents'
    
    def __str__(self):
        return f"{self.course_id.code} - {self.name}"


class Comment(models.Model):
    """Model untuk menyimpan komentar pada konten"""
    content_id = models.ForeignKey(CourseContent, on_delete=models.CASCADE, related_name='comments')
    member_id = models.ForeignKey(CourseMember, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField(help_text="Isi komentar")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
    
    def __str__(self):
        return f"Comment by {self.member_id.user_id.username} on {self.content_id.name}"
