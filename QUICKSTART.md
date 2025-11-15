# 🚀 Quick Start Guide - SimpleLMS

## Langkah-Langkah Menjalankan Aplikasi

### 1️⃣ Start Docker Containers
```powershell
cd c:\xampp\htdocs\tugas6\lms-orm-models
docker-compose up -d
```

Tunggu beberapa saat hingga kedua container (lms_app dan lms_db) berjalan.

### 2️⃣ Verifikasi Container Berjalan
```powershell
docker ps
```

Pastikan Anda melihat:
- `lms_app` - Status: Up - Port: 8003
- `lms_db` - Status: Up - Port: 5535

### 3️⃣ Akses Aplikasi

Buka browser dan kunjungi:
```
http://localhost:8003/
```

Anda akan melihat **Dashboard SimpleLMS** dengan:
- Statistik total courses, enrollments, dan materials
- Daftar course terbaru
- Quick action buttons

### 4️⃣ Login ke Admin Panel (Opsional)

Untuk mengakses admin panel:
```
http://localhost:8003/admin/
```

**Kredensial:**
- Username: `admin`
- Password: `admin`

Di admin panel Anda bisa:
- Mengelola users (tambah dosen, mahasiswa)
- Melihat semua data di database
- Melakukan operasi bulk

## 📖 Panduan Penggunaan Fitur

### Membuat Course Baru

1. Dari Dashboard, klik **"Tambah Course Baru"** atau klik menu **"Courses"** → **"Tambah Course"**
2. Isi form:
   - **Kode Mata Kuliah**: Contoh `IF101` (harus unik)
   - **Nama Mata Kuliah**: Contoh `Pemrograman Web`
   - **Deskripsi**: Penjelasan tentang course
   - **SKS**: Jumlah SKS (1-4)
   - **Dosen Pengampu**: Pilih dari dropdown (atau kosongkan)
3. Klik **"Simpan Course"**

### Menambah Materi ke Course

1. Buka detail course (klik nama course dari daftar)
2. Di bagian **"Materi Pembelajaran"**, klik **"Tambah Materi"**
3. Isi form:
   - **Judul Materi**: Contoh `Pertemuan 1: Pengenalan HTML`
   - **Konten Materi**: Isi materi pembelajaran
   - **Urutan Materi**: 1, 2, 3, dst.
4. Klik **"Simpan Materi"**

### Mendaftarkan Mahasiswa (Enrollment)

1. Klik menu **"Enrollments"** → **"Tambah Enrollment"**
2. Isi form:
   - **Mahasiswa**: Pilih username mahasiswa
   - **Mata Kuliah**: Pilih course yang akan diikuti
   - **Nilai**: Kosongkan dulu (bisa diisi nanti)
3. Klik **"Simpan Enrollment"**

### Input Nilai Mahasiswa

1. Buka **"Enrollments"**
2. Cari enrollment yang ingin diberi nilai
3. Klik tombol **Edit** (icon pensil)
4. Isi **Nilai** dengan huruf: A, B, C, D, atau E
5. Klik **"Update Enrollment"**

### Mencari Course

1. Buka halaman **"Courses"**
2. Gunakan search bar di atas daftar courses
3. Ketik kode course, nama, atau kata kunci dari deskripsi
4. Tekan Enter atau klik tombol Search

### Filter Enrollment

1. Buka halaman **"Enrollments"**
2. Gunakan filter:
   - **Cari Mahasiswa**: Ketik username mahasiswa
   - **Filter Course**: Pilih course dari dropdown
3. Klik **"Filter"**

## 🎯 Skenario Penggunaan Lengkap

### Skenario: Setup Course Baru untuk Semester

#### Step 1: Buat User Dosen (via Admin)
```
1. Login ke http://localhost:8003/admin/
2. Klik "Users" → "Add User"
3. Isi username: "dosen_budi"
4. Set password
5. Save
6. Edit lagi, isi First name: "Budi", Last name: "Santoso"
7. Save
```

#### Step 2: Buat Course
```
1. Kembali ke http://localhost:8003/
2. Klik "Tambah Course Baru"
3. Isi:
   - Kode: IF201
   - Nama: Struktur Data
   - Deskripsi: Mempelajari struktur data...
   - SKS: 3
   - Dosen: dosen_budi
4. Simpan
```

#### Step 3: Tambah Materi
```
1. Dari detail course, klik "Tambah Materi"
2. Buat materi pertama:
   - Judul: Pertemuan 1 - Array dan List
   - Konten: Penjelasan array...
   - Order: 1
3. Simpan
4. Ulangi untuk materi berikutnya (order: 2, 3, dst)
```

#### Step 4: Daftarkan Mahasiswa
```
1. Buat user mahasiswa dulu di admin (atau gunakan existing users)
2. Klik menu "Enrollments" → "Tambah Enrollment"
3. Pilih mahasiswa dan course IF201
4. Simpan
5. Ulangi untuk mahasiswa lain
```

#### Step 5: Input Nilai (End of Semester)
```
1. Buka "Enrollments"
2. Edit setiap enrollment
3. Isi nilai: A, B, C, D, atau E
4. Update
```

## 🛑 Stop & Start Aplikasi

### Stop Aplikasi
```powershell
cd c:\xampp\htdocs\tugas6\lms-orm-models
docker-compose down
```

### Start Aplikasi Lagi
```powershell
cd c:\xampp\htdocs\tugas6\lms-orm-models
docker-compose up -d
```

### Restart Hanya Django (jika ada perubahan code)
```powershell
docker restart lms_app
```

## ⚠️ Troubleshooting Cepat

### Aplikasi tidak bisa diakses (Connection Refused)

**Solusi:**
```powershell
# Cek status container
docker ps

# Jika tidak ada, start lagi
docker-compose up -d

# Jika ada tapi masih error, restart
docker restart lms_app
```

### Database error / Data hilang

**Solusi:**
```powershell
# Cek apakah postgres running
docker ps | findstr lms_db

# Restart postgres
docker restart lms_db

# Tunggu 5 detik, lalu restart django
timeout /t 5
docker restart lms_app
```

### Template/CSS tidak berubah

**Solusi:**
```powershell
# Collect static files
docker exec lms_app python manage.py collectstatic --noinput

# Restart container
docker restart lms_app

# Clear browser cache (Ctrl+F5 di browser)
```

### Port sudah digunakan (Port 8003 or 5535 in use)

**Solusi 1 - Gunakan port lain:**
Edit `docker-compose.yml`, ganti:
```yaml
ports:
  - "8004:8003"  # Ganti 8003 ke 8004
```

**Solusi 2 - Stop aplikasi yang menggunakan port tersebut**

## 💡 Tips & Tricks

### Tip 1: Gunakan Admin Panel untuk Bulk Operations
Admin panel Django sangat powerful untuk:
- Import banyak data sekaligus
- Bulk delete
- Filter dan search advanced
- Edit langsung di database

### Tip 2: Backup Database
```powershell
# Export database
docker exec lms_db pg_dump -U postgres lms_db > backup.sql

# Import database
docker exec -i lms_db psql -U postgres lms_db < backup.sql
```

### Tip 3: Lihat Logs untuk Debug
```powershell
# Lihat logs Django
docker logs lms_app

# Lihat logs real-time (Ctrl+C untuk stop)
docker logs -f lms_app
```

### Tip 4: Django Shell untuk Testing
```powershell
docker exec -it lms_app python manage.py shell
```

Kemudian di shell:
```python
from courses.models import Course, Enrollment
# Lihat semua courses
courses = Course.objects.all()
for c in courses:
    print(c.name)
```

## 📞 Bantuan Lebih Lanjut

Jika mengalami masalah:
1. Cek file `README.md` untuk dokumentasi lengkap
2. Lihat logs: `docker logs lms_app`
3. Pastikan Docker Desktop running
4. Cek koneksi database di settings.py
5. Restart semua container: `docker-compose down && docker-compose up -d`

## ✅ Checklist Setup Awal

- [ ] Docker Desktop terinstall dan running
- [ ] Clone/download project ke `c:\xampp\htdocs\tugas6\lms-orm-models`
- [ ] Jalankan `docker-compose up -d`
- [ ] Tunggu hingga kedua container running
- [ ] Akses http://localhost:8003/ di browser
- [ ] Login ke admin panel http://localhost:8003/admin/ (admin/admin)
- [ ] Buat user dosen dan mahasiswa
- [ ] Buat course pertama
- [ ] Tambah material ke course
- [ ] Buat enrollment
- [ ] Test semua fitur CRUD

---

**Selamat menggunakan SimpleLMS! 🎓**
