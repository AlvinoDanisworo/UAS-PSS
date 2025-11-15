from django import forms
from .models import Course, Enrollment, Material


class CourseForm(forms.ModelForm):
    """Form untuk Create dan Update Course"""
    
    class Meta:
        model = Course
        fields = ['code', 'name', 'description', 'credits', 'instructor']
        widgets = {
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contoh: CS101'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nama mata kuliah'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Deskripsi mata kuliah...'
            }),
            'credits': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 6
            }),
            'instructor': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
        labels = {
            'code': 'Kode Mata Kuliah',
            'name': 'Nama Mata Kuliah',
            'description': 'Deskripsi',
            'credits': 'SKS',
            'instructor': 'Dosen Pengampu',
        }


class MaterialForm(forms.ModelForm):
    """Form untuk Create dan Update Material"""
    
    class Meta:
        model = Material
        fields = ['title', 'content', 'order']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Judul materi'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': 'Isi materi pembelajaran...'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'value': 0
            }),
        }
        labels = {
            'title': 'Judul Materi',
            'content': 'Isi Materi',
            'order': 'Urutan',
        }


class EnrollmentForm(forms.ModelForm):
    """Form untuk Create dan Update Enrollment"""
    
    class Meta:
        model = Enrollment
        fields = ['student', 'course', 'grade']
        widgets = {
            'student': forms.Select(attrs={
                'class': 'form-control'
            }),
            'course': forms.Select(attrs={
                'class': 'form-control'
            }),
            'grade': forms.Select(attrs={
                'class': 'form-control'
            }, choices=[
                ('', '-- Pilih Nilai --'),
                ('A', 'A'),
                ('B', 'B'),
                ('C', 'C'),
                ('D', 'D'),
                ('E', 'E'),
            ]),
        }
        labels = {
            'student': 'Mahasiswa',
            'course': 'Mata Kuliah',
            'grade': 'Nilai',
        }
