Nama : Azka Nur Jauhar
NPM : 2506612410
Kelas : PBP B

---

## AI Disclosure

Dalam pengerjaan tugas individu 1 kali ini, saya membuat section berupa *Skills & Expertise* yang bertujuan untuk menampilkan beberapa keahlian yang sudah saya pelajari. Sebelum menggunakan AI, saya buat sendiri isi-isi yang ingin saya tulis beserta keterangannya yang masih berupa tulisan kasar. Saya hias sesuai imajinasi saya waktu itu, yaitu dengan membuat grip kotak-kotak sederhana pada sesi lab Rabu lalu. Namun setelah itu, saya mencari inspirasi desain *website* dari internet dan juga dari *website* yang dulu pernah saya buat saat SMA. Kemudian, saya menemukan referensi yang cocok dari internet. Lalu, saya meminta bantuan AI (Gemini 3.1 Pro) dengan memasukkan gambar referensi tersebut untuk meng-generate kode HTML dan CSS-nya.

Namun, hasil kode yang dihasilkan AI tidak terlalu sempurna untuk saya. Layout CSS nya belum menyesuaikan elemen yang sudah ada sebelumnya dan juga dan tampilannya belum adaptif ketika dibuka di layar HP. Selain itu, link dan path gambarnya masih berupa *placeholder*. Oleh karena itu, saya melakukan perbaikan manual, seperti menyesuaikan font, warna elemen, dan ukuran-ukuran dari elemen di section tersebut, merapikan grid serta tampilan media di style.css, serta mengubah link rujukan di index.html. Selain itu, saya juga memanfaatkan AI untuk membuat animasi elemen-elemen *website*nya.

Terakhir, saya menggunakan AI agent dari Visual Studio Code sendiri untuk membantu merapikan kode yang sebelumnya terlihat berantakan. Pemberian komentar pembatas seperti `<!-- Section: Skills -->` dari AI membantu saya meemisahkan antar-*section* agar struktur kode menjadi lebih terorganisasi, rapi, dan mudah dibaca.

Meskipun saya cukup banyak memanfaatkan bantuan AI, saya tetap berusaha mencari tahu dan memahami logika serta cara kerja dari setiap baris kode yang telah di-*generate*. Saya menelusuri bagaimana CSS memengaruhi elemen-elemen yang ada di kode html beserta animasi yang dilakukannya, serta mempelajari tag semantik dan class yang digunakan di HTML. Intinya, AI saya pakai untuk mempercepat proses belajar dan mengoding, sementara konsep ide tetap berada di tangan saya sendiri.

Note: untuk prompting AI sendiri, saya tidak menggunakan strategi prompting secara profesional, saya hanya menyuruh AI dengan prompting sederhana, yaitu "di bagian skills, tolong buat seperti ini yaa", dan juga "tolong beri animasi juga ke elemen-elemennya" lalu AI memberi kode HTML dan CSS nya.

---

### Tugas 1

1. Ya, dalam merancang struktur HTML, saya menggunakan elemen semantik HTML5 seperti <header>, <nav>, <main>, <section>, <article>, dan <footer>. Elemen-elemen ini sangat membantu dalam membuat *static web* karena memberikan struktur yang mudah dipahami, dimaintain, dan dikelola oleh orang yang membaca kode. Misalnya, saya menggunakan <section> untuk menyusun bagian-bagian homepage seperti "Profile" dan "Skills". Selain itu, saya juga menggunakaan <article> untuk komponen di section skills.

2. Tantangan saya saat mengatur CSS agar *responsive* adalah memastikan susunan *layout* berbasis *grid* dapat ditampilkan dengan mulus menjadi susunan yang rapi di layar kecil seperti *smartphone*. Contoh penerapannya, pada layar *desktop*, *skill card* dibuat dalam *grid* 2 kolom. Namun, pada ukuran layar yang lebih kecil seperti tablet (`max-width: 820px`), saya mengurangi jumlah kolom *grid* menjadi 1. Pada layar *smartphone* yang lebih kecil lagi (`max-width: 480px`), tata letak di dalam kartu itu sendiri saya ubah dari baris (`flex-direction: row`) menjadi kolom (`flex-direction: column`) agar gambar berada di atas teks dan ukuran konten tetap proporsional serta nyaman dibaca.

3. Karena portofolio saat ini masih berupa *static web* murni, batasan utama saat ini adalah repot saat ingin memperbarui konten. Setiap kali saya ingin menambah skill atau proyek baru, saya harus mengedit file HTML secara manual. Untuk selanjutnya, saya berencana menghubungkannya ke database menggunakan Django agar data portofolio bisa ditambah atau diedit langsung lewat browser tanpa perlu utak-atik kodingan lagi.
