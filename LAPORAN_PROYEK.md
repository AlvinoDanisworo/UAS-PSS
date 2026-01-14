# LAPORAN PROYEK PERANGKAT LUNAK
# SISTEM MANAJEMEN PEMBELAJARAN BERBASIS WEB

---

**Program Studi Teknik Informatika**  
**Universitas**  
**Tahun 2026**

---

## BAB I  
## PENDAHULUAN

### 1.1 Latar Belakang

Perkembangan teknologi informasi telah memberikan dampak signifikan terhadap dunia pendidikan, khususnya dalam proses pembelajaran dan pengelolaan mata kuliah. Institusi pendidikan tinggi memerlukan sistem yang dapat memfasilitasi interaksi antara pengajar dan mahasiswa, mengelola materi pembelajaran, serta memantau progres akademik secara terstruktur dan efisien.

Dalam konteks pembelajaran jarak jauh maupun hybrid learning, kebutuhan akan platform digital yang dapat mengorganisir mata kuliah, materi pembelajaran, dan data enrollment mahasiswa menjadi semakin mendesak. Sistem konvensional yang masih mengandalkan proses manual cenderung tidak efisien, rentan terhadap kesalahan pencatatan, dan sulit dalam melakukan monitoring secara real-time.

Berdasarkan permasalahan tersebut, diperlukan sebuah sistem manajemen pembelajaran berbasis web yang mampu mengintegrasikan seluruh aspek pengelolaan pembelajaran dalam satu platform terpadu. Sistem ini dirancang untuk memberikan kemudahan akses bagi pengajar dalam mengelola mata kuliah dan materi, serta bagi mahasiswa dalam mengakses konten pembelajaran dan melakukan enrollment.

Pengembangan sistem ini menggunakan pendekatan modern dengan memanfaatkan teknologi web framework Django, database relasional PostgreSQL, serta Application Programming Interface (API) berbasis REST untuk memastikan skalabilitas, keamanan, dan kemudahan integrasi dengan sistem lain di masa mendatang.

### 1.2 Rumusan Masalah

Berdasarkan latar belakang yang telah diuraikan, rumusan masalah dalam pengembangan sistem ini adalah sebagai berikut:

1. Bagaimana merancang dan mengimplementasikan sistem manajemen pembelajaran yang dapat mengelola data mata kuliah, materi pembelajaran, dan enrollment mahasiswa secara terintegrasi?
2. Bagaimana membangun arsitektur sistem yang scalable dan maintainable dengan memisahkan layer backend API dan frontend interface?
3. Bagaimana mengimplementasikan mekanisme autentikasi dan otorisasi yang aman menggunakan JSON Web Token (JWT)?
4. Bagaimana merancang struktur basis data yang optimal untuk mendukung relasi antar entitas seperti course, material, enrollment, dan user?
5. Bagaimana melakukan deployment sistem ke platform cloud agar dapat diakses secara publik dengan performa yang stabil?

### 1.3 Tujuan Pengembangan Sistem

Tujuan yang ingin dicapai dari pengembangan sistem ini adalah:

1. Menghasilkan sistem manajemen pembelajaran berbasis web yang dapat mengelola data mata kuliah, materi pembelajaran, dan enrollment mahasiswa secara efisien dan terintegrasi.
2. Membangun arsitektur aplikasi yang modular dengan pemisahan concern antara backend API dan frontend interface untuk memudahkan pengembangan dan pemeliharaan sistem.
3. Mengimplementasikan sistem keamanan berbasis JWT untuk autentikasi dan otorisasi pengguna yang robust dan sesuai standar industri.
4. Merancang dan mengimplementasikan skema basis data relasional yang optimal dengan mempertimbangkan normalisasi, integritas referensial, dan performa query.
5. Melakukan deployment aplikasi ke platform cloud (Railway) sehingga sistem dapat diakses secara global dengan availability dan reliability yang tinggi.

### 1.4 Manfaat Pengembangan Sistem

Pengembangan sistem ini memberikan manfaat bagi berbagai pihak sebagai berikut:

**Bagi Pengajar:**
1. Memudahkan pengelolaan mata kuliah, termasuk membuat, mengubah, dan menghapus data course.
2. Menyediakan platform untuk mengunggah dan mengorganisir materi pembelajaran secara terstruktur.
3. Memungkinkan monitoring enrollment mahasiswa dan pemberian nilai secara digital.
4. Meningkatkan efisiensi dalam distribusi konten pembelajaran kepada mahasiswa.

**Bagi Mahasiswa:**
1. Memberikan akses mudah terhadap informasi mata kuliah yang tersedia.
2. Menyediakan platform untuk melakukan enrollment secara mandiri.
3. Memfasilitasi akses terhadap materi pembelajaran yang terorganisir secara sistematis.
4. Memungkinkan mahasiswa untuk melihat nilai dan progres akademik secara real-time.

**Bagi Institusi Pendidikan:**
1. Menyediakan sistem terintegrasi untuk pengelolaan pembelajaran yang mengurangi proses manual.
2. Meningkatkan transparansi dan akuntabilitas dalam proses akademik.
3. Menyediakan data terpusat yang dapat digunakan untuk analisis dan pelaporan.
4. Mendukung transformasi digital institusi pendidikan.

**Bagi Pengembang:**
1. Memberikan pengalaman dalam membangun aplikasi web full-stack dengan teknologi modern.
2. Mempelajari implementasi RESTful API, autentikasi JWT, dan database design.
3. Memahami proses deployment aplikasi ke platform cloud.
4. Menghasilkan portfolio proyek yang dapat digunakan untuk keperluan akademik maupun profesional.

---

## BAB II  
## ANALISA DAN PERANCANGAN SISTEM

### 2.1 Analisa Kebutuhan Fungsional

Kebutuhan fungsional sistem didefinisikan berdasarkan fitur-fitur yang harus tersedia untuk memenuhi kebutuhan pengguna. Berikut adalah analisa kebutuhan fungsional sistem:

**2.1.1 Manajemen Autentikasi dan Pengguna**
1. Sistem harus menyediakan fitur registrasi pengguna baru dengan validasi input (username minimal 5 karakter, password minimal 8 karakter dengan kombinasi huruf dan angka).
2. Sistem harus menyediakan fitur login menggunakan username dan password yang menghasilkan JWT token untuk akses ke API.
3. Sistem harus mampu melakukan refresh token untuk memperpanjang sesi pengguna tanpa harus login ulang.
4. Sistem harus membedakan hak akses antara user biasa, pengajar, dan administrator.

**2.1.2 Manajemen Mata Kuliah (Course)**
1. Sistem harus dapat menampilkan daftar semua mata kuliah dengan informasi kode, nama, deskripsi, SKS, dan pengajar.
2. Sistem harus menyediakan fitur pencarian mata kuliah berdasarkan kode atau nama.
3. Sistem harus memungkinkan penambahan mata kuliah baru dengan validasi kode unik.
4. Sistem harus memungkinkan pengubahan informasi mata kuliah yang sudah ada.
5. Sistem harus memungkinkan penghapusan mata kuliah dengan konfirmasi.
6. Sistem harus menampilkan detail mata kuliah termasuk daftar materi dan mahasiswa yang terdaftar.

**2.1.3 Manajemen Materi Pembelajaran (Material)**
1. Sistem harus dapat menampilkan daftar materi pembelajaran untuk setiap mata kuliah.
2. Sistem harus memungkinkan penambahan materi baru dengan urutan (order) tertentu.
3. Sistem harus memungkinkan pengubahan konten materi yang sudah ada.
4. Sistem harus memungkinkan penghapusan materi dengan konfirmasi.
5. Sistem harus menampilkan materi secara berurutan sesuai dengan nilai order.

**2.1.4 Manajemen Enrollment**
1. Sistem harus dapat menampilkan daftar enrollment dengan filter berdasarkan mahasiswa atau mata kuliah.
2. Sistem harus memungkinkan mahasiswa untuk mendaftar ke mata kuliah (create enrollment).
3. Sistem harus mencegah duplikasi enrollment untuk kombinasi mahasiswa dan mata kuliah yang sama.
4. Sistem harus memungkinkan pengubahan data enrollment termasuk pemberian nilai (A, B, C, D, E).
5. Sistem harus memungkinkan penghapusan enrollment dengan konfirmasi.

**2.1.5 Dashboard dan Statistik**
1. Sistem harus menampilkan dashboard dengan statistik total course, enrollment, dan material.
2. Sistem harus menampilkan daftar mata kuliah terbaru.
3. Sistem harus menyediakan quick action untuk navigasi cepat ke fitur-fitur utama.

**2.1.6 RESTful API**
1. Sistem harus menyediakan API endpoints untuk operasi CRUD pada semua entitas.
2. API harus menerapkan pagination untuk efisiensi dalam menampilkan data dalam jumlah besar.
3. API harus menerapkan throttling untuk mencegah abuse dan serangan DDoS.
4. API harus memberikan response dalam format JSON dengan struktur yang konsisten.

### 2.2 Analisa Kebutuhan Non-Fungsional

Kebutuhan non-fungsional mendefinisikan karakteristik sistem yang berkaitan dengan kualitas dan performa. Berikut adalah analisa kebutuhan non-fungsional:

**2.2.1 Keamanan (Security)**
1. Sistem harus mengimplementasikan autentikasi berbasis JWT untuk melindungi endpoint API.
2. Password pengguna harus di-hash menggunakan algoritma yang aman sebelum disimpan ke database.
3. Sistem harus menerapkan validasi input untuk mencegah SQL injection dan XSS attacks.
4. Sistem harus menggunakan HTTPS untuk komunikasi client-server pada production environment.
5. Sistem harus menerapkan rate limiting untuk mencegah brute force attacks.

**2.2.2 Performa (Performance)**
1. Sistem harus mampu merespon request dalam waktu maksimal 2 detik untuk operasi standar.
2. Database queries harus dioptimasi menggunakan indexing dan query optimization.
3. Sistem harus menerapkan pagination untuk menghindari loading data dalam jumlah besar sekaligus.
4. Static files harus di-serve menggunakan middleware yang efisien (WhiteNoise).

**2.2.3 Skalabilitas (Scalability)**
1. Arsitektur sistem harus mendukung horizontal scaling dengan containerization menggunakan Docker.
2. Database harus mendukung connection pooling untuk menangani multiple concurrent requests.
3. Sistem harus dapat di-deploy di berbagai cloud platform tanpa perubahan signifikan.

**2.2.4 Ketersediaan (Availability)**
1. Sistem harus memiliki uptime minimal 99% pada production environment.
2. Sistem harus dapat melakukan graceful error handling tanpa menyebabkan crash.
3. Deployment harus menggunakan process manager (Gunicorn) yang dapat melakukan auto-restart.

**2.2.5 Maintainability**
1. Kode program harus mengikuti prinsip clean code dan design patterns yang established.
2. Sistem harus menggunakan environment variables untuk konfigurasi yang berbeda antara development dan production.
3. Dokumentasi API harus tersedia dan up-to-date untuk memudahkan maintenance.

**2.2.6 Usability**
1. Antarmuka pengguna harus responsif dan dapat diakses dari berbagai ukuran layar (desktop, tablet, mobile).
2. User interface harus intuitif dengan navigasi yang jelas.
3. Sistem harus memberikan feedback yang jelas terhadap setiap aksi pengguna.
4. Error messages harus informatif dan membantu pengguna untuk memperbaiki kesalahan.

### 2.3 Analisa Kebutuhan Hardware dan Software

**2.3.1 Kebutuhan Hardware**

**Development Environment:**
- Processor: Intel Core i3 atau setara (minimal dual-core)
- RAM: 4 GB (disarankan 8 GB atau lebih)
- Storage: 10 GB free space untuk source code, dependencies, dan database
- Network: Koneksi internet stabil untuk mengakses package repositories dan cloud deployment

**Production Environment (Railway Cloud Platform):**
- CPU: Shared vCPU sesuai paket Railway
- Memory: 512 MB - 2 GB RAM (auto-scaling)
- Storage: PostgreSQL database storage sesuai kebutuhan
- Network: Load balancer dan CDN untuk distribusi traffic

**2.3.2 Kebutuhan Software**

**Development Tools:**
1. **Operating System**: Windows 10/11, Linux (Ubuntu 20.04+), atau macOS
2. **Python**: Versi 3.14 (atau 3.10+)
3. **Code Editor**: Visual Studio Code, PyCharm, atau sejenisnya
4. **Version Control**: Git 2.30+
5. **Database**: PostgreSQL 14+ atau SQLite untuk development
6. **Container Platform**: Docker 20.10+ dan Docker Compose 2.0+
7. **Browser**: Chrome, Firefox, atau Edge untuk testing

**Backend Framework dan Libraries:**
1. **Django**: 5.2.7 - Web framework utama
2. **Django Ninja**: RESTful API framework untuk Django
3. **Django Ninja JWT**: JSON Web Token authentication
4. **psycopg2-binary**: PostgreSQL database adapter
5. **python-dotenv**: Environment variables management
6. **Gunicorn**: WSGI HTTP Server untuk production
7. **WhiteNoise**: Static files serving middleware
8. **dj-database-url**: Database URL parser
9. **Pillow**: Image processing library

**Frontend Technologies:**
1. **Bootstrap**: 5.3.0 - CSS framework untuk styling
2. **Bootstrap Icons**: Icon library
3. **Google Fonts (Inter)**: Typography
4. **Custom CSS**: Additional styling dengan gradient dan animations

**Deployment Platform:**
1. **Railway**: Cloud platform as a service (PaaS)
2. **PostgreSQL**: Managed database service
3. **GitHub**: Source code repository dan version control

### 2.4 Gambaran Arsitektur Sistem

Sistem manajemen pembelajaran ini dirancang menggunakan arsitektur monolithic dengan pemisahan concern antara backend dan frontend melalui pattern Model-View-Template (MVT) yang merupakan varian dari MVC. Sistem juga menyediakan RESTful API yang dapat diakses secara independen.

**2.4.1 Arsitektur Umum Sistem**

Sistem terdiri dari beberapa layer utama:

1. **Presentation Layer (Frontend)**
   - Template HTML dengan Bootstrap framework
   - Static files (CSS, JavaScript) untuk styling dan interaksi
   - Forms untuk input data pengguna
   - Responsive design untuk akses multi-device

2. **Application Layer (Backend)**
   - Django Views untuk handling request/response HTTP tradisional
   - Django Ninja API untuk RESTful endpoints
   - Business logic untuk validasi dan processing data
   - Authentication dan authorization menggunakan JWT

3. **Data Access Layer**
   - Django ORM (Object-Relational Mapping)
   - Models sebagai representasi entitas database
   - Query optimization dengan select_related dan prefetch_related
   - Migration management untuk version control database schema

4. **Database Layer**
   - PostgreSQL sebagai RDBMS utama
   - Connection pooling untuk efisiensi koneksi
   - Transaction management untuk data consistency

**2.4.2 Alur Request-Response**

**Untuk Web Interface:**
1. User mengakses URL melalui browser
2. Django URL dispatcher memetakan URL ke View yang sesuai
3. View memproses request, berinteraksi dengan Model jika diperlukan
4. View merender Template dengan context data
5. Template HTML di-return sebagai response ke browser

**Untuk API:**
1. Client mengirim HTTP request dengan JWT token di header
2. Django Ninja menerima request dan melakukan authentication
3. API endpoint memvalidasi input menggunakan Schema (Pydantic)
4. Business logic dijalankan dan berinteraksi dengan Model
5. Response di-serialize menjadi JSON dan dikirim ke client

**2.4.3 Containerization dengan Docker**

Sistem di-package menggunakan Docker untuk memastikan consistency antara development dan production environment:

1. **Web Container**: Berisi aplikasi Django dengan semua dependencies
2. **Database Container**: PostgreSQL (untuk development)
3. **Docker Compose**: Orchestration untuk menjalankan multiple containers

**2.4.4 Deployment Architecture**

Pada production, sistem di-deploy ke Railway platform dengan arsitektur:

1. **Application Server**: Django running on Gunicorn WSGI server
2. **Database Server**: Managed PostgreSQL by Railway
3. **Static Files**: Served via WhiteNoise middleware
4. **Load Balancer**: Managed by Railway untuk distribusi traffic
5. **Environment Configuration**: Environment variables untuk secret keys dan database credentials

### 2.5 Desain Basis Data

Desain basis data sistem menggunakan pendekatan normalisasi untuk menghindari redundansi dan memastikan integritas data. Berikut adalah deskripsi entitas-entitas utama dalam sistem:

**2.5.1 Entitas User**

Entitas ini merepresentasikan pengguna sistem, baik mahasiswa maupun pengajar. Django menggunakan built-in User model dengan atribut:
- id: Primary key, auto-increment integer
- username: String unique, digunakan untuk login
- password: String ter-hash menggunakan PBKDF2 algorithm
- email: String untuk komunikasi
- first_name: Nama depan pengguna
- last_name: Nama belakang pengguna
- is_staff: Boolean untuk membedakan admin
- is_active: Boolean untuk status akun
- date_joined: Timestamp pembuatan akun

**2.5.2 Entitas Course**

Entitas ini merepresentasikan mata kuliah dengan atribut:
- id: Primary key, auto-increment integer
- code: String unique maksimal 10 karakter (contoh: "CS101")
- name: String maksimal 200 karakter untuk nama mata kuliah
- description: Text panjang untuk deskripsi mata kuliah
- credits: Integer untuk jumlah SKS
- price: Integer untuk harga course (jika berbayar)
- teacher: Foreign key ke User (relasi many-to-one)
- instructor: Foreign key ke User (relasi many-to-one, optional)
- created_at: Timestamp otomatis saat record dibuat
- updated_at: Timestamp otomatis saat record diupdate

Relasi: Satu User dapat mengajar banyak Course (one-to-many)

**2.5.3 Entitas Material**

Entitas ini merepresentasikan materi pembelajaran dengan atribut:
- id: Primary key, auto-increment integer
- course: Foreign key ke Course (relasi many-to-one)
- title: String maksimal 200 karakter untuk judul materi
- content: Text panjang untuk isi materi
- order: Integer untuk urutan materi
- created_at: Timestamp otomatis saat record dibuat
- updated_at: Timestamp otomatis saat record diupdate

Relasi: Satu Course memiliki banyak Material (one-to-many)

**2.5.4 Entitas Enrollment**

Entitas ini merepresentasikan pendaftaran mahasiswa ke mata kuliah dengan atribut:
- id: Primary key, auto-increment integer
- student: Foreign key ke User (relasi many-to-one)
- course: Foreign key ke Course (relasi many-to-one)
- enrolled_at: Timestamp otomatis saat enrollment dibuat
- grade: String maksimal 2 karakter untuk nilai (A, B, C, D, E)

Relasi: 
- Satu User dapat memiliki banyak Enrollment (one-to-many)
- Satu Course dapat memiliki banyak Enrollment (one-to-many)
- Kombinasi student dan course harus unique (constraint)

**2.5.5 Entitas CourseMember**

Entitas ini merepresentasikan member dari course dengan role tertentu:
- id: Primary key, auto-increment integer
- user_id: Foreign key ke User (relasi many-to-one)
- course: Foreign key ke Course (relasi many-to-one)
- roles: String maksimal 50 karakter (student, instructor, etc)
- joined_at: Timestamp otomatis saat member bergabung

Relasi: Many-to-many antara User dan Course dengan additional field roles

**2.5.6 Entitas CourseContent**

Entitas ini merepresentasikan konten pembelajaran yang lebih detail:
- id: Primary key, auto-increment integer
- course_id: Foreign key ke Course (relasi many-to-one)
- name: String maksimal 200 karakter untuk nama konten
- description: Text untuk deskripsi konten
- video_url: URL untuk video pembelajaran (optional)
- file_attachment: String path untuk file attachment (optional)
- order: Integer untuk urutan konten
- created_at: Timestamp otomatis
- updated_at: Timestamp otomatis

**2.5.7 Entitas Comment**

Entitas ini merepresentasikan komentar pada konten pembelajaran untuk interaksi pengguna.

**2.5.8 Relasi Antar Entitas**

1. **User - Course**: One-to-Many (satu user/instructor dapat mengajar banyak course)
2. **Course - Material**: One-to-Many (satu course memiliki banyak material)
3. **Course - Enrollment**: One-to-Many (satu course dapat memiliki banyak enrollment)
4. **User - Enrollment**: One-to-Many (satu user dapat memiliki banyak enrollment)
5. **User - Course (via CourseMember)**: Many-to-Many with additional attributes
6. **Course - CourseContent**: One-to-Many (satu course memiliki banyak content)

**2.5.9 Indexing dan Optimasi**

Untuk meningkatkan performa query, dilakukan indexing pada:
1. Field yang sering digunakan untuk filtering (course.code, enrollment.student_id)
2. Foreign keys secara otomatis di-index oleh Django ORM
3. Unique constraints pada kombinasi field (student + course di Enrollment)

### 2.6 Alur Kerja Sistem

**2.6.1 Alur Registrasi dan Autentikasi**

1. User mengakses halaman registrasi
2. User mengisi form dengan username, email, password, dan informasi pribadi
3. Sistem melakukan validasi:
   - Username minimal 5 karakter dan belum digunakan
   - Email valid dan belum terdaftar
   - Password minimal 8 karakter dengan kombinasi huruf dan angka
4. Jika validasi berhasil, sistem membuat record User baru dengan password ter-hash
5. Sistem generate JWT token (access dan refresh token)
6. Token dikembalikan ke client untuk disimpan (localStorage atau cookie)
7. Untuk request selanjutnya, client mengirim access token di Authorization header
8. Sistem memverifikasi token sebelum memproses request
9. Jika access token expired, client dapat request refresh token untuk mendapat access token baru

**2.6.2 Alur Manajemen Course**

**Create Course:**
1. Instructor mengakses halaman tambah course
2. Instructor mengisi form dengan kode, nama, deskripsi, dan SKS
3. Sistem validasi bahwa kode course belum digunakan
4. Sistem menyimpan data course baru ke database
5. Sistem redirect ke halaman detail course

**View Course List:**
1. User mengakses halaman daftar course
2. Sistem query semua course dari database dengan pagination
3. Sistem menampilkan course dalam bentuk cards atau table
4. User dapat melakukan pencarian berdasarkan kode atau nama
5. Sistem filter dan menampilkan hasil pencarian

**Update Course:**
1. Instructor mengakses halaman edit course
2. Sistem load data course yang akan diupdate
3. Instructor mengubah informasi yang diperlukan
4. Sistem validasi dan update data ke database
5. Sistem redirect ke halaman detail course dengan notifikasi sukses

**Delete Course:**
1. Instructor klik tombol delete pada course
2. Sistem menampilkan halaman konfirmasi
3. Jika dikonfirmasi, sistem menghapus course dari database
4. Cascade delete akan menghapus material dan enrollment terkait
5. Sistem redirect ke halaman course list dengan notifikasi

**2.6.3 Alur Manajemen Material**

1. Instructor mengakses halaman detail course
2. Instructor klik tombol tambah material
3. Instructor mengisi form dengan judul, konten, dan urutan
4. Sistem menyimpan material dengan foreign key ke course
5. Sistem menampilkan material secara berurutan di halaman detail course
6. Untuk update/delete, alur serupa dengan course management

**2.6.4 Alur Enrollment**

**Student Enrollment:**
1. Mahasiswa mengakses halaman daftar course
2. Mahasiswa memilih course yang ingin diikuti
3. Mahasiswa klik tombol enroll
4. Sistem validasi bahwa mahasiswa belum terdaftar di course tersebut
5. Sistem create record enrollment baru
6. Sistem menampilkan notifikasi berhasil

**Grade Assignment:**
1. Instructor mengakses halaman enrollment list dengan filter berdasarkan course
2. Instructor memilih enrollment yang ingin diberi nilai
3. Instructor mengisi nilai (A, B, C, D, E)
4. Sistem update field grade pada enrollment
5. Mahasiswa dapat melihat nilai pada halaman profile

**2.6.5 Alur API Request**

1. Client application mengirim HTTP request ke API endpoint
2. Middleware Django memproses request:
   - Check throttling limit
   - Verify JWT token
   - Parse request body
3. Django Ninja router memetakan request ke handler function
4. Handler melakukan validasi input menggunakan Pydantic Schema
5. Business logic dieksekusi, berinteraksi dengan database via Django ORM
6. Response di-serialize menjadi JSON sesuai output Schema
7. Response dikembalikan dengan appropriate HTTP status code
8. Client menerima dan memproses response

---

## BAB III  
## IMPLEMENTASI SISTEM

### 3.1 Lingkungan Pengembangan

Pengembangan sistem manajemen pembelajaran ini dilakukan dengan menggunakan spesifikasi lingkungan sebagai berikut:

**3.1.1 Hardware yang Digunakan**
- Processor: Intel Core i5/i7 atau AMD Ryzen equivalent
- RAM: 8 GB atau lebih untuk menjalankan Docker dan IDE secara bersamaan
- Storage: SSD dengan minimal 20 GB free space
- Internet: Koneksi broadband untuk download dependencies dan deployment

**3.1.2 Software dan Tools**
- **Operating System**: Windows 10/11 dengan WSL2 untuk Docker support
- **Python**: Versi 3.14 dengan pip package manager
- **Code Editor**: Visual Studio Code dengan extensions:
  - Python extension
  - Django extension
  - Docker extension
  - GitLens untuk version control
- **Database**: PostgreSQL 14 untuk production, SQLite untuk quick development
- **Container**: Docker Desktop untuk Windows dengan Docker Compose
- **Version Control**: Git dengan GitHub sebagai remote repository
- **API Testing**: Postman atau Thunder Client untuk testing API endpoints
- **Browser**: Google Chrome dengan Developer Tools untuk debugging

**3.1.3 Package Manager dan Virtual Environment**
- **pip**: Python package installer
- **venv**: Virtual environment untuk isolasi dependencies
- **requirements.txt**: File untuk mendefinisikan semua dependencies

**3.1.4 Development Workflow**
1. Setup virtual environment untuk isolasi project
2. Install dependencies menggunakan pip dari requirements.txt
3. Configuration environment variables menggunakan .env file
4. Menjalankan migrations untuk setup database schema
5. Development dengan auto-reload feature Django
6. Testing menggunakan Django test framework
7. Version control menggunakan Git dengan conventional commits
8. Deployment ke Railway untuk production testing

### 3.2 Implementasi Arsitektur Aplikasi

**3.2.1 Struktur Direktori Proyek**

Proyek diorganisir dengan struktur yang memisahkan concern dan memudahkan maintenance:

```
UTS-Sisi-Server/
├── code/                           # Django project root
│   ├── manage.py                   # Django management script
│   ├── lms_project/                # Project configuration
│   │   ├── settings.py             # Settings dan configuration
│   │   ├── urls.py                 # Root URL routing
│   │   ├── wsgi.py                 # WSGI entry point
│   │   └── asgi.py                 # ASGI entry point
│   ├── courses/                    # Main application
│   │   ├── models.py               # Database models
│   │   ├── views.py                # View functions
│   │   ├── api.py                  # API endpoints
│   │   ├── auth_api.py             # Authentication API
│   │   ├── auth_schemas.py         # Pydantic schemas
│   │   ├── forms.py                # Django forms
│   │   ├── urls.py                 # App-specific URLs
│   │   ├── admin.py                # Admin panel config
│   │   ├── throttling.py           # Rate limiting
│   │   ├── health.py               # Health check endpoint
│   │   ├── templates/              # HTML templates
│   │   └── migrations/             # Database migrations
│   └── static/                     # Static files (CSS, JS)
├── docker-compose.yml              # Docker services definition
├── dockerfile                      # Docker image build instructions
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables
└── deployment files                # Railway deployment configs
```

**3.2.2 Configuration Management**

Sistem menggunakan environment variables untuk configuration yang berbeda antara development dan production:

**settings.py** mengimplementasikan:
1. **SECRET_KEY**: Diambil dari environment dengan fallback untuk development
2. **DEBUG**: Boolean flag yang di-set False untuk production
3. **ALLOWED_HOSTS**: List domain yang diizinkan mengakses aplikasi
4. **DATABASES**: Configuration menggunakan dj-database-url untuk parsing DATABASE_URL
5. **STATIC FILES**: Configuration untuk serving static files dengan WhiteNoise

**Environment Variables:**
- Disimpan dalam file .env untuk local development
- Dikonfigurasi melalui Railway dashboard untuk production
- Menggunakan python-dotenv untuk load variables

**3.2.3 Django Apps Structure**

Sistem menggunakan single app "courses" yang menghandle semua functionality:

1. **Models**: Definisi struktur data (Course, Material, Enrollment, dll)
2. **Views**: Function-based views untuk web interface
3. **API**: Class-based API dengan Django Ninja untuk RESTful endpoints
4. **Forms**: Django ModelForms dengan Bootstrap styling
5. **Templates**: HTML files dengan Django template language
6. **Migrations**: Database schema version control

**3.2.4 Middleware Configuration**

Middleware yang digunakan untuk request/response processing:
1. **SecurityMiddleware**: Security headers dan HTTPS enforcement
2. **WhiteNoiseMiddleware**: Efficient static files serving
3. **SessionMiddleware**: Session management
4. **AuthenticationMiddleware**: User authentication
5. **CSRFMiddleware**: Cross-Site Request Forgery protection
6. **MessageMiddleware**: Flash messages untuk user feedback

**3.2.5 URL Routing**

**Root URLs (lms_project/urls.py)**:
- /admin/: Django admin panel
- /: Web interface (courses app)
- /api/v1/: RESTful API endpoints
- /api/v1/health: Health check endpoint

**Courses URLs (courses/urls.py)**:
- /: Dashboard home
- /courses/: Course list
- /courses/<id>/: Course detail
- /courses/create/: Create course
- /courses/<id>/edit/: Edit course
- /courses/<id>/delete/: Delete course
- /materials/: Material management
- /enrollments/: Enrollment management
- /login/: Login page
- /register/: Registration page

**API URLs (api.py)**:
- /api/v1/auth/register: User registration
- /api/v1/auth/login: User login
- /api/v1/auth/refresh: Token refresh
- /api/v1/courses/: Course CRUD operations
- /api/v1/materials/: Material CRUD operations
- /api/v1/enrollments/: Enrollment CRUD operations

### 3.3 Implementasi Fitur Utama

**3.3.1 Sistem Autentikasi JWT**

Implementasi autentikasi menggunakan django-ninja-jwt untuk token-based authentication:

**Registrasi User:**
- Input divalidasi menggunakan Pydantic Schema dengan custom validators
- Username harus minimal 5 karakter dan unique
- Password minimal 8 karakter dengan kombinasi huruf dan angka
- Email harus valid dan unique
- Password di-hash menggunakan Django's PBKDF2 algorithm sebelum disimpan
- Setelah berhasil registrasi, sistem generate JWT tokens (access & refresh)

**Login:**
- User mengirim username dan password
- Sistem authenticate menggunakan Django's authentication backend
- Jika valid, generate JWT tokens yang berisi user_id dan expiration time
- Access token berlaku selama 24 jam (configurable)
- Refresh token berlaku selama 7 hari (configurable)

**Token Verification:**
- Setiap request ke protected endpoint harus include access token di header
- Format: Authorization: Bearer <access_token>
- Django Ninja JWT middleware memverifikasi token signature dan expiration
- Jika valid, user object di-attach ke request object

**Token Refresh:**
- Client mengirim refresh token ke endpoint /api/v1/auth/refresh
- Sistem verify refresh token validity
- Generate new access token dengan expiration baru
- Return new access token ke client

**3.3.2 Manajemen Course**

Implementasi CRUD operations untuk Course entity:

**Create Course:**
- Form dirender dengan Bootstrap styling untuk UI yang responsif
- Validasi di level form: code harus unique, credits harus positive integer
- Instructor field menggunakan dropdown select dari available users
- Django ORM save() method untuk persist data ke database
- Auto-populate created_at dan updated_at timestamps

**Read/List Course:**
- Query menggunakan Django ORM: Course.objects.all()
- Implementasi pagination untuk efisiensi (10 courses per page)
- Search functionality dengan Q objects untuk multiple field search
- Example: Q(code__icontains=query) | Q(name__icontains=query)
- Select related untuk optimize query (menghindari N+1 problem)

**Update Course:**
- Load existing course data menggunakan get_object_or_404()
- Pre-populate form dengan existing data
- Validasi bahwa code tetap unique (exclude current instance)
- Update database dengan save() method
- Redirect ke detail page dengan success message

**Delete Course:**
- Confirmation page untuk prevent accidental deletion
- ON DELETE CASCADE untuk automatic deletion of related materials dan enrollments
- Delete menggunakan instance.delete() method
- Redirect ke course list dengan success message

**API Implementation:**
- GET /api/v1/courses/: List dengan pagination dan search
- GET /api/v1/courses/{id}: Detail course dengan materials dan enrollments
- POST /api/v1/courses/: Create dengan JWT authentication required
- PUT /api/v1/courses/{id}: Update dengan permission check
- DELETE /api/v1/courses/{id}: Delete dengan permission check

**3.3.3 Manajemen Material**

Implementasi untuk managing learning materials:

**Create Material:**
- Form dengan foreign key ke Course (dropdown atau hidden field)
- Order field untuk sequence control
- Rich text content field (dapat di-extend dengan WYSIWYG editor)
- Validation bahwa course_id valid
- Auto-ordering jika order tidak specified (max order + 1)

**Display Materials:**
- Query dengan filter by course: Material.objects.filter(course=course)
- Ordering by order field: .order_by('order', 'created_at')
- Display di course detail page dalam urutan yang benar
- Inline editing capability untuk quick updates

**Update dan Delete:**
- Similar pattern dengan Course management
- Update order field untuk resequencing materials
- Cascade handling jika material di-delete

**3.3.4 Manajemen Enrollment**

Implementasi student enrollment system:

**Create Enrollment:**
- Form dengan student dan course selection
- Unique constraint validation (student, course)
- Check enrollment limit jika ada kapasitas course
- Auto-populate enrolled_at timestamp
- Handle duplicate enrollment dengan user-friendly error message

**List Enrollments:**
- Filter berdasarkan student atau course
- Display dengan information: student name, course code, enrolled date, grade
- Pagination untuk large datasets
- Export functionality untuk reporting (optional)

**Grade Assignment:**
- Update form dengan grade choices: A, B, C, D, E
- Validation bahwa grade valid
- Permission check: hanya instructor course yang bisa assign grade
- Log perubahan grade untuk audit trail

**Student View:**
- My Courses page menampilkan enrolled courses
- Filter enrollments by current user
- Display course information, materials, dan grade
- Quick access ke course materials

**3.3.5 Dashboard dan Reporting**

Implementasi dashboard untuk overview system:

**Statistics:**
- Count aggregation: Course.objects.count()
- Enrollment.objects.count()
- Material.objects.count()
- Display menggunakan cards dengan icons dan colors

**Recent Courses:**
- Query: Course.objects.all().order_by('-created_at')[:5]
- Display dengan basic information dan link ke detail

**Quick Actions:**
- Buttons untuk navigate ke frequently used features
- Conditional rendering based on user role (student vs instructor)

**3.3.6 RESTful API dengan Django Ninja**

Implementasi API menggunakan Django Ninja framework:

**Request Validation:**
- Menggunakan Pydantic Schema untuk input validation
- Type checking otomatis (int, str, bool, etc)
- Custom validators dengan @field_validator decorator
- Error messages yang descriptive

**Response Serialization:**
- Output schema untuk consistent response format
- Nested serialization untuk related objects
- Exclude sensitive information (password hash)

**Pagination:**
- Custom pagination class dengan configurable page_size
- Metadata di response: total, page, page_size
- Links untuk next dan previous page

**Error Handling:**
- HttpError untuk explicit error responses
- 400 Bad Request untuk validation errors
- 401 Unauthorized untuk authentication failures
- 404 Not Found untuk non-existent resources
- 500 Internal Server Error untuk unexpected errors

**API Documentation:**
- Auto-generated OpenAPI/Swagger documentation
- Available at /api/v1/docs
- Interactive API testing interface
- Schema definitions untuk request dan response

**3.3.7 Rate Limiting dan Throttling**

Implementasi untuk prevent API abuse:

**Throttle Decorators:**
- @throttle_strict: 10 requests per minute untuk sensitive endpoints (register, login)
- @throttle_moderate: 30 requests per minute untuk standard operations
- @throttle: 60 requests per minute untuk read operations

**Implementation:**
- Custom throttle decorator using caching backend
- Track requests by IP address atau user_id
- Return 429 Too Many Requests jika limit exceeded
- Include Retry-After header dengan cooldown time

### 3.4 Manajemen Data dan Database

**3.4.1 Database Configuration**

**Development Environment:**
- SQLite3 untuk quick setup tanpa external dependencies
- Database file: db.sqlite3 di project root
- Suitable untuk single-user development

**Production Environment:**
- PostgreSQL managed by Railway
- Connection string dari DATABASE_URL environment variable
- Connection pooling dengan conn_max_age=600 seconds
- Health checks enabled untuk automatic reconnection

**3.4.2 Django ORM Implementation**

**Model Definition:**
- Class-based models inheriting from models.Model
- Field types: CharField, TextField, IntegerField, ForeignKey, DateTimeField
- Meta options: ordering, unique_together, verbose_name
- Custom __str__ methods untuk readable representation

**Query Optimization:**
- select_related() untuk forward ForeignKey relationships
- prefetch_related() untuk reverse ForeignKey dan Many-to-Many
- only() dan defer() untuk limiting fields retrieved
- Indexing pada frequently queried fields

**Transaction Management:**
- Atomic transactions untuk operations yang modify multiple tables
- Rollback otomatis jika exception terjadi
- Use @transaction.atomic decorator untuk critical operations

**3.4.3 Database Migrations**

**Migration Workflow:**
1. Modify models.py dengan changes
2. Run: python manage.py makemigrations
3. Review generated migration file
4. Run: python manage.py migrate
5. Commit migration files ke version control

**Migration Files:**
- 0001_initial.py: Initial schema creation
- Subsequent migrations: incremental changes
- Dependencies tracking untuk proper order
- Reversible dengan migrate backward

**Production Migrations:**
- Migrations dijalankan automatically pada Railway deployment
- Script: migrate.sh yang execute migrations sebelum start server
- Zero-downtime migrations untuk avoid service interruption

**3.4.4 Data Seeding**

**Demo Data Setup:**
- Management command: setup_demo untuk populate initial data
- Create sample users, courses, materials, dan enrollments
- Useful untuk testing dan demonstration
- Script: setup_demo_data.py di management/commands

**Fixtures:**
- JSON atau YAML files untuk predefined data
- Load dengan: python manage.py loaddata fixture_name
- Useful untuk test data consistency

### 3.5 Pengujian Sistem

**3.5.1 Unit Testing**

Implementasi unit tests menggunakan Django test framework:

**Test Cases untuk Models:**
- Test model creation dengan valid data
- Test field validations dan constraints
- Test unique constraints
- Test foreign key relationships
- Test model methods dan properties

**Test Cases untuk Views:**
- Test GET requests return correct templates
- Test POST requests create/update data correctly
- Test form validations
- Test authentication requirements
- Test permission checks

**Test Cases untuk API:**
- Test endpoint responses dengan different HTTP methods
- Test authentication requirements
- Test input validation dengan invalid data
- Test pagination functionality
- Test error handling dan status codes

**Running Tests:**
- Command: python manage.py test
- Test database otomatis created dan destroyed
- Coverage report untuk track test coverage
- Continuous Integration dengan GitHub Actions (optional)

**3.5.2 Integration Testing**

Testing interaksi between components:
- Test complete user flows (register → login → create course → enroll)
- Test database transactions dan rollbacks
- Test API integration dengan frontend
- Test external service integrations

**3.5.3 Manual Testing**

Testing melalui user interface:
- Functional testing untuk semua fitur
- UI/UX testing untuk responsiveness dan usability
- Cross-browser testing (Chrome, Firefox, Safari, Edge)
- Mobile responsiveness testing
- Performance testing dengan banyak data

**3.5.4 API Testing dengan Postman**

Testing API endpoints:
- Create collection untuk semua endpoints
- Environment variables untuk base_url dan tokens
- Test scripts untuk automated assertions
- Chain requests untuk workflow testing
- Export collection untuk documentation

### 3.6 Deployment

**3.6.1 Containerization dengan Docker**

**Dockerfile Configuration:**
- Base image: python:3.14-slim
- Working directory: /app/code
- Copy requirements.txt dan install dependencies
- Copy source code
- Expose port 8000
- CMD untuk run Gunicorn server

**Docker Compose Setup:**
- Service: web (Django app)
- Service: db (PostgreSQL)
- Volume mounting untuk persistent data
- Network configuration untuk inter-container communication
- Environment variables configuration

**3.6.2 Production Server Setup**

**Gunicorn Configuration:**
- WSGI HTTP server untuk production
- Worker processes: (2 × CPU cores) + 1
- Worker class: sync untuk standard requests
- Timeout: 120 seconds
- Bind to 0.0.0.0:8000

**Static Files:**
- WhiteNoise middleware untuk serve static files
- Collect static: python manage.py collectstatic
- Compression enabled untuk faster loading
- Cache headers untuk browser caching

**3.6.3 Deployment ke Railway**

**Preparation:**
- Push code ke GitHub repository
- Create .env file dengan production settings
- Test locally dengan production-like settings

**Railway Setup:**
1. Connect GitHub repository ke Railway
2. Railway auto-detect Dockerfile
3. Add PostgreSQL service
4. Configure environment variables
5. Railway auto-build dan deploy

**Environment Variables di Railway:**
- SECRET_KEY: Django secret key untuk production
- DEBUG: False
- ALLOWED_HOSTS: railway-domain.railway.app
- DATABASE_URL: Auto-populated by Railway PostgreSQL
- JWT settings: token lifetimes

**Deployment Process:**
1. Railway detect changes di GitHub
2. Build Docker image dari Dockerfile
3. Run predeploy script (migrations)
4. Start container dengan Gunicorn
5. Health check untuk verify deployment
6. Route traffic ke new deployment
7. Old deployment terminated after successful health check

**3.6.4 Post-Deployment**

**Monitoring:**
- Railway provides logs untuk debugging
- Monitor resource usage (CPU, memory, disk)
- Set up alerts untuk downtime atau errors

**Database Backup:**
- Railway automatic daily backups untuk PostgreSQL
- Manual backup via pg_dump jika diperlukan
- Restore procedure documented

**Domain Configuration:**
- Railway provides subdomain: app-name.railway.app
- Custom domain dapat dikonfigurasi
- Automatic SSL/TLS certificates via Let's Encrypt

**Continuous Deployment:**
- Push ke main branch trigger automatic deployment
- Review apps untuk testing changes sebelum merge
- Rollback capability jika deployment failed

---

## BAB IV  
## PENUTUP

### 4.1 Kesimpulan

Berdasarkan pengembangan sistem manajemen pembelajaran berbasis web yang telah dilakukan, dapat diambil beberapa kesimpulan sebagai berikut:

1. **Keberhasilan Implementasi Sistem**
   Sistem manajemen pembelajaran berbasis web telah berhasil dibangun dengan mengimplementasikan seluruh fitur yang direncanakan, meliputi manajemen mata kuliah, materi pembelajaran, enrollment mahasiswa, serta sistem autentikasi dan otorisasi yang aman. Sistem dapat menjalankan operasi Create, Read, Update, dan Delete (CRUD) untuk semua entitas utama dengan performa yang optimal.

2. **Arsitektur yang Modular dan Scalable**
   Penggunaan framework Django dengan pattern Model-View-Template (MVT) memungkinkan pemisahan concern yang jelas antara business logic, data access, dan presentation layer. Implementasi RESTful API menggunakan Django Ninja memberikan fleksibilitas untuk integrasi dengan aplikasi frontend modern atau mobile application di masa mendatang. Containerization menggunakan Docker memastikan consistency antara development dan production environment serta memudahkan scaling horizontal.

3. **Keamanan Sistem yang Terjamin**
   Implementasi autentikasi berbasis JSON Web Token (JWT) memberikan mekanisme keamanan yang robust dengan stateless authentication. Password pengguna di-hash menggunakan algoritma PBKDF2 sebelum disimpan ke database, dan sistem menerapkan rate limiting untuk mencegah brute force attacks. Validasi input yang ketat di level form dan API schema membantu mencegah SQL injection dan XSS attacks.

4. **Database Design yang Optimal**
   Struktur database yang menerapkan normalisasi hingga bentuk normal ketiga memastikan integritas data dan menghindari redundansi. Relasi antar entitas seperti one-to-many dan many-to-many telah diimplementasikan dengan benar menggunakan foreign keys dan constraint. Indexing pada field yang sering di-query meningkatkan performa sistem secara signifikan.

5. **User Experience yang Baik**
   Interface pengguna yang dibangun dengan Bootstrap framework menghasilkan tampilan yang modern, responsif, dan user-friendly. Sistem dapat diakses dari berbagai perangkat (desktop, tablet, mobile) dengan tampilan yang optimal. Feedback yang jelas melalui flash messages membantu pengguna memahami hasil dari setiap aksi yang dilakukan.

6. **Deployment yang Sukses**
   Sistem telah berhasil di-deploy ke platform cloud Railway dan dapat diakses secara publik. Managed PostgreSQL database memberikan reliability dan automatic backup. Continuous deployment dari GitHub repository memudahkan proses update dan maintenance sistem.

7. **Pencapaian Tujuan Pembelajaran**
   Proyek ini telah memberikan pengalaman praktis dalam membangun aplikasi web full-stack dengan teknologi modern. Pemahaman mendalam tentang backend development dengan Django, database design, RESTful API, autentikasi JWT, containerization, dan cloud deployment telah tercapai dengan baik.

### 4.2 Saran Pengembangan (Next Step)

Meskipun sistem telah berfungsi dengan baik, masih terdapat beberapa aspek yang dapat dikembangkan lebih lanjut untuk meningkatkan fungsionalitas dan performa sistem:

**4.2.1 Peningkatan Fitur Fungsional**

1. **Sistem Notifikasi Real-time**
   Implementasi WebSocket menggunakan Django Channels untuk memberikan notifikasi real-time kepada pengguna ketika ada update pada course, material baru, atau perubahan nilai. Push notification untuk mobile devices juga dapat diintegrasikan.

2. **Forum Diskusi dan Q&A**
   Menambahkan fitur forum diskusi untuk setiap course agar mahasiswa dapat bertanya dan berdiskusi dengan pengajar maupun sesama mahasiswa. Implementasi system voting untuk jawaban terbaik dapat meningkatkan engagement.

3. **Quiz dan Assignment**
   Implementasi fitur quiz dengan auto-grading untuk multiple choice questions dan assignment submission dengan deadline tracking. Gradebook yang comprehensive untuk tracking progres mahasiswa secara detail.

4. **Video Streaming Integration**
   Integrasi dengan platform video seperti YouTube, Vimeo, atau self-hosted video server untuk pembelajaran berbasis video. Implementasi video progress tracking untuk monitoring pembelajaran.

5. **Learning Analytics dan Dashboard**
   Dashboard analytics untuk instructor yang menampilkan statistik engagement mahasiswa, completion rate, average scores, dan insights lainnya menggunakan visualization libraries seperti Chart.js atau D3.js.

**4.2.2 Peningkatan Teknis**

1. **Caching Layer**
   Implementasi Redis sebagai caching layer untuk meningkatkan performa dengan menyimpan frequently accessed data di memory. Cache invalidation strategy untuk memastikan data consistency.

2. **Search Engine Integration**
   Integrasi dengan Elasticsearch untuk full-text search yang lebih powerful dengan support untuk fuzzy matching, relevance scoring, dan faceted search.

3. **Asynchronous Task Processing**
   Implementasi Celery untuk handling background tasks seperti email sending, report generation, dan data processing yang memakan waktu. Redis atau RabbitMQ sebagai message broker.

4. **API Versioning**
   Implementasi API versioning (v1, v2) untuk maintain backward compatibility ketika melakukan breaking changes pada API structure.

5. **GraphQL API**
   Selain REST API, implementasi GraphQL endpoint menggunakan Graphene-Django untuk memberikan fleksibilitas kepada client dalam query data yang dibutuhkan.

**4.2.3 Peningkatan Keamanan**

1. **Two-Factor Authentication (2FA)**
   Implementasi 2FA menggunakan TOTP (Time-based One-Time Password) atau SMS verification untuk menambah layer keamanan pada login process.

2. **OAuth2 Integration**
   Integrasi dengan OAuth2 providers seperti Google, GitHub, atau Microsoft untuk social login yang memudahkan pengguna.

3. **Audit Logging**
   Implementasi comprehensive audit logging untuk tracking semua perubahan data yang dilakukan pengguna untuk compliance dan security purposes.

4. **Content Security Policy (CSP)**
   Implementasi CSP headers untuk mencegah XSS attacks dengan restrict sources dari mana scripts dapat di-load.

**4.2.4 Peningkatan DevOps**

1. **CI/CD Pipeline**
   Setup GitHub Actions atau GitLab CI untuk automated testing, linting, dan deployment. Automatic rollback jika tests failed.

2. **Monitoring dan Alerting**
   Integrasi dengan monitoring tools seperti Sentry untuk error tracking, New Relic atau Datadog untuk application performance monitoring (APM).

3. **Load Testing**
   Melakukan load testing menggunakan tools seperti Locust atau Apache JMeter untuk mengetahui capacity sistem dan identify bottlenecks.

4. **Kubernetes Deployment**
   Migrate dari Railway ke Kubernetes cluster untuk more control over orchestration, auto-scaling, dan zero-downtime deployments.

**4.2.5 Peningkatan User Experience**

1. **Progressive Web App (PWA)**
   Convert aplikasi menjadi PWA agar dapat di-install di mobile devices dan support offline functionality menggunakan service workers.

2. **Internationalization (i18n)**
   Implementasi multi-language support menggunakan Django's internationalization framework agar sistem dapat digunakan oleh pengguna dari berbagai negara.

3. **Accessibility (A11y)**
   Improve accessibility dengan implementasi ARIA labels, keyboard navigation, screen reader support, dan color contrast yang sesuai WCAG guidelines.

4. **Dark Mode**
   Implementasi dark mode theme yang dapat di-toggle oleh pengguna untuk better user experience terutama untuk penggunaan malam hari.

**4.2.6 Integrasi dengan Sistem Lain**

1. **Learning Tools Interoperability (LTI)**
   Implementasi LTI protocol untuk integrasi dengan learning management systems lain atau educational tools.

2. **Payment Gateway**
   Jika ada course berbayar, integrasi dengan payment gateway seperti Stripe, PayPal, atau Midtrans untuk processing payments.

3. **Email Service**
   Integrasi dengan transactional email service seperti SendGrid atau Mailgun untuk sending notifications, password reset, dan newsletters.

4. **Cloud Storage**
   Implementasi cloud storage seperti AWS S3 atau Google Cloud Storage untuk storing course materials, assignments, dan user-uploaded content.

**4.2.7 Mobile Application**

1. **Native Mobile App**
   Develop native mobile applications untuk Android dan iOS menggunakan React Native atau Flutter yang consume existing REST API.

2. **Mobile-First Design**
   Redesign interface dengan mobile-first approach untuk better experience pada mobile devices yang merupakan majority users.

Dengan implementasi saran-saran pengembangan di atas secara bertahap, sistem manajemen pembelajaran ini dapat berkembang menjadi platform yang lebih komprehensif, robust, dan sesuai dengan kebutuhan institusi pendidikan modern. Continuous improvement dan feedback dari pengguna akan menjadi kunci dalam evolusi sistem ke depannya.

---

**AKHIR LAPORAN**

