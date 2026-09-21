Nama       : Azka Nur Jauhar<br>
NPM        : 2506612410<br>
Kelas      : PBP B<br>
Tautan PWS : http://azka-nur-myportofolio.pws.cs.ui.ac.id/

---

## Panduan Menjalankan Proyek (Setup Guide)

1. **Clone repositori dan masuk ke direktori proyek**:
   ```bash
   git clone https://github.com/Otsukaax/myportofolio.git
   cd myportofolio
   ```

2. **Membuat dan mengaktifkan virtual environment**:
   ```bash
   # Windows
   python -m venv env
   .\env\Scripts\activate

   # Linux/macOS
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

5. **Menjalankan server**:
   ```bash
   python manage.py runserver
   ```
   Buka `http://localhost:8000/` pada browser untuk melihat portofolio.

---

## Progress Mingguan Week 3

- **Penyelesaian Tutorial 3:** Mengikuti alur dan instruksi dari Tutorial 3.
- **Implementasi CRUD pada Experience:** Menambahkan fitur *Create, Read, Update,* dan *Delete* untuk model `Experience`.
- **Penambahan Fitur Pencarian:** Menambahkan fitur filter/pencarian (*search filter*) pada halaman `Experience`.
- **Pembuatan Unit Test:** Menambahkan *CRUD test* untuk fitur `Experience` demi memastikan fungsi berjalan dengan baik.
- **Penambahan _Character Counter_ pada _experience form_:** Menambahkan _character counter_ pada _form_ add _experience_.

---

### Tugas 3

1. **Jelaskan mengapa kita menggunakan `ModelForm` pada Django alih-alih membuat form HTML secara manual. Selain itu, jelaskan pula mengapa kita diwajibkan menambahkan `{% csrf_token %}` pada form tersebut!**

   Kita menggunakan `ModelForm` karena lebih praktis dan efisien. Kita tidak perlu menulis setiap elemen dalam `<form>` di HTML. Django akan otomatis membaca atribut dari model yang sudah ada dan membuatkan form yang sesuai, lengkap dengan sistem validasinya (seperti tipe data, batasan panjang teks, required, dll). Hal ini membuat kode lebih bersih, meminimalisasi human error, dan sangat mudah di-maintain jika sewaktu-waktu modelnya berubah.
   
   Sementara itu, `{% csrf_token %}` wajib ditambahkan demi keamanan untuk mencegah serangan *Cross-Site Request Forgery* (CSRF). Token rahasia ini memastikan bahwa *request* berupa modifikasi data (seperti POST, PUT, DELETE) benar-benar berasal dari website kita sendiri, bukan dari website lain yang mencoba membajak sesi pengguna.

2. **Pada Tutorial 03, kita membahas format data JSON dan XML. Mengapa JSON lebih disukai dalam pengembangan aplikasi web modern dibandingkan XML?**

   JSON lebih disukai karena strukturnya jauh lebih sederhana, ringan, dan ringkas. Tidak seperti XML, format JSON menggunakan *key-value* (*dictionary*). Karena ukurannya yang lebih kecil, proses transfer data juga menjadi lebih cepat.

3. **Jelaskan alur yang terjadi saat kamu menggunakan fungsi *view* untuk mengembalikan data portofoliomu dalam bentuk JSON. Mengapa kita perlu melakukan proses *serialization* pada model Django sebelum datanya dikirim?**

   **Alur:** Di portofolioku, misalkan ketika URL `/experience/json/` diakses, `urls.py` akan memanggil fungsi view `get_experience_json`. Di dalam fungsi tersebut, data dari database diambil menggunakan `Experience.objects.all()`. Kemudian, data-data tersebut dikonversi menjadi format JSON dengan menggunakan `serializers.serialize("json", experience_list)`. Data JSON tersebut baru dikirim kembali lewat `HttpResponse` dengan *content-type* `"application/json"`.

   **Alasan *serialization*:** Objek yang diambil dari database (seperti objek model `Experience` dan `Education`) bentuk aslinya adalah *Python Objects*. Format objek Python ini tidak bisa langsung dikirim begitu saja melalui protokol HTTP untuk dibaca oleh browser. Jadi, kita perlu menggunakan *serialization* untuk menerjemahkan objek Python tersebut menjadi format yang universal, seperti JSON.

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
   
   **Contoh Perubahan Model**:
   Ketika saya membuat model baru `Education` di `main/models.py` (dengan atribut nama institusi, gelar, IPK, waktu mulai, dan waktu selesai):
   1. Database SQLite awalnya belum memiliki tabel untuk data tersebut.
   2. Saya menjalankan `python manage.py makemigrations` untuk membuat file rancangan migrasi `0003_education.py`.
   3. Selanjutnya, saya menjalankan `python manage.py migrate` agar tabel `main_education` benar-benar dibuat di dalam database SQLite.
   Kedua perintah ini juga wajib dijalankan jika di kemudian hari saya menambah kolom baru (misalnya kolom `description` pada model `Education`), mengubah tipe data suatu kolom, atau menghapus kolom yang sudah ada. 

## AI Disclosure Week 2

Dalam pengerjaan Tugas Individu 2 kali ini, saya mengerjakan instruksi yang diberikan secara mandiri disertai sedikit bantuan AI. Saya melakukan penambahan model baru pada aplikasi `main` dan menyesuaikan beberapa bagian pada *website* untuk mengikuti penggunaan model yang telah dibuat.

* **Ringkasan Percakapan dengan AI**: https://share.gemini.google/yWPbjNQfUZ2L
* **Strategi Prompting**: Pada tugas kali ini, saya menerapkan pendekatan *context-based prompting* dan *iterative prompting*. Saya memberikan konteks potongan kode yang relevan (seperti struktur model Django, HTML, dan styling CSS) serta menyampaikan kebutuhan secara bertahap—mulai dari perancangan alur timeline halaman education, pembuatan unit testing, hingga merapikan komentar dan keterbacaan kode.
* **Catatan Tambahan**: Untuk animasi pada *section education*, saya menggunakan bantuan AI Agent (Gemini 3.8 Flash Medium) dari Antigravity untuk memberikan efek animasi pada komponen *timeline*. Serta, saya juga menggunakan AI untuk merapikan kode saya dan menambahkan beberapa keterangan pada kode.
* **Next Project**: Ke depannya, saya berencana merombak *base* tampilan *website* saya yang terinspirasi dari referensi berikut:
  * Referensi Desain: https://www.wallofportfolios.in/portfolios/trushank-mistry/

---

### Tugas 1

1. Ya, dalam merancang struktur HTML, saya menggunakan elemen semantik HTML5 seperti `<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, dan `<footer>`. Elemen-elemen ini sangat membantu dalam membuat *static web* karena memberikan struktur yang mudah dipahami, dimaintain, dan dikelola oleh orang yang membaca kode. Misalnya, saya menggunakan `<section>` untuk menyusun bagian-bagian homepage seperti "Profile" dan "Skills". Selain itu, saya juga menggunakaan `<article>` untuk komponen di section skills.

2. Tantangan saya saat mengatur CSS agar *responsive* adalah memastikan susunan *layout* berbasis *grid* dapat ditampilkan dengan mulus menjadi susunan yang rapi di layar kecil seperti *smartphone*. Contoh penerapannya, pada layar *desktop*, *skill card* dibuat dalam *grid* 2 kolom. Namun, pada ukuran layar yang lebih kecil seperti tablet (`max-width: 820px`), saya mengurangi jumlah kolom *grid* menjadi 1. Pada layar *smartphone* yang lebih kecil lagi (`max-width: 480px`), tata letak di dalam kartu itu sendiri saya ubah dari baris (`flex-direction: row`) menjadi kolom (`flex-direction: column`) agar gambar berada di atas teks dan ukuran konten tetap proporsional serta nyaman dibaca.

3. Karena portofolio saat ini masih berupa *static web* murni, batasan utama saat ini adalah repot saat ingin memperbarui konten. Setiap kali saya ingin menambah skill atau proyek baru, saya harus mengedit file HTML secara manual. Untuk selanjutnya, saya berencana menghubungkannya ke database menggunakan Django agar data portofolio bisa ditambah atau diedit langsung lewat browser tanpa perlu utak-atik kodingan lagi.

## AI Disclosure Week 1

Dalam pengerjaan tugas individu 1 kali ini, saya membuat section berupa *Skills & Expertise* yang bertujuan untuk menampilkan beberapa keahlian yang sudah saya pelajari. Sebelum menggunakan AI, saya buat sendiri isi-isi yang ingin saya tulis beserta keterangannya yang masih berupa tulisan kasar. Saya hias sesuai imajinasi saya waktu itu, yaitu dengan membuat grip kotak-kotak sederhana pada sesi lab Rabu lalu. Namun setelah itu, saya mencari inspirasi desain *website* dari internet dan juga dari *website* yang dulu pernah saya buat saat SMA. Kemudian, saya menemukan referensi yang cocok dari internet. Lalu, saya meminta bantuan AI (Gemini 3.1 Pro) dengan memasukkan gambar referensi tersebut untuk meng-generate kode HTML dan CSS-nya.

Namun, hasil kode yang dihasilkan AI tidak terlalu sempurna untuk saya. Layout CSS nya belum menyesuaikan elemen yang sudah ada sebelumnya dan juga dan tampilannya belum adaptif ketika dibuka di layar HP. Selain itu, link dan path gambarnya masih berupa *placeholder*. Oleh karena itu, saya melakukan perbaikan manual, seperti menyesuaikan font, warna elemen, dan ukuran-ukuran dari elemen di section tersebut, merapikan grid serta tampilan media di style.css, serta mengubah link rujukan di index.html. Selain itu, saya juga memanfaatkan AI untuk membuat animasi elemen-elemen *website*nya.

Terakhir, saya menggunakan AI agent dari Visual Studio Code sendiri untuk membantu merapikan kode yang sebelumnya terlihat berantakan. Pemberian komentar pembatas seperti `<!-- Section: Skills -->` dari AI membantu saya meemisahkan antar-*section* agar struktur kode menjadi lebih terorganisasi, rapi, dan mudah dibaca.

Meskipun saya cukup banyak memanfaatkan bantuan AI, saya tetap berusaha mencari tahu dan memahami logika serta cara kerja dari setiap baris kode yang telah di-*generate*. Saya menelusuri bagaimana CSS memengaruhi elemen-elemen yang ada di kode html beserta animasi yang dilakukannya, serta mempelajari tag semantik dan class yang digunakan di HTML. Intinya, AI saya pakai untuk mempercepat proses belajar dan mengoding, sementara konsep ide tetap berada di tangan saya sendiri.

Note: untuk prompting AI sendiri, saya tidak menggunakan strategi prompting secara profesional, saya hanya menyuruh AI dengan prompting sederhana, yaitu "di bagian skills, tolong buat seperti ini yaa", dan juga "tolong beri animasi juga ke elemen-elemennya" lalu AI memberi kode HTML dan CSS nya.