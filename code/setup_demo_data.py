"""
Script untuk setup demo data SimpleLMS
Jalankan dengan: docker exec -it lms_app python manage.py shell < setup_demo_data.py
"""

from django.contrib.auth.models import User
from courses.models import Course, Material, Enrollment

# Create superuser admin
if not User.objects.filter(username='admin').exists():
    admin = User.objects.create_superuser('admin', 'admin@lms.com', 'admin')
    print("✅ Superuser 'admin' created (password: admin)")
else:
    print("ℹ️  Superuser 'admin' already exists")

# Create instructors
dosen1, created = User.objects.get_or_create(
    username='dosen_andi',
    defaults={
        'first_name': 'Andi',
        'last_name': 'Pratama',
        'email': 'andi@university.edu'
    }
)
if created:
    dosen1.set_password('dosen123')
    dosen1.save()
    print("✅ Dosen 'dosen_andi' created")

dosen2, created = User.objects.get_or_create(
    username='dosen_budi',
    defaults={
        'first_name': 'Budi',
        'last_name': 'Santoso',
        'email': 'budi@university.edu'
    }
)
if created:
    dosen2.set_password('dosen123')
    dosen2.save()
    print("✅ Dosen 'dosen_budi' created")

# Create students
students = []
student_data = [
    ('mahasiswa_andi', 'Andi', 'Wijaya'),
    ('mahasiswa_sari', 'Sari', 'Permata'),
    ('mahasiswa_dewi', 'Dewi', 'Lestari'),
    ('mahasiswa_rudi', 'Rudi', 'Hartono'),
    ('mahasiswa_fitri', 'Fitri', 'Wulandari'),
]

for username, first, last in student_data:
    student, created = User.objects.get_or_create(
        username=username,
        defaults={
            'first_name': first,
            'last_name': last,
            'email': f'{username}@student.edu'
        }
    )
    if created:
        student.set_password('student123')
        student.save()
        print(f"✅ Mahasiswa '{username}' created")
    students.append(student)

# Create courses
courses_data = [
    {
        'code': 'CS101',
        'name': 'Pemrograman Web',
        'description': 'Mempelajari dasar-dasar pemrograman web menggunakan HTML, CSS, JavaScript, dan framework modern',
        'credits': 3,
        'instructor': dosen1
    },
    {
        'code': 'CS201',
        'name': 'Basis Data',
        'description': 'Konsep database relational, SQL, normalisasi, dan manajemen database menggunakan PostgreSQL',
        'credits': 3,
        'instructor': dosen1
    },
    {
        'code': 'CS301',
        'name': 'Algoritma dan Struktur Data',
        'description': 'Mempelajari algoritma fundamental, kompleksitas, sorting, searching, dan struktur data',
        'credits': 4,
        'instructor': dosen2
    },
    {
        'code': 'CS401',
        'name': 'Pemrograman Mobile',
        'description': 'Pengembangan aplikasi mobile untuk Android dan iOS menggunakan React Native',
        'credits': 3,
        'instructor': dosen2
    },
]

courses = []
for data in courses_data:
    course, created = Course.objects.get_or_create(
        code=data['code'],
        defaults=data
    )
    if created:
        print(f"✅ Course '{data['code']} - {data['name']}' created")
    courses.append(course)

# Create materials for each course
materials_data = {
    'CS101': [
        ('Pertemuan 1 - HTML & CSS Basics', 'Pengenalan HTML tags, CSS selectors, box model, dan responsive design', 1),
        ('Pertemuan 2 - JavaScript Fundamentals', 'Variables, data types, functions, dan DOM manipulation', 2),
        ('Pertemuan 3 - Bootstrap Framework', 'Menggunakan Bootstrap untuk responsive web design', 3),
        ('Pertemuan 4 - Django Framework', 'Introduction to Django, MVT pattern, dan ORM', 4),
    ],
    'CS201': [
        ('Pertemuan 1 - SQL Basics', 'SELECT, INSERT, UPDATE, DELETE queries', 1),
        ('Pertemuan 2 - Database Design', 'ER Diagram, normalisasi, dan relasi antar tabel', 2),
        ('Pertemuan 3 - Advanced SQL', 'JOIN, subquery, aggregation, dan indexing', 3),
        ('Pertemuan 4 - PostgreSQL Features', 'Stored procedures, triggers, dan views', 4),
    ],
    'CS301': [
        ('Pertemuan 1 - Pengenalan Algoritma', 'Konsep algoritma, kompleksitas waktu O(n)', 1),
        ('Pertemuan 2 - Sorting Algorithms', 'Bubble sort, insertion sort, merge sort, quick sort', 2),
        ('Pertemuan 3 - Data Structures', 'Array, linked list, stack, queue', 3),
        ('Pertemuan 4 - Trees & Graphs', 'Binary tree, BST, graph traversal (DFS, BFS)', 4),
    ],
    'CS401': [
        ('Pertemuan 1 - React Native Setup', 'Development environment, components, dan props', 1),
        ('Pertemuan 2 - State Management', 'useState, useEffect, dan Context API', 2),
        ('Pertemuan 3 - Navigation', 'React Navigation library dan routing', 3),
        ('Pertemuan 4 - API Integration', 'Fetch data dari REST API, async/await', 4),
    ],
}

for course in courses:
    if course.code in materials_data:
        for title, content, order in materials_data[course.code]:
            material, created = Material.objects.get_or_create(
                course=course,
                order=order,
                defaults={'title': title, 'content': content}
            )
            if created:
                print(f"   ✅ Material '{title}' added to {course.code}")

# Create enrollments with grades
grades = ['A', 'A', 'B', 'B', 'C']
enrollment_count = 0

for i, student in enumerate(students):
    # Each student enrolls in 2-3 courses
    enrolled_courses = courses[:3] if i % 2 == 0 else courses[1:4]
    
    for j, course in enumerate(enrolled_courses):
        enrollment, created = Enrollment.objects.get_or_create(
            student=student,
            course=course,
            defaults={'grade': grades[j % len(grades)]}
        )
        if created:
            enrollment_count += 1

print(f"\n✅ {enrollment_count} enrollments created")

# Summary
print("\n" + "="*60)
print("📊 DEMO DATA SUMMARY")
print("="*60)
print(f"👤 Users: {User.objects.count()} (1 admin, 2 dosen, {len(students)} mahasiswa)")
print(f"📚 Courses: {Course.objects.count()}")
print(f"📄 Materials: {Material.objects.count()}")
print(f"🎓 Enrollments: {Enrollment.objects.count()}")
print("="*60)
print("\n✅ Setup complete!")
print("\n🌐 Akses aplikasi:")
print("   - Web: http://localhost:8003/")
print("   - Admin: http://localhost:8003/admin/")
print("\n🔑 Login credentials:")
print("   - Admin: admin / admin")
print("   - Dosen: dosen_andi / dosen123")
print("   - Mahasiswa: mahasiswa_andi / student123")
print("="*60)
