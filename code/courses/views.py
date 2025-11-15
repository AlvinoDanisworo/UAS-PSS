from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from .models import Course, Enrollment, Material
from .forms import CourseForm, EnrollmentForm, MaterialForm

# Home/Dashboard View
def home(request):
    """Dashboard utama LMS"""
    total_courses = Course.objects.count()
    total_enrollments = Enrollment.objects.count()
    total_materials = Material.objects.count()
    
    recent_courses = Course.objects.all().order_by('-created_at')[:6]
    
    context = {
        'total_courses': total_courses,
        'total_enrollments': total_enrollments,
        'total_materials': total_materials,
        'recent_courses': recent_courses,
    }
    return render(request, 'courses/home.html', context)


# Course Views
def course_list(request):
    """List semua courses dengan search functionality"""
    query = request.GET.get('q', '')
    courses = Course.objects.all()
    
    if query:
        courses = courses.filter(
            Q(code__icontains=query) | 
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )
    
    courses = courses.annotate(enrollment_count=Count('enrollments'))
    
    context = {
        'courses': courses,
        'query': query,
    }
    return render(request, 'courses/course_list.html', context)


def course_detail(request, pk):
    """Detail course dengan materials dan enrollments"""
    course = get_object_or_404(Course, pk=pk)
    materials = course.materials.all()
    enrollments = course.enrollments.select_related('student')[:10]
    
    context = {
        'course': course,
        'materials': materials,
        'enrollments': enrollments,
    }
    return render(request, 'courses/course_detail.html', context)


def course_create(request):
    """Create new course"""
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save()
            messages.success(request, f'Course "{course.name}" berhasil ditambahkan!')
            return redirect('course_detail', pk=course.pk)
    else:
        form = CourseForm()
    
    return render(request, 'courses/course_form.html', {
        'form': form,
        'title': 'Tambah Course Baru'
    })


def course_update(request, pk):
    """Update existing course"""
    course = get_object_or_404(Course, pk=pk)
    
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, f'Course "{course.name}" berhasil diupdate!')
            return redirect('course_detail', pk=course.pk)
    else:
        form = CourseForm(instance=course)
    
    return render(request, 'courses/course_form.html', {
        'form': form,
        'title': f'Edit Course: {course.name}',
        'course': course
    })


def course_delete(request, pk):
    """Delete course"""
    course = get_object_or_404(Course, pk=pk)
    
    if request.method == 'POST':
        course_name = course.name
        course.delete()
        messages.success(request, f'Course "{course_name}" berhasil dihapus!')
        return redirect('course_list')
    
    return render(request, 'courses/course_confirm_delete.html', {'course': course})


# Material Views
def material_create(request, course_pk):
    """Create new material for a course"""
    course = get_object_or_404(Course, pk=course_pk)
    
    if request.method == 'POST':
        form = MaterialForm(request.POST)
        if form.is_valid():
            material = form.save(commit=False)
            material.course = course
            material.save()
            messages.success(request, f'Material "{material.title}" berhasil ditambahkan!')
            return redirect('course_detail', pk=course.pk)
    else:
        form = MaterialForm()
    
    return render(request, 'courses/material_form.html', {
        'form': form,
        'course': course,
        'title': f'Tambah Material untuk {course.name}'
    })


def material_update(request, pk):
    """Update existing material"""
    material = get_object_or_404(Material, pk=pk)
    
    if request.method == 'POST':
        form = MaterialForm(request.POST, instance=material)
        if form.is_valid():
            form.save()
            messages.success(request, f'Material "{material.title}" berhasil diupdate!')
            return redirect('course_detail', pk=material.course.pk)
    else:
        form = MaterialForm(instance=material)
    
    return render(request, 'courses/material_form.html', {
        'form': form,
        'course': material.course,
        'title': f'Edit Material: {material.title}',
        'material': material
    })


def material_delete(request, pk):
    """Delete material"""
    material = get_object_or_404(Material, pk=pk)
    course = material.course
    
    if request.method == 'POST':
        material_title = material.title
        material.delete()
        messages.success(request, f'Material "{material_title}" berhasil dihapus!')
        return redirect('course_detail', pk=course.pk)
    
    return render(request, 'courses/material_confirm_delete.html', {
        'material': material,
        'course': course
    })


# Enrollment Views
def enrollment_list(request):
    """List all enrollments"""
    enrollments = Enrollment.objects.select_related('student', 'course').all()
    all_courses = Course.objects.all()
    
    # Filter by student search
    student_query = request.GET.get('student', '')
    if student_query:
        enrollments = enrollments.filter(student__username__icontains=student_query)
    
    # Filter by course
    course_filter = request.GET.get('course', '')
    if course_filter:
        enrollments = enrollments.filter(course__pk=course_filter)
    
    context = {
        'enrollments': enrollments,
        'all_courses': all_courses,
    }
    return render(request, 'courses/enrollment_list.html', context)


def enrollment_create(request):
    """Create new enrollment"""
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            enrollment = form.save()
            messages.success(request, f'Enrollment untuk {enrollment.student.username} di course {enrollment.course.code} berhasil ditambahkan!')
            return redirect('enrollment_list')
    else:
        form = EnrollmentForm()
    
    return render(request, 'courses/enrollment_form.html', {
        'form': form,
        'title': 'Tambah Enrollment Baru'
    })


def enrollment_update(request, pk):
    """Update enrollment (mainly for grading)"""
    enrollment = get_object_or_404(Enrollment, pk=pk)
    
    if request.method == 'POST':
        form = EnrollmentForm(request.POST, instance=enrollment)
        if form.is_valid():
            form.save()
            messages.success(request, f'Enrollment berhasil diupdate!')
            return redirect('enrollment_list')
    else:
        form = EnrollmentForm(instance=enrollment)
    
    return render(request, 'courses/enrollment_form.html', {
        'form': form,
        'title': f'Edit Enrollment: {enrollment.student.username} - {enrollment.course.code}',
        'enrollment': enrollment
    })


def enrollment_delete(request, pk):
    """Delete enrollment"""
    enrollment = get_object_or_404(Enrollment, pk=pk)
    
    if request.method == 'POST':
        enrollment.delete()
        messages.success(request, 'Enrollment berhasil dihapus!')
        return redirect('enrollment_list')
    
    return render(request, 'courses/enrollment_confirm_delete.html', {'enrollment': enrollment})
