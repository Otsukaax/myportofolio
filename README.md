# Portofolio Pribadi - Pemrograman Berbasis Platform (CSUI)

| Atribut | Informasi |
| :--- | :--- |
| **Nama** | Azka Nur Jauhar |
| **NPM** | 2506612410 |
| **Kelas** | PBP B |
| **Tautan PWS** | [https://azka-nur-myportofolio.pws.cs.ui.ac.id/](https://azka-nur-myportofolio.pws.cs.ui.ac.id/) |
| **Tautan Repositori** | [https://github.com/Otsukaax/myportofolio](https://github.com/Otsukaax/myportofolio) |

---

## Deskripsi Proyek
Proyek web portofolio dinamis yang dibangun menggunakan framework **Django** untuk mata kuliah Pemrograman Berbasis Platform (PBP), Fakultas Ilmu Komputer, Universitas Indonesia. Proyek ini mengimplementasikan konsep arsitektur *Model-View-Template* (MVT), manajemen autentikasi & *Role-Based Access Control* (RBAC), relasi database, interaksi asinkronus berbasis **AJAX (Fetch API)**, serta alur otomatisasi *Continuous Integration & Continuous Deployment* (**CI/CD**) ke Pacil Web Service (**PWS**).

---

## Panduan Menjalankan Proyek (Setup Guide)

### Prasyarat
- Python 3.10 atau versi yang lebih baru
- Git
- Peramban web modern (Google Chrome, Mozilla Firefox, Safari, atau Microsoft Edge)

### Langkah Instalasi & Menjalankan Lokal

1. **Clone repositori dan masuk ke direktori proyek**:
   ```bash
   git clone https://github.com/Otsukaax/myportofolio.git
   cd myportofolio
   ```

2. **Membuat dan mengaktifkan virtual environment**:
   - **Windows**:
     ```bash
     python -m venv env
     .\env\Scripts\activate
     ```
   - **Linux / macOS**:
     ```bash
     python3 -m venv env
     source env/bin/activate
     ```

3. **Install dependensi**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Migrasi database**:
   ```bash
   python manage.py migrate
   ```

5. **Menjalankan unit test** *(verifikasi fungsionalitas)*:
   ```bash
   python manage.py test
   ```

6. **Menjalankan server pengembangan**:
   ```bash
   python manage.py runserver
   ```
   Buka tautan [http://localhost:8000/](http://localhost:8000/) pada peramban web untuk melihat aplikasi portofolio.

---

### Alur CI/CD Deployment ke PWS
Proyek ini telah dikonfigurasi dengan alur deployment otomatis menggunakan **GitHub Actions**:
- **Branch Pengembangan (`dev`)**: Digunakan untuk pengerjaan fitur baru dan eksperimen tanpa memengaruhi lingkungan produksi.
- **Branch Produksi (`main`)**: Setiap perubahan yang di-*push* atau di-*merge* ke branch `main` akan secara otomatis memicu alur kerja GitHub Actions untuk melakukan sinkronisasi dan *push* ke branch `master` pada server Pacil Web Service (PWS).

---

## Progress Mingguan Week 7

- **Penyelesaian Tutorial 7 & Individual Assignment 6**
- **Implementasi Django REST Framework (DRF) Serializer:** Membuat EducationSerializer dengan pendaftaran *fields* eksplisit, *field* kalkulasi *read-only* (is_current, star_count, is_starred, starred_by_names), serta sanitasi input menggunakan strip_tags().
- **Implementasi RESTful API Endpoints:** Membangun endpoint berbasis fungsi @api_view di /api/v1/educations/ untuk operasi list (GET, POST), detail (GET, PUT, PATCH, DELETE), dan toggle star (POST) dengan kode status HTTP terstandarisasi (200, 201, 204, 400, 403, 404).
- **Penerapan Hak Akses Berlapis (Role-Based Access Control):** Menggunakan IsPortfolioOwnerOrEditorOrReadOnly dan IsAuthenticated untuk menegakkan aturan akses 4 peran (Guest, User biasa, Editor, dan Superuser) langsung di level server/API.
- **Integrasi Frontend AJAX Tanpa Reload:** Memperbarui antarmuka education.html agar menampilkan data, pencarian *real-time* (debouncing 300ms), penambahan data, interaksi bintang, dan penghapusan data secara asinkronus via Fetch API dengan notifikasi Toast interaktif.
- **Fitur Ekstra Modal Edit Interaktif (Kriteria Skor 4):** Menyediakan form popover modal edit interaktif dengan *pre-fill* data otomatis yang memungkinkan Editor dan Superuser memperbarui data riwayat pendidikan via method PUT/PATCH secara asinkron tanpa *reload* dokumen.
- **Optimasi Database & Pengujian Menyeluruh:** Mengoptimalkan pembacaan relasi data menggunakan .prefetch_related('starred_by') untuk mencegah masalah query N+1, serta menambahkan pengujian unit komprehensif pada 	ests_api.py (total 47 tes app main lulus 100%).

---

### Tugas 6

1. **Jelaskan apa yang dimaksud dengan REST dan mengapa mengembalikan JSON saja belum cukup untuk menyebut sebuah API sebagai RESTful! Jelaskan pula perbedaan PUT dan PATCH beserta contoh kapan masing-masing sebaiknya digunakan!**

   - REST (*Representational State Transfer*) adalah gaya arsitektur perangkat lunak untuk sistem terdistribusi yang memanfaatkan protokol komunikasi *stateless* dengan memanipulasi *resource* melalui URI dan method standar.
   - Kenapa JSON belum cukup? JSON hanyalah format representasi/serialisasi data mentah. Sebuah API baru dapat dikatakan *RESTful* jika memenuhi prinsip-prinsip arsitektur REST, di antaranya:
     - **Resource-Oriented URI:** endpoint dinamai berdasarkan kata benda representasi *resource* (misalnya `/api/v1/educations/`)
     - **Uniform Interface & Standard HTTP Methods:** Menggunakan kata kerja HTTP sesuai semantiknya (`GET`/`HEAD` untuk membaca, `POST` untuk membuat, `PUT` untuk mengganti total, `PATCH` untuk memperbarui sebagian, dan `DELETE` untuk menghapus) serta mengembalikan status code HTTP yang standar (`200 OK`, `201 Created`, `204 No Content`, `400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`).
     - **Statelessness:** Setiap request dari klien ke server harus memuat semua informasi yang dibutuhkan secara lengkap tanpa mengandalkan status konteks sesi yang disimpan di memori server secara dependen.
   - **Perbedaan PUT dan PATCH:**
     - **`PUT` (Full Replacement):** Digunakan untuk mengganti seluruh representasi resource dengan payload yang baru dikirim secara menyeluruh. Klien mengirimkan semua atribut; atribut yang tidak dikirim idealnya dianggap direset atau dikosongkan oleh server.
       - *Contoh Penggunaan:* Saat form modal edit riwayat pendidikan mengirimkan pembaruan untuk seluruh field sekaligus (institusi, jenjang/program studi, IPK, tanggal mulai, dan tanggal selesai).
     - **`PATCH` (Partial Update):** Digunakan untuk memperbarui sebagian (*partial update*) dari atribut resource tanpa memengaruhi atribut lainnya.
       - *Contoh Penggunaan:* Ketika aplikasi hanya ingin memperbarui status aktif/lulus (`ended_at`), memperbarui nilai IPK saja, atau saat fitur *toggle star* memperbarui daftar pengguna yang membintangi tanpa perlu mengirim ulang data riwayat pendidikan lainnya.

2. **Jelaskan peran serializer pada Django REST Framework! Apa keuntungannya dibandingkan merakit dictionary secara manual dengan JsonResponse seperti pada Tutorial 05?**

   - **Peran Serializer:** Serializer pada DRF bertindak sebagai jembatan dua arah (*two-way converter*) antara objek kompleks Django dan format data universal:
     1. **Serialization:** Mengonversi objek model/QuerySet Django yang kompleks menjadi struktur data primitif Python (seperti *dictionary*) yang siap dirender ke dalam JSON.
     2. **Deserialization & Validation:** Menerima data masukan mentah dari request (JSON), memvalidasi integritas dan keamanannya melalui aturan schema atau method `validate_<field>()`, lalu menginstansiasinya kembali menjadi objek model database yang siap disimpan (`.save()`).
   - **Keuntungan Dibandingkan Merakit Dictionary Manual (`JsonResponse` Tutorial 05):**
     - **Menghilangkan Boilerplate & Duplikasi Kode (DRY):** Tidak perlu lagi menulis perulangan `for` dan merakit dictionary secara manual field-per-field setiap kali ingin mengirim data JSON.
     - **Validasi Terintegrasi dan Deklaratif:** Serializer otomatis memeriksa tipe data, batas karakter (*maxlength*), keharusan pengisian (*required*), serta format angka/tanggal melalui `is_valid(raise_exception=True)`. Pada `JsonResponse` manual, seluruh logika validasi dan penanganan error harus dirangkai sendiri secara manual.
     - **Dukungan Relasi Kompleks & Computed Fields:** Memudahkan penanganan relasi database (seperti *ManyToMany* `starred_by`) dan pembuatan *computed field* melalui `SerializerMethodField` (misalnya `is_current`, `star_count`, dan `is_starred`) dengan integrasi optimasi query seperti `.prefetch_related()`.

3. **Jelaskan perbedaan autentikasi dan otorisasi pada Django REST Framework! Mengapa hak akses harus diperiksa dengan permission class di server, bukan hanya dengan menyembunyikan tombol di template?**

   - **Perbedaan Autentikasi dan Otorisasi:**
     - **Autentikasi:** Proses untuk memverifikasi identitas pengguna yang melakukan request (apakah pengguna terdaftar dan memiliki sesi/kredensial yang valid). Di DRF, contohnya diatur via `@authentication_classes([SessionAuthentication])`.
     - **Otorisasi:** Proses untuk menentukan apakah pengguna yang sudah teridentifikasi memiliki hak akses untuk membaca atau memanipulasi *resource* tertentu. Di DRF, ini diatur melalui permission classes seperti `IsPortfolioOwnerOrEditorOrReadOnly` dan `IsAuthenticated`.
   - **Mengapa Hak Akses Harus Diperiksa di Server (Permission Class):**
     - Menyembunyikan tombol pada antarmuka/template hanyalah aspek kenyamanan visual (*User Experience* / UX), bukan keamanan (*Security*).
     - Pengguna atau penyerang dapat dengan mudah memicu request HTTP mutasi (seperti `POST`, `PUT`, atau `DELETE`) secara langsung ke endpoint API menggunakan *browser developer tools (Console/Fetch API)*, cURL, atau Postman tanpa perlu mengeklik tombol yang ada di layar.
     - Pemeriksaan di sisi server melalui *permission class* bertindak sebagai gerbang pengamanan absolut yang menolak request yang tidak sah secara konsisten di tingkat backend dengan status HTTP `401 Unauthorized` atau `403 Forbidden`.

4. **Jelaskan mengapa permintaan yang mengubah data tetap memerlukan token CSRF ketika API memakai SessionAuthentication! Mengapa test yang memakai force_authenticate tidak cukup untuk membuktikan bahwa perlindungan CSRF berjalan?**

   - **Alasan Perlunya Token CSRF pada `SessionAuthentication`:**
     - `SessionAuthentication` mengandalkan cookie sesi browser (`sessionid`) untuk mengenali pengguna yang login.
     - Browser secara otomatis akan selalu menyertakan cookie tersebut pada setiap request ke domain yang dituju, termasuk jika request tersebut dipicu secara tersembunyi oleh situs berbahaya pihak ketiga (*Cross-Site Request Forgery* / CSRF).
     - Tanpa token CSRF, situs jahat dapat membuat browser korban mengirimkan request mutasi data (seperti `POST`, `PUT`, `DELETE`) atas nama korban yang sedang login tanpa sepengetahuannya. Oleh karena itu, token rahasia `X-CSRFToken` wajib disertakan pada header request untuk memastikan bahwa mutasi data benar-benar berasal dari antarmuka aplikasi portofolio yang sah.
   - **Mengapa Test dengan `force_authenticate` Tidak Cukup:**
     - Method `force_authenticate` pada pustaka pengujian DRF bekerja dengan langsung menyuntikkan objek `user` dummy ke dalam request dan **melewati (bypass)** seluruh middleware autentikasi bawaan, termasuk *CSRF validation check*.
     - Akibatnya, pengujian yang menggunakan `force_authenticate` hanya menguji logika permission dan logika view, tetapi sama sekali tidak menguji apakah pertahanan CSRF aktif dan berfungsi normal dalam menolak request tanpa token.
     - Untuk membuktikan perlindungan CSRF bekerja secara nyata, pengujian harus dilakukan dengan klien pengujian yang menegakkan pemeriksaan CSRF (`enforce_csrf_checks=True`) atau menggunakan alur login standar berbasis cookie sesi.

---

## AI Disclosure Week 6

Dalam pengerjaan Tugas Individu 6 kali ini, saya menerapkan prinsip kolaborasi kritis bersama AI Assistant (*Antigravity* berbasis model *Gemini 3.8 Flash*) untuk membantu membedah alur arsitektur RESTful API, merancang struktur pengujian unit test yang komprehensif, dan mengaudit keamanan aplikasi.

* **Log Percakapan Lengkap**: Riwayat transkrip percakapan utuh dari awal hingga akhir telah diabadikan secara transparan pada berkas [`AI_CHAT_LOG.md`](AI_CHAT_LOG.md).
* **Strategi Prompting**:
  1. *Pseudocode-First Approach*: Sebelum menulis atau menyentuh kode, saya meminta AI merancang seluruh alur logika backend (API views) dan frontend (AJAX) ke dalam bentuk *pseudocode* agar saya memahami setiap tahapan proses komunikasi data secara konseptual.
  2. *Modular Step-by-Step Prompting*: Pengerjaan dipecah menjadi tahapan-tahapan kecil yang terisolasi (Tahap 1: Serializer $\rightarrow$ Tahap 2: API Views & Routing $\rightarrow$ Tahap 3: Integrasi Frontend AJAX & Modal Edit $\rightarrow$ Tahap 4: Unit Testing), di mana setiap tahap diuji dan diverifikasi secara mandiri sebelum lanjut ke tahap berikutnya.
  3. *Critical Questioning*: Saya aktif menelusuri dan mempertanyakan setiap fungsi yang disarankan jika dirasa asing atau berada di luar cakupan panduan resmi dari dosen.

* **Bagian yang Dibantu oleh AI**:
  * Merumuskan skenario pengujian komprehensif pada `main/tests_api.py` yang mencakup 4 peran pengguna (*Guest*, *Regular User*, *Editor*, dan *Superuser*), penolakan mutasi database, serta verifikasi proteksi CSRF.
  * Membantu membedah rubrik penilaian untuk memastikan kriteria skor 4 (seperti optimasi query database `.prefetch_related()` dan modal interaktif edit) terpenuhi.
  * Melakukan review keamanan pada integrasi AJAX terhadap potensi celah XSS dan kelengkapan header `X-CSRFToken`.

* **Analisis Kritis Keterbatasan AI**:
  1. *Keterbatasan Konteks Materi Kuliah vs Kode Nyata*: Pada tahap pembuatan serializer, AI sempat mengusulkan penggunaan method lanjutan `to_internal_value` untuk menangani input tanggal kosong `ended_at`. Padahal method ini tergolong *overengineered* dan tidak pernah diajarkan di slide materi perkuliahan. Hal ini terjadi karena AI kurang peka bahwa modul panduan dosen menggunakan model `Project` (yang hanya berisi field teks dan URL sederhana tanpa tanggal opsional).
  2. *Keterbatasan dalam Menangkap Konteks Logika Template Dinamis*: AI sempat melewatkan peletakan tag `{% csrf_token %}` di luar blok kondisional `{% if %}`. Karena form modal hanya dirender untuk Superuser dan Editor, pengguna biasa yang membuka halaman tidak akan memiliki input CSRF di DOM sehingga browser tidak membuat cookie `csrftoken`. Akibatnya, aksi interaktif Star bagi pengguna biasa akan ditolak oleh server dengan status `403 CSRF Failed: CSRF cookie not set`.

* **Perbaikan dan Koreksi Manual yang Dilakukan**:
  * **Penyederhanaan Serializer**: Saya menolak pendekatan `to_internal_value` dan mempertahankan struktur `EducationSerializer` agar 100% konsisten dengan template standar materi tutorial. Sebagai gantinya, penanganan tanggal kosong diselesaikan secara bersih dan wajar di frontend JavaScript dengan mengubah string kosong menjadi `null` (`fields.get('ended_at') || null`).
  * **Koreksi Penempatan CSRF**: Menempatkan tag `{% csrf_token %}` secara eksplisit di luar blok kondisional (tepat di atas tag pembuka `<script>`), menjamin seluruh pengguna yang login memiliki cookie keamanan saat berinteraksi.
  * **Penyusunan Kode Frontend Mandiri**: Saya menulis dan mengintegrasikan sendiri elemen modal HTML popover edit (`#edit-education-modal`), fungsi *pre-fill* form otomatis dari `dataset`, serta perbaikan entitas tombol penutup modal (`&times;`).
---

## Progress Mingguan Week 5

- **Penyelesaian Tutorial 5**
- **Implementasi AJAX Read pada Education:** Mengubah halaman `Education` agar hanya memuat kerangka dasar (skeleton), lalu mengambil dan merender data riwayat pendidikan secara asinkronus dari endpoint JSON via `fetch()`.
- **Implementasi Fitur Pencarian Real-Time dengan Debouncing:** Menerapkan fungsi pencarian nama institusi dengan *debounce delay* sebesar 300ms tanpa perlu me-*reload* halaman browser.
- **Implementasi Modal Form Berbasis HTML5 Popover API:** Membuat form penambahan riwayat pendidikan menggunakan Popover API bawaan (`popover="auto"` dan `popovertarget`) tanpa dependensi pustaka eksternal.
- **Implementasi AJAX Create dengan Toast Feedback:** Mengirim data form via Fetch API method `POST` dengan proteksi `X-CSRFToken`, menutup modal otomatis, menampilkan notifikasi toast (sukses/gagal), dan me-*refresh* daftar timeline seketika.
- **Pertahanan XSS Berlapis:** Menerapkan *client-side escaping* (`escapeHtml()`) dan *server-side sanitization* (`strip_tags()` dan `ValidationError`) pada method `clean_institution` dan `clean_degree` di `EducationForm`.
- **Pembuatan dan Penyesuaian Unit Tests:** Menyesuaikan kelas `EducationTest` di `tests.py` untuk menguji kerangka AJAX, endpoint JSON, fitur search, otorisasi RBAC, dan sanitasi XSS (22 unit tests lulus 100%).

---

### Tugas 5

1. **Jelaskan apa itu debouncing dan mengapa teknik ini penting diterapkan pada fitur pencarian yang menggunakan AJAX!**

   **Pengertian:** *Debouncing* adalah teknik yang menunda eksekusi suatu fungsi sampai beberapa waktu tertentu dari terakhir kali fungsi/event tersebut dipicu. Contoh mekanisme ini diterapkan dalam fitur pencarian dengan memanfaatkan *timer* (`setTimeout`) dan membatalkan *timer* sebelumnya (`clearTimeout`) setiap kali ada input karakter baru sebelum jeda waktu yang ditentukan berakhir.
   
   Tanpa debouncing, setiap kali pengguna mengetik satu karakter (event `input`), browser akan langsung mengirimkan satu HTTP request ke backend. Jika pengguna mengetik kata `"Universitas Indonesia"` (21 karakter), server akan menerima 21 request dalam beberapa detik. Dengan debouncing, request hanya dikirim 1 kali saat pengguna selesai mengetik. Selain itu, ada kemungkinan terjadinya *race condition* yang disebabkan oleh latensi jaringan dan server yang telat memproses request sesuai urutan.

2. **Jelaskan fungsi dari penggunaan await ketika kita menggunakan fetch()! Apa yang akan terjadi jika kita tidak menggunakan await?**

   `await` digunakan di dalam fungsi `async` untuk menjeda eksekusi baris kode berikutnya sampai objek `Promise` yang dihasilkan oleh operasi asinkronus (misalnya pemanggilan `fetch()` atau `.json()`) selesai dan mengembalikan nilai aslinya berupa objek `Response` atau data JSON.
   
   **Apa yang terjadi jika tidak menggunakan `await`?**
   - Variabel yang menampung hasil pemanggilan tidak akan berisi objek data, melainkan objek `Promise` yang masih berstatus *pending*.
   - Ketika mencoba mengakses properti atau membaca data, kode akan langsung mengalami kegagalan/error atau menghasilkan nilai `undefined` karena data dari server belum selesai diambil.

3. **Jelaskan apa itu serangan XSS (Cross-Site Scripting) dan mengapa data yang ditampilkan melalui AJAX/JavaScript lebih rentan terhadap serangan ini daripada data yang ditampilkan langsung melalui template Django!**

   *Cross-Site Scripting* (XSS) adalah jenis kerentanan keamanan web di mana penyerang berhasil menyuntikkan skrip berbahaya ke dalam konten halaman web yang dapat dipercaya. Ketika korban membuka halaman tersebut, skrip tersebut akan dieksekusi oleh browser korban, memungkinkan penyerang mencuri *session cookie* atau token autentikasi milik korban.

   **Mengapa AJAX/JavaScript lebih rentan dibandingkan dengan template Django?**
   - Secara bawaan, template Django secara otomatis melakukan *HTML escaping* pada setiap variabel yang dirender di server. Karakter sensitif seperti `<`, `>`, `&`, `"`, dan `'` otomatis diubah menjadi entitas HTML aman (`&lt;`, `&gt;`, dsb), sehingga aman dari injeksi script biasa.
   - Pada pola AJAX, data diterima dari server dalam bentuk teks mentah (JSON). Ketika JavaScript merender data tersebut ke antarmuka menggunakan properti seperti `element.innerHTML = completeHtml`, browser akan mem-parsing string tersebut langsung sebagai elemen HTML. Jika data input user mengandung tulisan seperti `<img src="x" onerror="fetch('https://iniwebjahat.com/hahahaha')">` dan tidak disanitasi, browser akan langsung memicu *event handler* tersebut dan mengeksekusi skripnya.

---

## AI Disclosure Week 5

Dalam pengerjaan *Individual Assignment* 5 ini, saya berkolaborasi secara interaktif dengan asisten AI (Google Antigravity IDE dan Gemini 3.8 Flash) menggunakan pendekatan *pair-programming* yang bertahap dan kritis.

* **Link Gemini** : https://share.gemini.google/07eKpQ1N7d6k
* **Strategi Prompting**: Saya menerapkan strategi *step-by-step modular prompting*. Tugas dipecah menjadi langkah-langkah terpisah: mulai dari penyesuaian backend JSON, pembuatan kerangka DOM dan *debouncing*, pembuatan modal form berbasis Popover API, integrasi Fetch API POST dengan CSRF dan Toast, hingga sanitasi XSS. Setiap kali AI memberikan saran kode, saya tidak langsung menerapkannya, melainkan menelaah dan mengonfirmasikannya terlebih dahulu dengan kode proyek lokal saya.
* **Bagian yang Dibantu AI**: AI membantu dalam memberikan pemahaman konseptual mendalam tentang cara kerja *event debouncing* dengan `setTimeout`/`clearTimeout`, pola dasar pengiriman form menggunakan `FormData` dan header `X-CSRFToken` pada Fetch API, serta draf awal pengujian unit test di `tests.py`.
* **Analisis Kritis Keterbatasan AI & Perbaikan Manual yang Dilakukan**:
  1. *Ketidaktepatan Desain HTML & CSS*: Saran awal dari AI web cenderung menebak class CSS generik Bootstrap (seperti `btn btn-primary`, `project-form-modal__dialog`, `edu-card`) yang tidak ada di `style.css` portofolio saya. Saya mengoreksi AI dan secara manual mempertahankan class CSS asli (`.edu-timeline__item`, `.edu-timeline__connector`, `.project-form-modal__backdrop`, dsb) agar desain timeline tidak rusak.
  2. *Komponen Interaktif Star & Hapus yang Terhapus*: AI sempat menyarankan penggantian tombol interaktif star menjadi teks statis biasa, serta mengubah tombol Hapus menjadi tag `<a>` (GET). Saya secara kritis mengoreksi ini karena operasi hapus di Django wajib menggunakan method POST yang aman dengan token CSRF, dan interaksi bintang harus tetap terhubung ke backend.
  3. *Penanganan Validasi XSS pada ModelForm*: AI awalnya hanya menyarankan `strip_tags()` biasa tanpa melempar `ValidationError` jika teks yang tersisa kosong. Saya menanyakan dan menambahkan validasi eksplisit `ValidationError` agar input yang seluruhnya berisi tag HTML jahat (seperti `<script></script>`) ditolak dengan status HTTP 400 Bad Request.

---

## Progress Mingguan Week 4

- **Penyelesaian Tutorial 4**
- **Implementasi Autentikasi dan Cookies:** Menambahkan fitur Register, Login, Logout serta menampilkan waktu terakhir login (`last_login`) pengguna menggunakan cookies.
- **Penambahan Relasi ManyToMany (Fitur Star):** Menambahkan field `starred_by` pada model `Experience` dan `Education` agar pengguna terdaftar dapat memberi interaksi bintang.
- **Implementasi Role-based Access Control:** Membatasi fitur manipulasi data sesuai peran pengguna (Guest, User, Editor, dan Superuser). Superuser memiliki hak penuh (CRUD), Editor hanya dapat melakukan fungsi pembaruan data (Update), pengguna biasa dapat memberi interaksi bintang, dan pengunjung (*guest*) hanya dapat membaca data.

---

## AI Disclosure Week 4

Dalam pengerjaan *Individual Assignment* 4 kali ini, saya mematuhi instruksi modul dan menambahkan logika otorisasi tingkat lanjut (termasuk implementasi peran Editor) menggunakan bantuan asisten AI (Google Antigravity IDE / Gemini 3.1 Pro).

* **Strategi Prompting**: Saya menggunakan pendekatan *context-based prompting* dengan memberikan narasi kondisi awal model proyek saya (`Experience` dan `Education`) serta melampirkan *screenshot* panduan soal tugas. Kami berdiskusi layaknya *pair-programming* untuk menerjemahkan instruksi pada modul (yang tadinya memakai contoh model generik `Project`) agar bisa diadaptasi secara langsung ke dalam struktur spesifik portofolio saya.
* **Bagian yang Dibantu AI**: AI sangat membantu pada tahap merumuskan *server-side validation* untuk memverifikasi keanggotaan pengguna di grup `Editor` (`request.user.groups.filter(name='Editor').exists()`), menerapkan logika *conditional rendering* pada UI template untuk menampilkan/menyembunyikan tombol sesuai hak akses, serta merancang fungsionalitas komponen tombol SVG berwarna *cyber-neon* untuk fitur interaktif *Star*.
* **Refleksi Penggunaan AI**: AI sangat membantu memecah belah kebingungan saya mengenai logika sistem autentikasi bawaan Django. Namun, instruksi awal dari AI sering kali masih berupa template umum (seperti menggunakan teks dasar untuk *button*), sehingga saya secara kritis harus mengarahkan AI untuk memoles komponen UI-nya agar selaras dengan estetika *modern* dari *website* saya dan memastikan kode *backend*-nya tetap aman dari kebocoran data (misalnya dengan menggunakan *natural foreign keys*).

---

## Progress Mingguan Week 3

- **Penyelesaian Tutorial 3:** Mengikuti alur dan instruksi dari Tutorial 3.
- **Implementasi CRUD pada Experience:** Menambahkan fitur *Create, Read, Update,* dan *Delete* untuk model `Experience`.
- **Penambahan Fitur Pencarian:** Menambahkan fitur filter/pencarian (*search filter*) pada halaman `Experience`.
- **Pembuatan Unit Test:** Menambahkan *CRUD test* untuk fitur `Experience` demi memastikan fungsi berjalan dengan baik.
- **Penambahan Character Counter pada Form Experience:** Menambahkan *character counter* pada form *add experience*.

---

### Tugas 3

1. **Jelaskan mengapa kita menggunakan `ModelForm` pada Django alih-alih membuat form HTML secara manual. Selain itu, jelaskan pula mengapa kita diwajibkan menambahkan `{% csrf_token %}` pada form tersebut!**

   Kita menggunakan `ModelForm` karena lebih praktis dan efisien. Kita tidak perlu menulis setiap elemen dalam `<form>` di HTML. Django akan otomatis membaca atribut dari model yang sudah ada dan membuatkan form yang sesuai, lengkap dengan sistem validasinya (seperti tipe data, batasan panjang teks, required, dll). Hal ini membuat kode lebih bersih, meminimalisasi human error, dan sangat mudah di-maintain jika sewaktu-waktu modelnya berubah.
   
   Sementara itu, `{% csrf_token %}` wajib ditambahkan demi keamanan untuk mencegah serangan *Cross-Site Request Forgery* (CSRF). Token rahasia ini memastikan bahwa *request* berupa modifikasi data (seperti POST, PUT, DELETE) benar-benar berasal dari website kita sendiri, bukan dari website lain yang mencoba membajak sesi pengguna.

2. **Pada Tutorial 03, kita membahas format data JSON dan XML. Mengapa JSON lebih disukai dalam pengembangan aplikasi web modern dibandingkan XML?**

   JSON lebih disukai karena strukturnya jauh lebih sederhana, ringan, dan ringkas. Tidak seperti XML, format JSON menggunakan *key-value* (*dictionary*). Karena ukurannya yang lebih kecil, proses transfer data juga menjadi lebih cepat.

3. **Jelaskan alur yang terjadi saat kamu menggunakan fungsi *view* untuk mengembalikan data portofoliomu dalam bentuk JSON. Mengapa kita perlu melakukan proses *serialization* pada model Django sebelum datanya dikirim?**

   **Alur:** Di portofolioku, misalkan ketika URL `/experience/json/` diakses, `urls.py` akan memanggil fungsi view `get_experience_json`. Di dalam fungsi tersebut, data dari database diambil menggunakan `Experience.objects.all()`. Kemudian, data-data tersebut dikonversi menjadi format JSON dengan menggunakan `serializers.serialize("json", experience_list)`. Data JSON tersebut baru dikirim kembali lewat `HttpResponse` dengan *content-type* `"application/json"`.

   **Alasan Serialization:** Objek yang diambil dari database (seperti objek model `Experience` dan `Education`) bentuk aslinya adalah *Python Objects*. Format objek Python ini tidak bisa langsung dikirim begitu saja melalui protokol HTTP untuk dibaca oleh browser. Jadi, kita perlu menggunakan *serialization* untuk menerjemahkan objek Python tersebut menjadi format yang universal, seperti JSON.

---

## AI Disclosure Week 3

Dalam pengerjaan Tugas Individu 3 kali ini, saya mengerjakan instruksi yang diberikan secara bertahap (per poin) dengan bantuan AI Gemini 3.1 Pro. Saya melakukan penambahan fitur CRUD (*Create, Read, Update, Delete*) pada aplikasi `main` dan menyelesaikan beberapa *checklist* tugas dengan bantuan AI.

* **Ringkasan Percakapan dengan AI**: https://share.gemini.google/U0ftq0XJbHay
* **Strategi Prompting**: Pada tugas kali ini, saya menerapkan pendekatan *step-by-step prompting* yang sangat terstruktur. Saya memecah instruksi dari tutorial satu per satu ke AI. Setelah AI memberikan solusi untuk satu poin, saya mengimplementasikannya ke kode saya, menyesuaikan sesuai kebutuhan dan mengoreksi kode yang kurang sesuai, melakukan *cross-check*, dan baru melangkah ke poin instruksi selanjutnya.

---

### Tugas 2

1. **Jelaskan alur yang terjadi ketika pengguna membuka halaman portofolio baru, mulai dari permintaan yang diterima proyek hingga data ditampilkan pada browser. Dalam jawabanmu, jelaskan peran `urls.py` proyek, `urls.py` aplikasi, `view`, `model`, dan `template`.**

   Alur yang terjadi ketika pengguna membuka halaman baru (misalnya page *Education*):
   * Pengguna mengklik tautan atau mengetikkan URL di browser. Browser kemudian mengirimkan *HTTP Request* ke server Django.
   * `urls.py` bertindak sebagai *router* utama. Ketika menerima request, file ini akan membaca URL tersebut dan meneruskannya ke aplikasi `main`.
   * `urls.py` pada aplikasi `main` mencocokkan rute spesifik yang diminta (yaitu `"education/"`). Begitu sesuai, `urls.py` pada aplikasi `main` memanggil fungsi yang ada di `views.py`, yaitu `show_education`.
   * Fungsi tersebut bertindak sebagai pengatur halaman yang ingin dituju. Pada fungsi `show_education(request)`, view menghubungi `model` untuk mengambil data dari database.
   * Model bertugas mengelola data dan struktur tabel database. Model mengambil data riwayat pendidikan dari database SQLite lalu menyerahkannya kembali ke view.
   * Data yang didapat kemudian dimasukkan oleh view, lalu dikirim ke template `education.html` menggunakan fungsi `render()` di `views.py`.
   * `education.html` memproses data tersebut dan menampilkannya secara dinamis ke kerangka halaman. Halaman HTML yang sudah terisi data dikirim balik oleh server ke browser pengguna sebagai *HTTP Response*, sehingga pengguna bisa melihat halaman Education di layar.

2. **Mengapa data untuk bagian portofolio baru sebaiknya disimpan pada model dan tidak ditulis langsung di dalam template? Jelaskan dampaknya terhadap kemudahan pemeliharaan dan pengembangan aplikasi.**

   Menyimpan data di model jauh lebih baik daripada *hardcode* di HTML karena:
   * Agar ada pemisahan tanggung jawab sesuai prinsip SRP, yang di mana HTML hanya fokus pada urusan tampilan visual, sedangkan model berfokus pada urusan penyimpanan dan pengelolaan data.
   * Jika data ditulis langsung di HTML, setiap kali kita ingin menambah, mengedit, atau menghapusnya, kita harus membuka kodingan HTML secara manual. Dengan model, kita bisa mengelola data dengan lebih praktis.
   * Data yang tersimpan di model bersifat fleksibel dan bisa digunakan ulang (*reusable*). Misalnya, data pendidikan yang sama bisa kita tampilkan sebagai ringkasan di homepage, diurutkan, difilter, atau diubah menjadi format lain jika di kemudian hari ingin dihubungkan ke aplikasi lain.

3. **Apa perbedaan fungsi `makemigrations` dan `migrate` pada Django? Berikan contoh perubahan model yang mengharuskanmu menjalankan kedua perintah tersebut.**

   * `makemigrations` berfungsi untuk mencatat perubahan yang kita buat pada file `models.py`, lalu menyimpannya sebagai file baru di folder `migrations/` (misalnya file `0003_education.py`). Perintah ini hanya menyiapkan instruksi perubahannya saja dan belum mengubah isi database.
   * `migrate` berfungsi untuk menerapkan instruksi yang ada di file tersebut ke dalam database. Django akan membaca file migrasi dan mengeksekusi perintah SQL ke database fisik.
   
   **Contoh Perubahan Model:**  
   Ketika saya membuat model baru `Education` di `main/models.py` (dengan atribut nama institusi, gelar, IPK, waktu mulai, dan waktu selesai):
   1. Database SQLite awalnya belum memiliki tabel untuk data tersebut.
   2. Saya menjalankan `python manage.py makemigrations` untuk membuat file rancangan migrasi `0003_education.py`.
   3. Selanjutnya, saya menjalankan `python manage.py migrate` agar tabel `main_education` benar-benar dibuat di dalam database SQLite.
   
   Kedua perintah ini juga wajib dijalankan jika di kemudian hari saya menambah kolom baru (misalnya kolom `description` pada model `Education`), mengubah tipe data suatu kolom, atau menghapus kolom yang sudah ada. 

---

## AI Disclosure Week 2

Dalam pengerjaan Tugas Individu 2 kali ini, saya mengerjakan instruksi yang diberikan secara mandiri disertai sedikit bantuan AI. Saya melakukan penambahan model baru pada aplikasi `main` dan menyesuaikan beberapa bagian pada *website* untuk mengikuti penggunaan model yang telah dibuat.

* **Ringkasan Percakapan dengan AI**: https://share.gemini.google/yWPbjNQfUZ2L
* **Strategi Prompting**: Pada tugas kali ini, saya menerapkan pendekatan *context-based prompting* dan *iterative prompting*. Saya memberikan konteks potongan kode yang relevan (seperti struktur model Django, HTML, dan styling CSS) serta menyampaikan kebutuhan secara bertahap—mulai dari perancangan alur timeline halaman education, pembuatan unit testing, hingga merapikan komentar dan keterbacaan kode.
* **Catatan Tambahan**: Untuk animasi pada *section education*, saya menggunakan bantuan AI Agent (Gemini 3.8 Flash Medium) dari Antigravity untuk memberikan efek animasi pada komponen *timeline*. Serta, saya juga menggunakan AI untuk merapikan kode saya dan menambahkan beberapa keterangan pada kode.
* **Next Project**: Ke depannya, saya berencana merombak *base* tampilan *website* saya yang terinspirasi dari referensi berikut:
  * Referensi Desain: https://www.wallofportfolios.in/portfolios/trushank-mistry/

---

### Tugas 1

1. Ya, dalam merancang struktur HTML, saya menggunakan elemen semantik HTML5 seperti `<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, dan `<footer>`. Elemen-elemen ini sangat membantu dalam membuat *static web* karena memberikan struktur yang mudah dipahami, dimaintain, dan dikelola oleh orang yang membaca kode. Misalnya, saya menggunakan `<section>` untuk menyusun bagian-bagian homepage seperti "Profile" dan "Skills". Selain itu, saya juga menggunakan `<article>` untuk komponen di section skills.

2. Tantangan saya saat mengatur CSS agar *responsive* adalah memastikan susunan *layout* berbasis *grid* dapat ditampilkan dengan mulus menjadi susunan yang rapi di layar kecil seperti *smartphone*. Contoh penerapannya, pada layar *desktop*, *skill card* dibuat dalam *grid* 2 kolom. Namun, pada ukuran layar yang lebih kecil seperti tablet (`max-width: 820px`), saya mengurangi jumlah kolom *grid* menjadi 1. Pada layar *smartphone* yang lebih kecil lagi (`max-width: 480px`), tata letak di dalam kartu itu sendiri saya ubah dari baris (`flex-direction: row`) menjadi kolom (`flex-direction: column`) agar gambar berada di atas teks dan ukuran konten tetap proporsional serta nyaman dibaca.

3. Karena portofolio saat ini masih berupa *static web* murni, batasan utama saat ini adalah repot saat ingin memperbarui konten. Setiap kali saya ingin menambah skill atau proyek baru, saya harus mengedit file HTML secara manual. Untuk selanjutnya, saya berencana menghubungkannya ke database menggunakan Django agar data portofolio bisa ditambah atau diedit langsung lewat browser tanpa perlu utak-atik kodingan lagi.

---

## AI Disclosure Week 1

Dalam pengerjaan tugas individu 1 kali ini, saya membuat section berupa *Skills & Expertise* yang bertujuan untuk menampilkan beberapa keahlian yang sudah saya pelajari. Sebelum menggunakan AI, saya buat sendiri isi-isi yang ingin saya tulis beserta keterangannya yang masih berupa tulisan kasar. Saya hias sesuai imajinasi saya waktu itu, yaitu dengan membuat grid kotak-kotak sederhana pada sesi lab Rabu lalu. Namun setelah itu, saya mencari inspirasi desain *website* dari internet dan juga dari *website* yang dulu pernah saya buat saat SMA. Kemudian, saya menemukan referensi yang cocok dari internet. Lalu, saya meminta bantuan AI (Gemini 3.1 Pro) dengan memasukkan gambar referensi tersebut untuk meng-generate kode HTML dan CSS-nya.

Namun, hasil kode yang dihasilkan AI tidak terlalu sempurna untuk saya. Layout CSS nya belum menyesuaikan elemen yang sudah ada sebelumnya dan tampilannya belum adaptif ketika dibuka di layar HP. Selain itu, link dan path gambarnya masih berupa *placeholder*. Oleh karena itu, saya melakukan perbaikan manual, seperti menyesuaikan font, warna elemen, dan ukuran-ukuran dari elemen di section tersebut, merapikan grid serta tampilan media di style.css, serta mengubah link rujukan di index.html. Selain itu, saya juga memanfaatkan AI untuk membuat animasi elemen-elemen *website*nya.

Terakhir, saya menggunakan AI agent dari Visual Studio Code sendiri untuk membantu merapikan kode yang sebelumnya terlihat berantakan. Pemberian komentar pembatas seperti `<!-- Section: Skills -->` dari AI membantu saya memisahkan antar-*section* agar struktur kode menjadi lebih terorganisasi, rapi, dan mudah dibaca.

Meskipun saya cukup banyak memanfaatkan bantuan AI, saya tetap berusaha mencari tahu dan memahami logika serta cara kerja dari setiap baris kode yang telah di-*generate*. Saya menelusuri bagaimana CSS memengaruhi elemen-elemen yang ada di kode html beserta animasi yang dilakukannya, serta mempelajari tag semantik dan class yang digunakan di HTML. Intinya, AI saya pakai untuk mempercepat proses belajar dan mengoding, sementara konsep ide tetap berada di tangan saya sendiri.

Note: untuk prompting AI sendiri, saya tidak menggunakan strategi prompting secara profesional, saya hanya menyuruh AI dengan prompting sederhana, yaitu "di bagian skills, tolong buat seperti ini yaa", dan juga "tolong beri animasi juga ke elemen-elemennya" lalu AI memberi kode HTML dan CSS nya.
