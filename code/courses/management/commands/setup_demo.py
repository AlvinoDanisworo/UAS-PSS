from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from courses.models import Course, Material, Enrollment, CourseMember, CourseContent, Comment


class Command(BaseCommand):
    help = 'Setup demo data untuk SimpleLMS'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Setting up demo data...\n'))

        # Create superuser admin
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser('admin', 'admin@lms.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('✅ Superuser "admin" created'))
            self.stdout.write(self.style.WARNING('   Username: admin'))
            self.stdout.write(self.style.WARNING('   Password: admin123'))
        else:
            admin = User.objects.get(username='admin')
            self.stdout.write(self.style.SUCCESS('ℹ️  Superuser "admin" already exists'))
            self.stdout.write(self.style.WARNING('   Username: admin'))
            self.stdout.write(self.style.WARNING('   Password: admin123'))

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
            self.stdout.write(self.style.SUCCESS('✅ Dosen "dosen_andi" created (password: dosen123)'))

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
            self.stdout.write(self.style.SUCCESS('✅ Dosen "dosen_budi" created (password: dosen123)'))

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
                self.stdout.write(self.style.SUCCESS(f'✅ Mahasiswa "{username}" created (password: student123)'))
            students.append(student)

        # Create courses
        courses_data = [
            {
                'code': 'CS101',
                'name': 'Pemrograman Web',
                'description': 'Mempelajari dasar-dasar pemrograman web menggunakan HTML, CSS, JavaScript, dan framework modern seperti Django dan React',
                'credits': 3,
                'price': 500000,
                'instructor': dosen1,
                'teacher': dosen1
            },
            {
                'code': 'CS201',
                'name': 'Basis Data',
                'description': 'Konsep database relational, SQL, normalisasi, dan manajemen database menggunakan PostgreSQL dan MySQL',
                'credits': 3,
                'price': 600000,
                'instructor': dosen1,
                'teacher': dosen1
            },
            {
                'code': 'CS301',
                'name': 'Algoritma dan Struktur Data',
                'description': 'Mempelajari algoritma fundamental, kompleksitas waktu, sorting, searching, dan struktur data seperti tree, graph, stack, queue',
                'credits': 4,
                'price': 700000,
                'instructor': dosen2,
                'teacher': dosen2
            },
            {
                'code': 'CS401',
                'name': 'Pemrograman Mobile',
                'description': 'Pengembangan aplikasi mobile untuk Android dan iOS menggunakan React Native dan Flutter',
                'credits': 3,
                'price': 650000,
                'instructor': dosen2,
                'teacher': dosen2
            },
            {
                'code': 'CS501',
                'name': 'Machine Learning',
                'description': 'Pengenalan machine learning, supervised/unsupervised learning, neural networks, dan deep learning dengan Python',
                'credits': 4,
                'price': 800000,
                'instructor': dosen1,
                'teacher': dosen1
            },
            {
                'code': 'CS601',
                'name': 'Cloud Computing',
                'description': 'Konsep cloud computing, deployment di AWS, Azure, Google Cloud, Docker, dan Kubernetes',
                'credits': 3,
                'price': 750000,
                'instructor': dosen2,
                'teacher': dosen2
            },
        ]

        courses = []
        for data in courses_data:
            course, created = Course.objects.get_or_create(
                code=data['code'],
                defaults=data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✅ Course "{data["code"]} - {data["name"]}" created'))
            courses.append(course)

        # Create materials for each course
        materials_data = {
            'CS101': [
                ('Pertemuan 1 - HTML & CSS Basics', 'Pengenalan HTML tags, CSS selectors, box model, dan responsive design', 1),
                ('Pertemuan 2 - JavaScript Fundamentals', 'Variables, data types, functions, dan DOM manipulation', 2),
                ('Pertemuan 3 - Bootstrap Framework', 'Menggunakan Bootstrap untuk responsive web design', 3),
                ('Pertemuan 4 - Django Framework', 'Introduction to Django, MVT pattern, dan ORM', 4),
                ('Pertemuan 5 - React Basics', 'Components, props, state, dan hooks', 5),
            ],
            'CS201': [
                ('Pertemuan 1 - SQL Basics', 'SELECT, INSERT, UPDATE, DELETE queries', 1),
                ('Pertemuan 2 - Database Design', 'ER Diagram, normalisasi, dan relasi antar tabel', 2),
                ('Pertemuan 3 - Advanced SQL', 'JOIN, subquery, aggregation, dan indexing', 3),
                ('Pertemuan 4 - PostgreSQL Features', 'Stored procedures, triggers, dan views', 4),
                ('Pertemuan 5 - NoSQL Databases', 'MongoDB, Redis, dan use cases', 5),
            ],
            'CS301': [
                ('Pertemuan 1 - Pengenalan Algoritma', 'Konsep algoritma, kompleksitas waktu O(n)', 1),
                ('Pertemuan 2 - Sorting Algorithms', 'Bubble sort, insertion sort, merge sort, quick sort', 2),
                ('Pertemuan 3 - Data Structures', 'Array, linked list, stack, queue', 3),
                ('Pertemuan 4 - Trees & Graphs', 'Binary tree, BST, graph traversal (DFS, BFS)', 4),
                ('Pertemuan 5 - Dynamic Programming', 'Memoization, tabulation, dan optimization problems', 5),
            ],
            'CS401': [
                ('Pertemuan 1 - React Native Setup', 'Development environment, components, dan props', 1),
                ('Pertemuan 2 - State Management', 'useState, useEffect, dan Context API', 2),
                ('Pertemuan 3 - Navigation', 'React Navigation library dan routing', 3),
                ('Pertemuan 4 - API Integration', 'Fetch data dari REST API, async/await', 4),
                ('Pertemuan 5 - Native Modules', 'Camera, geolocation, dan push notifications', 5),
            ],
            'CS501': [
                ('Pertemuan 1 - Python for ML', 'NumPy, Pandas, Matplotlib basics', 1),
                ('Pertemuan 2 - Supervised Learning', 'Linear regression, logistic regression, decision trees', 2),
                ('Pertemuan 3 - Unsupervised Learning', 'K-means clustering, PCA, anomaly detection', 3),
                ('Pertemuan 4 - Neural Networks', 'Perceptron, backpropagation, activation functions', 4),
                ('Pertemuan 5 - Deep Learning', 'CNN, RNN, LSTM dengan TensorFlow dan PyTorch', 5),
            ],
            'CS601': [
                ('Pertemuan 1 - Cloud Fundamentals', 'IaaS, PaaS, SaaS, dan cloud providers', 1),
                ('Pertemuan 2 - Docker Containers', 'Dockerfile, images, containers, dan Docker Compose', 2),
                ('Pertemuan 3 - Kubernetes', 'Pods, deployments, services, dan orchestration', 3),
                ('Pertemuan 4 - CI/CD Pipelines', 'GitHub Actions, Jenkins, automated deployment', 4),
                ('Pertemuan 5 - Cloud Security', 'IAM, encryption, monitoring, dan best practices', 5),
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
                        self.stdout.write(f'   ✅ Material "{title}" added to {course.code}')

        # Create enrollments with grades
        grades = ['A', 'A-', 'B+', 'B', 'C']
        enrollment_count = 0

        for i, student in enumerate(students):
            # Each student enrolls in 3-4 courses
            enrolled_courses = courses[:4] if i % 2 == 0 else courses[2:6]
            
            for j, course in enumerate(enrolled_courses):
                enrollment, created = Enrollment.objects.get_or_create(
                    student=student,
                    course=course,
                    defaults={'grade': grades[j % len(grades)]}
                )
                if created:
                    enrollment_count += 1

        self.stdout.write(self.style.SUCCESS(f'\n✅ {enrollment_count} enrollments created'))

        # Create Course Members
        member_count = 0
        for course in courses:
            # Add instructor as member
            member, created = CourseMember.objects.get_or_create(
                user_id=course.instructor,
                course=course,
                defaults={'roles': 'instructor'}
            )
            if created:
                member_count += 1
            
            # Add enrolled students as members
            enrollments = Enrollment.objects.filter(course=course)
            for enrollment in enrollments:
                member, created = CourseMember.objects.get_or_create(
                    user_id=enrollment.student,
                    course=course,
                    defaults={'roles': 'student'}
                )
                if created:
                    member_count += 1

        self.stdout.write(self.style.SUCCESS(f'✅ {member_count} course members created'))

        # Summary
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('Demo data setup completed!\n'))
        self.stdout.write(self.style.WARNING('Admin Credentials:'))
        self.stdout.write(self.style.WARNING('  Username: admin'))
        self.stdout.write(self.style.WARNING('  Password: admin123\n'))
        self.stdout.write(self.style.WARNING('Dosen Credentials:'))
        self.stdout.write(self.style.WARNING('  Username: dosen_andi / dosen_budi'))
        self.stdout.write(self.style.WARNING('  Password: dosen123\n'))
        self.stdout.write(self.style.WARNING('Student Credentials:'))
        self.stdout.write(self.style.WARNING('  Username: mahasiswa_andi / mahasiswa_sari / etc'))
        self.stdout.write(self.style.WARNING('  Password: student123'))
        self.stdout.write(self.style.SUCCESS('='*60))
