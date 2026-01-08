# LMS Credentials

## Admin Access
- **Username:** `admin`
- **Password:** `admin123`
- **Email:** admin@lms.com
- **Role:** Superuser (full access)

## Dosen (Instructor) Access
- **Username:** `dosen_andi` atau `dosen_budi`
- **Password:** `dosen123`
- **Role:** Instructor

## Mahasiswa (Student) Access
- **Username:** `mahasiswa_andi`, `mahasiswa_sari`, `mahasiswa_dewi`, `mahasiswa_rudi`, `mahasiswa_fitri`
- **Password:** `student123`
- **Role:** Student

## Available Courses
1. **CS101 - Pemrograman Web** (3 SKS, Rp 500.000)
2. **CS201 - Basis Data** (3 SKS, Rp 600.000)
3. **CS301 - Algoritma dan Struktur Data** (4 SKS, Rp 700.000)
4. **CS401 - Pemrograman Mobile** (3 SKS, Rp 650.000)
5. **CS501 - Machine Learning** (4 SKS, Rp 800.000)
6. **CS601 - Cloud Computing** (3 SKS, Rp 750.000)

## Setup Demo Data
To manually setup demo data, run:
```bash
python manage.py setup_demo
```

This will create:
- Admin user
- 2 Instructors (dosen)
- 5 Students (mahasiswa)
- 6 Courses with materials
- Enrollments and course members
