> BUG:
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
- create chapter: saya ingin nomor chapternya juga bisa diedit (misal 1,0 atau 1,1 atau 2,3)