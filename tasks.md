> BUG:
- chapter viewer: saat di zoom in/out, ada perpindahan view (page/image), jadi saya ingin saat in/out tetap di page/image yang lagi di baca.
- saya baru menambahkan common code language, dan saya coba gunakan di edit chapter pada komik [http://localhost:3000/comic/120bf3b9-c461-4ac7-adf1-151b66dd7960], terjadi error:
    [Nest] 24500  - 10/16/2026, 12:25:56 AM   ERROR [AllExceptionsFilter] HTTP 500 Error: 
    Invalid `prisma.languages.create()` invocation:

    The provided value for the column is too long for the column's type. Column: (not available)
    InternalServerErrorException: 
    Invalid `prisma.languages.create()` invocation:

    The provided value for the column is too long for the column's type. Column: (not available)
        at editChapter (D:\komify\backend\dist\main.js:61462:17)
        at processTicksAndRejections (native:7:39).

> IMPROVE:
- detail comic > chapter: tambahkan fitur download chapter/comic.
- edit comic: cover bisa direplase (upload cover baru atau ambil gambar dari chapter).
- random comic: saya ingin sistem randomnya tidak termasuk komik yang statusnya not complete.
- detail chapter > chapter section: bikin fungsi untuk pengurutan chapter (terbaru/A-Z).
- upload page: setelah sukses upload, halaman di refresh bukan ke homepage.
- upload page > modal extract: perbaiki layout, tingginya input fix.
- upload page > modal extract: tambahkan 2 input chapter (1,0) [main, submain], di setiap input url extract (otomatis bertamah: 1,0 lalu 2,0 dan seterusnya), dan tmabhkan input title chapternya.
- upload page > extract: jika urlnya lebih dari 1, kasih progressnya di notif.
- homepage: urutannya update dulu baru created.
- upload page > chapter section: setiap chapter saya ingin ada preview image/page pertama dari setiap chapter.
- [new feature] history reading.
- settings > dashboard: tambahkan rating