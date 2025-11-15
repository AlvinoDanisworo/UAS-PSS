# SimpleLMS - Learning Management System

## 📚 Deskripsi Proyek
SimpleLMS adalah sistem manajemen pembelajaran (Learning Management System) yang dibangun menggunakan Django dan PostgreSQL dengan Docker. Sistem ini memungkinkan pengelolaan mata kuliah, materi pembelajaran, dan enrollment mahasiswa dengan antarmuka yang modern dan responsif.

## ✨ Fitur Utama

### 1. Dashboard
- Statistik total courses, enrollments, dan materials
- Daftar course terbaru
- Quick actions untuk navigasi cepat

### 2. Manajemen Course
- **List Courses**: Tampilan semua mata kuliah dengan fungsi pencarian
- **Detail Course**: Informasi lengkap course, daftar materi, dan mahasiswa terdaftar
- **Create Course**: Tambah mata kuliah baru
- **Edit Course**: Update informasi course
- **Delete Course**: Hapus course dengan konfirmasi

### 3. Manajemen Material
- **Create Material**: Tambah materi pembelajaran untuk setiap course
- **Edit Material**: Update materi yang sudah ada
- **Delete Material**: Hapus materi dengan konfirmasi
- Sorting materi berdasarkan urutan (order)

### 4. Manajemen Enrollment
- **List Enrollments**: Daftar semua enrollment dengan filter
- **Create Enrollment**: Daftarkan mahasiswa ke course
- **Update Enrollment**: Edit enrollment dan input nilai
- **Delete Enrollment**: Hapus enrollment dengan konfirmasi
- Filter berdasarkan mahasiswa dan course
- Sistem penilaian (A, B, C, D, E)

## 🛠️ Teknologi yang Digunakan

### Backend
- **Django 5.2.7**: Web framework Python
- **PostgreSQL (latest)**: Database relational
- **psycopg2-binary**: PostgreSQL adapter untuk Python

### Frontend
- **Bootstrap 5.3.0**: CSS framework untuk UI responsif
- **Bootstrap Icons**: Icon library
- **Google Fonts (Inter)**: Typography modern
- **Custom CSS**: Styling tambahan dengan gradient, hover effects, dan animasi

### DevOps
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **Python 3.14**: Runtime environment

## 📂 Struktur Proyek

```
lms-orm-models/
├── docker-compose.yml          # Konfigurasi Docker services
├── dockerfile                   # Django container definition
└── code/                        # Django project root
    ├── lms_project/            # Project settings
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── courses/                # Main app
    │   ├── models.py           # Course, Material, Enrollment models
    │   ├── views.py            # CRUD views
    │   ├── forms.py            # Django forms dengan Bootstrap
    │   ├── urls.py             # URL routing
    │   ├── admin.py            # Admin panel config
    │   └── templates/          # HTML templates
    │       ├── base.html       # Base template
    │       └── courses/
    │           ├── home.html
    │           ├── course_list.html
    │           ├── course_detail.html
    │           ├── course_form.html
    │           ├── course_confirm_delete.html
    │           ├── material_form.html
    │           ├── material_confirm_delete.html
    │           ├── enrollment_list.html
    │           ├── enrollment_form.html
    │           └── enrollment_confirm_delete.html
    ├── static/                 # Static files
    │   └── css/
    │       └── custom.css      # Custom styling
    └── manage.py
```

## 🗄️ Database Schema

### Course Model
```python
- code (CharField, max 10, unique)
- name (CharField, max 200)
- description (TextField, optional)
- credits (PositiveIntegerField)
- instructor (ForeignKey to User, optional)
- created_at (DateTimeField, auto)
- updated_at (DateTimeField, auto)
```

### Material Model
```python
- course (ForeignKey to Course)
- title (CharField, max 200)
- content (TextField)
- order (PositiveIntegerField)
- created_at (DateTimeField, auto)
- updated_at (DateTimeField, auto)
```

### Enrollment Model
```python
- student (ForeignKey to User)
- course (ForeignKey to Course)
- enrolled_at (DateTimeField, auto)
- grade (CharField, max 2, optional)
- unique_together: (student, course)
```

## 🚀 Cara Menjalankan

### 1. Start Docker Containers
```bash
cd c:\xampp\htdocs\tugas6\lms-orm-models
docker-compose up -d
```

### 2. Akses Aplikasi
- **Web Interface**: http://localhost:8003/
- **Admin Panel**: http://localhost:8003/admin/
  - Username: `admin`
  - Password: `admin`

### 3. Database Connection
- **Host**: localhost
- **Port**: 5535
- **Database**: lms_db
- **Username**: postgres
- **Password**: postgres

## 📋 Perintah Penting

### Docker Commands
```bash
# Lihat container yang berjalan
docker ps

# Stop containers
docker-compose down

# Restart Django container
docker restart lms_app

# Lihat logs
docker logs lms_app
docker logs lms_db
```

### Django Commands (via Docker)
```bash
# Buat migrations
docker exec lms_app python manage.py makemigrations

# Apply migrations
docker exec lms_app python manage.py migrate

# Buat superuser
docker exec -it lms_app python manage.py createsuperuser

# Collect static files
docker exec lms_app python manage.py collectstatic --noinput

# Django shell
docker exec -it lms_app python manage.py shell
```

## 🎨 Fitur UI/UX

### Design Features
- **Responsive Design**: Otomatis menyesuaikan di desktop, tablet, dan mobile
- **Modern UI**: Menggunakan Bootstrap 5 dengan custom styling
- **Color Scheme**: Gradient backgrounds dengan warna primary (#667eea - #764ba2)
- **Icons**: Bootstrap Icons untuk visual yang lebih baik
- **Hover Effects**: Smooth transitions dan lift effects pada cards
- **Search & Filter**: Pencarian dan filtering untuk kemudahan navigasi

### Custom CSS Features
- Gradient backgrounds untuk buttons dan headers
- Card hover lift effects
- Custom scrollbar styling
- Smooth page transitions
- Responsive tables
- Form styling dengan focus effects
- Badge color coding untuk grades
- Print-friendly styles

## 📱 Navigasi Menu

### Main Navigation
1. **Home**: Dashboard dengan statistik
2. **Courses**: Manajemen mata kuliah
3. **Enrollments**: Manajemen enrollment mahasiswa
4. **Admin** (jika login): Akses Django admin panel

### Quick Actions (Dashboard)
- Tambah Course Baru
- Lihat Semua Courses
- Kelola Enrollments

## 🔐 Authentication

Saat ini sistem menggunakan Django User model default. Untuk mengakses:
- Admin panel memerlukan login (admin/admin)
- User reguler dapat ditambahkan melalui admin panel
- Authentication dapat ditambahkan ke views dengan decorator `@login_required`

## 📊 Fitur Statistik

Dashboard menampilkan:
- Total Courses yang tersedia
- Total Enrollments mahasiswa
- Total Materials pembelajaran
- 6 Course terbaru dengan informasi enrollment

## 🎓 Use Cases

### Untuk Dosen/Instructor:
1. Membuat course baru
2. Menambah materi pembelajaran
3. Melihat daftar mahasiswa yang terdaftar
4. Input/update nilai mahasiswa

### Untuk Admin:
1. Mengelola semua courses
2. Mendaftarkan mahasiswa ke course
3. Monitoring enrollments
4. Mengelola user (dosen & mahasiswa)

## 🔧 Troubleshooting

### Container tidak bisa start
```bash
# Hapus container dan volume lama
docker-compose down -v
docker-compose up -d
```

### Database connection refused
```bash
# Pastikan postgres container running
docker ps

# Restart containers
docker restart lms_db
docker restart lms_app
```

### Static files tidak muncul
```bash
# Collect static files lagi
docker exec lms_app python manage.py collectstatic --noinput
```

### Template tidak berubah
```bash
# Restart Django container
docker restart lms_app
```

## 📝 Notes

### PostgreSQL Version Compatibility
- PostgreSQL 18+ menggunakan `/var/lib/postgresql` sebagai volume mount
- Versi sebelumnya menggunakan `/var/lib/postgresql/data`
- Docker-compose.yml sudah dikonfigurasi untuk PostgreSQL 18+

### Development vs Production
Konfigurasi ini untuk development. Untuk production:
- Set `DEBUG = False` di settings.py
- Gunakan secret key yang aman
- Configure proper ALLOWED_HOSTS
- Gunakan environment variables untuk credentials
- Setup proper HTTPS/SSL
- Configure static files serving (nginx/whitenoise)

## 🎯 Future Enhancements

Fitur yang bisa ditambahkan:
- User authentication & authorization yang lebih robust
- Role-based access (student, instructor, admin)
- File upload untuk materials (PDF, PPT, video)
- Quiz & assignment system
- Attendance tracking
- Email notifications
- Student dashboard
- Course ratings & reviews
- Discussion forum
- Calendar integration
- Report generation (transcript, certificate)

## 📄 License

This project is created for educational purposes.

## 👥 Credits

- Bootstrap 5 - https://getbootstrap.com/
- Bootstrap Icons - https://icons.getbootstrap.com/
- Google Fonts - https://fonts.google.com/
- Django - https://www.djangoproject.com/
- PostgreSQL - https://www.postgresql.org/

---

**Dibuat dengan ❤️ mengikuti tutorial PDF dengan tampilan yang lebih modern dan fitur yang lebih lengkap**
