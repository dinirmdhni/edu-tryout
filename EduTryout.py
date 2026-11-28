"""
EDU TRYOUT
Sistem Informasi Pendaftaran dan Pengelolaan Tryout Pendidikan Berbasis Konsol

Persiapan:
1. Install Python.
2. Install driver PostgreSQL:
       pip install psycopg2-binary
3. Pastikan database dan seluruh tabel Edu Tryout sudah dibuat di pgAdmin.
4. Sesuaikan konfigurasi koneksi database dengan PostgreSQL lokal.
5. Jalankan:
       python EduTryout.py

Catatan:
- Verifikasi pembayaran dilakukan manual oleh admin setelah mengecek bukti transfer
  dan rekening lembaga di luar aplikasi.
"""

import email

import psycopg2
from datetime import datetime
import os
import re


def koneksi_database():
    """Menghubungkan Python dengan database PostgreSQL."""
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="EduTryout",
            user="postgres",
            password="dini19",
            port="5432"
        )
        return conn
    except psycopg2.Error:
        print("Gagal terhubung ke database.")
        print("Periksa konfigurasi dan pastikan PostgreSQL sedang berjalan.")
        return None


def bersihkan_layar():
    """Membersihkan tampilan terminal."""
    os.system("cls" if os.name == "nt" else "clear")


def jalankan_query(query, data=None, ambil_data=False):
    """Menjalankan perintah SQL dan mengembalikan hasil jika diperlukan."""
    conn = koneksi_database()

    if conn is None:
        return None

    try:
        with conn.cursor() as cur:
            cur.execute(query, data)

            if ambil_data:
                hasil = cur.fetchall()
            else:
                hasil = True

        conn.commit()
        return hasil

    except psycopg2.Error:
        conn.rollback()
        print("Maaf, terjadi kendala saat memproses data.")
        print("Silakan periksa kembali data atau coba beberapa saat lagi.")
        return None

    finally:
        conn.close()


def garis():
    print("=" * 55)


def jeda():
    input("\nTekan ENTER untuk melanjutkan...")


def input_teks(teks, boleh_batal=False):
    """Meminta teks yang wajib diisi."""
    while True:
        data = input(teks).strip()

        if boleh_batal and data == "0":
            return None
        elif data:
            return data

        print("Input tidak boleh kosong. Silakan isi kembali.")


def input_email(boleh_batal=False):
    while True:
        email = input("Email        : ").strip()

        if boleh_batal and email == "0":
            return None

        pola_email = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

        if re.fullmatch(pola_email, email):
            return email

        print("Format email tidak valid.")
        print("Contoh: nama@gmail.com atau nama@yahoo.com")


def input_password(boleh_batal=False):
    """Memeriksa panjang minimum password."""
    while True:
        password = input("Password     : ").strip()

        if boleh_batal and password == "0":
            return None

        elif len(password) >= 6:
            return password

        print("Password minimal terdiri dari 6 karakter.")


def input_angka(teks, boleh_batal=False):
    """Meminta input berupa bilangan bulat."""
    while True:
        data = input(teks).strip()

        if boleh_batal and data == "0":
            return None

        try:
            return int(data)
        except ValueError:
            print("Input harus berupa angka. Silakan coba lagi.")


def input_harga(teks, boleh_batal=False):
    while True:
        harga = input(teks).strip()

        if boleh_batal and harga == "0":
            return None

        if harga.isdigit() and int(harga) >= 10000:
            return int(harga)

        print("Harga paket minimal Rp10.000.")


def input_durasi(teks, boleh_batal=False):
    while True:
        durasi = input(teks).strip()

        if boleh_batal and durasi == "0":
            return None

        if durasi.isdigit() and int(durasi) >= 10:
            return int(durasi)

        print("Durasi paket minimal 10 menit.")


def input_pilihan(teks, pilihan_valid):
    """Meminta pilihan sampai pengguna memasukkan pilihan yang benar."""
    while True:
        pilihan = input(teks).strip()
        if pilihan in pilihan_valid:
            return pilihan
        print(
            "Pilihan tidak tersedia. "
            f"Masukkan salah satu pilihan: {', '.join(pilihan_valid)}."
        )


def input_teks_huruf(teks, boleh_batal=False):
    while True:
        data = input(teks).strip()

        if boleh_batal and data == "0":
            return None

        if not data:
            print("Input tidak boleh kosong.")
        elif not any(huruf.isalpha() for huruf in data):
            print("Input harus mengandung huruf.")
        else:
            return data
        

def input_nama(boleh_batal=False):
    while True:
        nama = input("Nama lengkap : ").strip()

        if boleh_batal and nama == "0":
            return None
        elif not nama:
            print("Nama lengkap tidak boleh kosong.")
        elif not all(huruf.isalpha() or huruf.isspace() for huruf in nama):
            print("Nama hanya boleh berisi huruf dan spasi.")
        else:
            return nama
        

def email_sudah_digunakan(email):
    """Memeriksa apakah email sudah terdaftar tanpa membedakan huruf besar/kecil."""
    hasil = jalankan_query(
        "SELECT id_pengguna FROM pengguna WHERE LOWER(email) = LOWER(%s)",
        (email,),
        True
    )

    if hasil is None:
        return None

    return len(hasil) > 0


def username_sudah_digunakan(username):
    """Memeriksa apakah username sudah terdaftar tanpa membedakan huruf besar/kecil."""
    hasil = jalankan_query(
        "SELECT id_pengguna FROM pengguna WHERE LOWER(username) = LOWER(%s)",
        (username,),
        True
    )

    if hasil is None:
        return None

    return len(hasil) > 0


# =========================================================
# REGISTRASI DAN LOGIN
# =========================================================

def registrasi_peserta():
    bersihkan_layar()
    garis()
    print("REGISTRASI PESERTA")
    garis()
    print("Ketentuan:")
    print("- Semua data wajib diisi.")
    print("- Gunakan format email yang benar.")
    print("- Password minimal 6 karakter.\n")

    nama = input_nama()
    email = input_email()
    username = input_teks("Username     : ")
    password = input_password()

    email_duplikat = email_sudah_digunakan(email)
    if email_duplikat is None:
        return
    if email_duplikat:
        print("Email sudah terdaftar. Silakan gunakan email lain.")
        return

    username_duplikat = username_sudah_digunakan(username)
    if username_duplikat is None:
        return
    if username_duplikat:
        print("Username sudah digunakan. Silakan gunakan username lain.")
        return


    query = """
        INSERT INTO pengguna
        (nama_pengguna, email, username, password, id_role)
        VALUES (%s, %s, %s, %s, %s)
  """

    berhasil = jalankan_query(
        query,
        (nama, email, username, password, 3)
   )

    if berhasil is not None:
        print("\nRegistrasi berhasil!")
        print("Akun kamu sudah terdaftar sebagai Peserta.")
        print("Silakan login menggunakan username dan password.")


def login():
    bersihkan_layar()
    garis()
    print("LOGIN EDU TRYOUT")
    garis()

    username = input_teks("Username : ")
    password = input_teks("Password : ")

    query = """
        SELECT p.id_pengguna, p.nama_pengguna, p.username,
               r.nama_role, p.id_role
        FROM pengguna p
        JOIN role r ON p.id_role = r.id_role
        WHERE p.username = %s AND p.password = %s
    """

    hasil = jalankan_query(query, (username, password), True)

    if hasil:
        pengguna = hasil[0]
        print("\nLogin berhasil. Selamat datang,", pengguna[1])
        return {
            "id_pengguna": pengguna[0],
            "nama": pengguna[1],
            "username": pengguna[2],
            "role": pengguna[3],
            "id_role": pengguna[4]
        }

    if hasil is not None:
        print("Username atau password salah.")
    return None


# =========================================================
# FUNGSI PESERTA
# =========================================================

def tampilkan_paket():
    garis()
    print("DAFTAR PAKET TRYOUT")
    garis()

    query = """
        SELECT p.id_paket, p.nama_paket, p.deskripsi_paket,
               p.harga_paket, p.durasi_waktu, u.nama_pengguna
        FROM paket_tryout p
        JOIN pengguna u ON p.id_pengguna = u.id_pengguna
        WHERE p.status_aktif = TRUE
        ORDER BY p.id_paket
    """

    hasil = jalankan_query(query, ambil_data=True)

    if hasil is None:
        return

    if not hasil:
        print("Belum ada paket tryout.")
        return

    for paket in hasil:
        print(f"\nID Paket       : {paket[0]}")
        print(f"Nama Paket     : {paket[1]}")
        print(f"Deskripsi      : {paket[2]}")
        print(f"Harga          : Rp{paket[3]:,.0f}")
        print(f"Durasi         : {paket[4]} menit")
        print(f"Pengajar       : {paket[5]}")


def daftar_paket(id_pengguna):
    tampilkan_paket()

    print("Masukkan 0 untuk kembali ke menu peserta.")
    id_paket = input_angka("\nMasukkan ID paket yang dipilih: ")

    if id_paket == 0:
        print("Pendaftaran dibatalkan.")
        return

    paket = jalankan_query(
        """
        SELECT id_paket, harga_paket
        FROM paket_tryout
        WHERE id_paket = %s 
          AND status_aktif = TRUE
        """,
        (id_paket,),
        True
    )

    if paket is None:
        return

    if not paket:
        print("Paket tidak ditemukan.")
        return

    sudah_daftar = jalankan_query(
        """
        SELECT id_pendaftaran
        FROM pendaftaran
        WHERE id_pengguna = %s AND id_paket = %s
        """,
        (id_pengguna, id_paket),
        True
    )

    if sudah_daftar is None:
        return

    if sudah_daftar:
        print("Kamu sudah pernah mendaftar pada paket ini.")
        return

    harga = paket[0][1]

    print("\nPilih Metode Pembayaran:")
    print("1. Tunai")
    print("2. Non Tunai")
    print("0. Kembali ke menu peserta")

    pilihan = input_pilihan(
        "Pilih metode pembayaran (1/2/0): ",
        ["1", "2", "0"]
    )

    if pilihan == "0":
        print("Pendaftaran dibatalkan.")
        return
    
    if pilihan == "1":
        metode = "Tunai"
    else:
        metode = "Non Tunai"
        print("\nSilakan transfer melalui layanan bank atau e-wallet.")
        print("Setelah transfer, kirim bukti pembayaran kepada admin.")

    conn = koneksi_database()

    if conn is None:
        return

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO pendaftaran
                (tanggal_pendaftaran, status_pendaftaran,
                id_pengguna, id_paket)
                VALUES (CURRENT_DATE, 'Menunggu', %s, %s)
                RETURNING id_pendaftaran
                """,
                (id_pengguna, id_paket)
            )

            id_pendaftaran = cur.fetchone()[0]

            cur.execute(
                """
                INSERT INTO pembayaran
                (tanggal_pembayaran, jumlah_pembayaran,
                metode_pembayaran, status_pembayaran, id_pendaftaran)
                VALUES (CURRENT_TIMESTAMP, %s, %s, 'Menunggu', %s)
                """,
                (harga, metode, id_pendaftaran)
            )

        conn.commit()

        print("\nPendaftaran berhasil dicatat.")
        print("Status pembayaran: Menunggu verifikasi admin.")

    except psycopg2.Error:
        conn.rollback()
        print("Pendaftaran gagal dicatat.")
        print("Silakan periksa kembali data atau hubungi admin.")

    finally:
        conn.close()


def lihat_pendaftaran(id_pengguna):
    garis()
    print("STATUS PENDAFTARAN DAN PEMBAYARAN")
    garis()

    query = """
        SELECT pt.id_pendaftaran, pk.nama_paket,
               pt.status_pendaftaran, pb.status_pembayaran,
               pb.jumlah_pembayaran
        FROM pendaftaran pt
        JOIN paket_tryout pk ON pt.id_paket = pk.id_paket
        LEFT JOIN pembayaran pb ON pt.id_pendaftaran = pb.id_pendaftaran
        WHERE pt.id_pengguna = %s
        ORDER BY pt.id_pendaftaran
    """

    hasil = jalankan_query(query, (id_pengguna,), True)

    if hasil is None:
        return

    if not hasil:
        print("Kamu belum memiliki pendaftaran.")
        return

    for data in hasil:
        print(f"\nID Pendaftaran : {data[0]}")
        print(f"Paket          : {data[1]}")
        print(f"Status daftar  : {data[2]}")
        print(f"Status bayar   : {data[3] or 'Belum ada pembayaran'}")
        if data[4] is not None:
            print(f"Jumlah bayar   : Rp{data[4]:,.0f}")


def kerjakan_tryout(id_pengguna):
    garis()
    print("MULAI TRYOUT")
    garis()

    query_pendaftaran = """
        SELECT pt.id_pendaftaran, pk.id_paket, pk.nama_paket,
               pk.durasi_waktu
        FROM pendaftaran pt
        JOIN paket_tryout pk ON pt.id_paket = pk.id_paket
        JOIN pembayaran pb ON pt.id_pendaftaran = pb.id_pendaftaran
        WHERE pt.id_pengguna = %s
          AND pt.status_pendaftaran = 'Diterima'
          AND pb.status_pembayaran = 'Berhasil'
          AND pk.status_aktif = TRUE
        ORDER BY pt.id_pendaftaran
    """

    daftar = jalankan_query(
        query_pendaftaran, (id_pengguna,), True
    )

    if daftar is None:
        return

    if not daftar:
        print("Belum ada paket yang dapat dikerjakan.")
        print("Pastikan pembayaran sudah diverifikasi oleh admin.")
        return

    print("Paket yang dapat dikerjakan:")
    for data in daftar:
        print(f"ID Pendaftaran {data[0]} - {data[2]} ({data[3]} menit)")

    id_pendaftaran = input_angka("\nMasukkan ID pendaftaran: ")

    pilihan = None
    for data in daftar:
        if data[0] == id_pendaftaran:
            pilihan = data
            break

    if pilihan is None:
        print("Pendaftaran tidak ditemukan atau belum dapat dikerjakan.")
        return

    # Mencegah pengerjaan ulang pada pendaftaran yang sama.
    pengerjaan_lama = jalankan_query(
        """
        SELECT id_pengerjaan
        FROM pengerjaan_tryout
        WHERE id_pendaftaran = %s
        """,
        (id_pendaftaran,),
        True
    )

    if pengerjaan_lama is None:
        return

    if pengerjaan_lama:
        print("Pengerjaan untuk pendaftaran ini sudah pernah dibuat.")
        return

    id_paket = pilihan[1]

    soal = jalankan_query(
        """
        SELECT id_soal, pertanyaan, pilihan_a, pilihan_b,
               pilihan_c, pilihan_d, kunci_jawaban
        FROM soal
        WHERE id_paket = %s
          AND status_aktif = TRUE
        ORDER BY id_soal
        """,
        (id_paket,),
        True
    )

    if soal is None:
        return

    if not soal:
        print("Belum ada soal untuk paket ini.")
        return

    # Mencatat pengerjaan tryout sebelum peserta menjawab soal.
    hasil_pengerjaan = jalankan_query(
        """
        INSERT INTO pengerjaan_tryout
        (waktu_mulai, waktu_selesai,
        status_pengerjaan, id_pendaftaran)
        VALUES (CURRENT_TIMESTAMP, NULL, %s, %s)
        RETURNING id_pengerjaan
        """,
        ("Sedang Berlangsung", id_pendaftaran),
        True
  )

    if hasil_pengerjaan is None:
        return

    id_pengerjaan = hasil_pengerjaan[0][0]

    print(f"\nPaket: {pilihan[2]}")
    print(f"Jumlah soal: {len(soal)}")
    print("Masukkan jawaban A, B, C, atau D.\n")

    jumlah_benar = 0

    for nomor, data in enumerate(soal, start=1):
        bersihkan_layar()

        id_soal = data[0]
        pertanyaan = data[1]
        pilihan_a = data[2]
        pilihan_b = data[3]
        pilihan_c = data[4]
        pilihan_d = data[5]
        kunci = data[6]

        print(f"\nSoal {nomor}")
        print(pertanyaan)
        print("A.", pilihan_a)
        print("B.", pilihan_b)
        print("C.", pilihan_c)
        print("D.", pilihan_d)

        jawaban = input("Jawaban kamu: ").strip().upper()

        while jawaban not in ["A", "B", "C", "D"]:
            print("Jawaban hanya boleh A, B, C, atau D.")
            jawaban = input("Jawaban kamu: ").strip().upper()

        status_benar = jawaban == kunci

        if status_benar:
            jumlah_benar += 1

        hasil_jawaban = jalankan_query(
            """
            INSERT INTO jawaban
            (jawaban_peserta, status_benar,
            id_pengerjaan, id_soal)
            VALUES (%s, %s, %s, %s)
            """,
            (jawaban, status_benar, id_pengerjaan, id_soal)
        )

        if hasil_jawaban is None:
            return

    jumlah_soal = len(soal)
    jumlah_salah = jumlah_soal - jumlah_benar
    nilai = (jumlah_benar / jumlah_soal) * 100

    # Mengubah status pengerjaan setelah seluruh soal selesai dijawab.
    hasil_update = jalankan_query(
        """
        UPDATE pengerjaan_tryout
        SET waktu_selesai = CURRENT_TIMESTAMP,
            status_pengerjaan = 'Selesai'
        WHERE id_pengerjaan = %s
        """,
        (id_pengerjaan,)
    )

    if hasil_update is None:
        return

    hasil_simpan = jalankan_query(
        """
        INSERT INTO hasil_tryout
        (nilai, jumlah_benar, jumlah_salah, id_pengerjaan)
        VALUES (%s, %s, %s, %s)
        """,
        (nilai, jumlah_benar, jumlah_salah, id_pengerjaan)
    )

    if hasil_simpan is None:
        return

    garis()
    print("TRYOUT SELESAI")
    garis()
    print(f"Jumlah soal  : {jumlah_soal}")
    print(f"Benar        : {jumlah_benar}")
    print(f"Salah        : {jumlah_salah}")
    print(f"Nilai        : {nilai:.2f}")


def lihat_hasil_peserta(id_pengguna):
    garis()
    print("HASIL TRYOUT SAYA")
    garis()

    query = """
        SELECT pk.nama_paket, ht.nilai, ht.jumlah_benar,
               ht.jumlah_salah, pg.waktu_mulai, pg.waktu_selesai
        FROM hasil_tryout ht
        JOIN pengerjaan_tryout pg ON ht.id_pengerjaan = pg.id_pengerjaan
        JOIN pendaftaran pt ON pg.id_pendaftaran = pt.id_pendaftaran
        JOIN paket_tryout pk ON pt.id_paket = pk.id_paket
        WHERE pt.id_pengguna = %s
    """

    hasil = jalankan_query(query, (id_pengguna,), True)

    if hasil is None:
        return

    if not hasil:
        print("Belum ada hasil tryout.")
        return

    for data in hasil:
        print(f"\nPaket          : {data[0]}")
        print(f"Nilai          : {data[1]}")
        print(f"Jumlah benar   : {data[2]}")
        print(f"Jumlah salah   : {data[3]}")
        print(f"Waktu mulai    : {data[4]}")
        print(f"Waktu selesai  : {data[5]}")


def menu_peserta(pengguna):
    while True:
        bersihkan_layar()
        garis()
        print("MENU PESERTA")
        garis()
        print("1. Lihat paket tryout")
        print("2. Daftar paket dan pembayaran")
        print("3. Lihat status pendaftaran")
        print("4. Kerjakan tryout")
        print("5. Lihat hasil tryout")
        print("0. Logout")

        pilihan = input_pilihan(
            "Pilih menu: ", ["1", "2", "3", "4", "5", "0"]
        )

        if pilihan == "1":
            tampilkan_paket()
            jeda()
        elif pilihan == "2":
            daftar_paket(pengguna["id_pengguna"])
            jeda()
        elif pilihan == "3":
            lihat_pendaftaran(pengguna["id_pengguna"])
            jeda()
        elif pilihan == "4":
            kerjakan_tryout(pengguna["id_pengguna"])
            jeda()
        elif pilihan == "5":
            lihat_hasil_peserta(pengguna["id_pengguna"])
            jeda()
        else:
            break


# =========================================================
# FUNGSI PENGAJAR
# =========================================================

def tambah_paket(id_pengajar):
    cek_pengajar = jalankan_query(
        """
        SELECT p.id_pengguna
        FROM pengguna p
        JOIN role r ON p.id_role = r.id_role
        WHERE p.id_pengguna = %s
          AND r.nama_role = 'Pengajar'
        """,
        (id_pengajar,),
        True
    )

    if cek_pengajar is None:
        return

    if not cek_pengajar:
        print("Hanya pengajar yang dapat menambahkan paket.")
        return

    garis()
    print("TAMBAH PAKET TRYOUT")
    print("Masukkan 0 kapan saja untuk kembali ke menu pengajar.")
    garis()

    nama = input_teks_huruf("Nama paket       : ", True)
    if nama is None:
        print("Penambahan paket dibatalkan.")
        return

    deskripsi = input_teks("Deskripsi paket  : ", True)
    if deskripsi is None:
        print("Penambahan paket dibatalkan.")
        return

    print("Masukkan harga tanpa titik atau tulisan Rp (contoh: 30000).")
    harga = input_harga("Harga paket      : ", True)
    if harga is None:
        print("Penambahan paket dibatalkan.")
        return

    durasi = input_durasi("Durasi paket (menit): ", True)
    if durasi is None:
        print("Penambahan paket dibatalkan.")
        return

    hasil = jalankan_query(
        """
        INSERT INTO paket_tryout
        (nama_paket, deskripsi_paket, harga_paket,
        durasi_waktu, id_pengguna)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (nama, deskripsi, harga, durasi, id_pengajar)
    )

    if hasil is not None:
        print("Paket tryout berhasil ditambahkan.")


def nonaktifkan_paket(id_pengajar):
    garis()
    print("NONAKTIFKAN PAKET TRYOUT")
    garis()

    paket = jalankan_query(
        """
        SELECT id_paket, nama_paket
        FROM paket_tryout
        WHERE id_pengguna = %s
          AND status_aktif = TRUE
        ORDER BY id_paket
        """,
        (id_pengajar,),
        True
    )

    if paket is None:
        return

    if not paket:
        print("Belum ada paket aktif.")
        return

    for data in paket:
        print(f"{data[0]}. {data[1]}")

    id_paket = input_angka("\nMasukkan ID paket: ")

    hasil = jalankan_query(
        """
        UPDATE paket_tryout
        SET status_aktif = FALSE
        WHERE id_paket = %s
          AND id_pengguna = %s
          AND status_aktif = TRUE
        RETURNING id_paket
        """,
        (id_paket, id_pengajar),
        True
    )

    if hasil is None:
        return
    if hasil:
        print("Paket berhasil dinonaktifkan.")
    else:
        print("Paket tidak ditemukan atau bukan milik Anda.")


def aktifkan_paket(id_pengajar):
    garis()
    print("AKTIFKAN KEMBALI PAKET TRYOUT")
    garis()

    paket = jalankan_query(
        """
        SELECT id_paket, nama_paket
        FROM paket_tryout
        WHERE id_pengguna = %s
          AND status_aktif = FALSE
        ORDER BY id_paket
        """,
        (id_pengajar,),
        True
    )

    if paket is None:
        return

    if not paket:
        print("Tidak ada paket yang perlu diaktifkan.")
        return

    for data in paket:
        print(f"{data[0]}. {data[1]}")

    id_paket = input_angka("\nMasukkan ID paket: ")

    hasil = jalankan_query(
        """
        UPDATE paket_tryout
        SET status_aktif = TRUE
        WHERE id_paket = %s
          AND id_pengguna = %s
          AND status_aktif = FALSE
        RETURNING id_paket
        """,
        (id_paket, id_pengajar),
        True
    )

    if hasil:
        print("Paket berhasil diaktifkan kembali.")
    elif hasil is not None:
        print("Paket tidak ditemukan atau bukan milik Anda.")


def tambah_soal(id_pengajar):
    garis()
    print("TAMBAH SOAL TRYOUT")
    print("Masukkan 0 kapan saja untuk kembali ke menu pengajar.")
    garis()

    paket = jalankan_query(
        """
        SELECT id_paket, nama_paket
        FROM paket_tryout
        WHERE id_pengguna = %s
          AND status_aktif = TRUE
        ORDER BY id_paket
        """,
        (id_pengajar,),
        True
    )

    if paket is None:
        return

    if not paket:
        print("Kamu belum memiliki paket tryout.")
        return

    for data in paket:
        print(f"{data[0]}. {data[1]}")

    id_paket = input_angka("Pilih ID paket: ", True)

    if id_paket is None:
        print("Penambahan soal dibatalkan.")
        return

    paket_valid = False
    for data in paket:
        if data[0] == id_paket:
            paket_valid = True
            break

    if not paket_valid:
        print("Paket tidak ditemukan atau bukan milikmu.")
        return

    pertanyaan = input_teks("Pertanyaan : ", True)
    if pertanyaan is None:
        print("Penambahan soal dibatalkan.")
        return

    pilihan_a = input_teks("Pilihan A  : ", True)
    if pilihan_a is None:
        print("Penambahan soal dibatalkan.")
        return

    pilihan_b = input_teks("Pilihan B  : ", True)
    if pilihan_b is None:
        print("Penambahan soal dibatalkan.")
        return

    pilihan_c = input_teks("Pilihan C  : ", True)
    if pilihan_c is None:
        print("Penambahan soal dibatalkan.")
        return

    pilihan_d = input_teks("Pilihan D  : ", True)
    if pilihan_d is None:
        print("Penambahan soal dibatalkan.")
        return

    print("\nMasukkan A, B, C, atau D sebagai kunci jawaban.")
    print("Masukkan 0 untuk membatalkan penambahan soal.")

    while True:
        kunci = input("Kunci (A/B/C/D): ").strip().upper()

        if kunci == "0":
            print("Penambahan soal dibatalkan.")
            return

        if kunci in ["A", "B", "C", "D"]:
            break

        print("Kunci jawaban harus A, B, C, atau D.")

    hasil = jalankan_query(
        """
        INSERT INTO soal
        (pertanyaan, pilihan_a, pilihan_b, pilihan_c,
        pilihan_d, kunci_jawaban, id_paket)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        (pertanyaan, pilihan_a, pilihan_b, pilihan_c,
         pilihan_d, kunci, id_paket)
    )

    if hasil is not None:
        print("Soal berhasil ditambahkan.")


def nonaktifkan_soal(id_pengajar):
    garis()
    print("NONAKTIFKAN SOAL")
    garis()

    soal = jalankan_query(
        """
        SELECT s.id_soal, s.pertanyaan, p.nama_paket
        FROM soal s
        JOIN paket_tryout p ON s.id_paket = p.id_paket
        WHERE p.id_pengguna = %s
          AND p.status_aktif = TRUE
          AND s.status_aktif = TRUE
        ORDER BY s.id_soal
        """,
        (id_pengajar,),
        True
    )

    if soal is None:
        return

    if not soal:
        print("Belum ada soal aktif.")
        return

    for data in soal:
        print(f"\nID Soal   : {data[0]}")
        print(f"Pertanyaan: {data[1]}")
        print(f"Paket     : {data[2]}")

    id_soal = input_angka("\nMasukkan ID soal: ")

    hasil = jalankan_query(
        """
        UPDATE soal s
        SET status_aktif = FALSE
        FROM paket_tryout p
        WHERE s.id_paket = p.id_paket
          AND s.id_soal = %s
          AND p.id_pengguna = %s
          AND s.status_aktif = TRUE
        RETURNING s.id_soal
        """,
        (id_soal, id_pengajar),
        True
    )
    if hasil is None:
        return
    if hasil:
        print("Soal berhasil dinonaktifkan.")
    else:
        print("Soal tidak ditemukan atau bukan milik Anda.")


def aktifkan_soal(id_pengajar):
    garis()
    print("AKTIFKAN KEMBALI SOAL")
    garis()

    soal = jalankan_query(
        """
        SELECT s.id_soal, s.pertanyaan, p.nama_paket
        FROM soal s
        JOIN paket_tryout p ON s.id_paket = p.id_paket
        WHERE p.id_pengguna = %s
          AND p.status_aktif = TRUE
          AND s.status_aktif = FALSE
        ORDER BY s.id_soal
        """,
        (id_pengajar,),
        True
    )

    if soal is None:
        return

    if not soal:
        print("Tidak ada soal yang perlu diaktifkan.")
        return

    for data in soal:
        print(f"\nID Soal   : {data[0]}")
        print(f"Pertanyaan: {data[1]}")
        print(f"Paket     : {data[2]}")

    id_soal = input_angka("\nMasukkan ID soal: ")

    hasil = jalankan_query(
        """
        UPDATE soal s
        SET status_aktif = TRUE
        FROM paket_tryout p
        WHERE s.id_paket = p.id_paket
          AND s.id_soal = %s
          AND p.id_pengguna = %s
          AND p.status_aktif = TRUE
          AND s.status_aktif = FALSE
        RETURNING s.id_soal
        """,
        (id_soal, id_pengajar),
        True
    )

    if hasil:
        print("Soal berhasil diaktifkan kembali.")
    elif hasil is not None:
        print("Soal tidak ditemukan atau bukan milik Anda.")


def pantau_hasil_pengajar(id_pengajar):
    garis()
    print("HASIL PESERTA PADA PAKET SAYA")
    garis()

    query = """
        SELECT u.nama_pengguna, pk.nama_paket, ht.nilai,
               ht.jumlah_benar, ht.jumlah_salah
        FROM hasil_tryout ht
        JOIN pengerjaan_tryout pg ON ht.id_pengerjaan = pg.id_pengerjaan
        JOIN pendaftaran pt ON pg.id_pendaftaran = pt.id_pendaftaran
        JOIN pengguna u ON pt.id_pengguna = u.id_pengguna
        JOIN paket_tryout pk ON pt.id_paket = pk.id_paket
        WHERE pk.id_pengguna = %s
    """

    hasil = jalankan_query(query, (id_pengajar,), True)

    if hasil is None:
        return

    if not hasil:
        print("Belum ada hasil peserta pada paketmu.")
        return

    for data in hasil:
        print(f"\nPeserta        : {data[0]}")
        print(f"Paket          : {data[1]}")
        print(f"Nilai          : {data[2]}")
        print(f"Jumlah benar   : {data[3]}")
        print(f"Jumlah salah   : {data[4]}")


def menu_pengajar(pengguna):
    while True:
        bersihkan_layar()
        garis()
        print("MENU PENGAJAR")
        garis()
        print("1. Lihat paket milik saya")
        print("2. Tambah paket tryout")
        print("3. Tambah soal")
        print("4. Pantau hasil peserta")
        print("5. Nonaktifkan paket")
        print("6. Nonaktifkan soal")
        print("7. Aktifkan kembali paket")
        print("8. Aktifkan kembali soal")
        print("0. Logout")

        pilihan = input_pilihan(
            "Pilih menu: ", ["1", "2", "3", "4", "5", "6", "7", "8", "0"]
        )

        if pilihan == "1":
            paket = jalankan_query(
                """
                SELECT id_paket, nama_paket, harga_paket, durasi_waktu
                FROM paket_tryout
                WHERE id_pengguna = %s
                  AND status_aktif = TRUE
                ORDER BY id_paket
                """,
                (pengguna["id_pengguna"],),
                True
            )
            if paket is None:
                pass
            elif paket:
                for data in paket:
                    print(data)
            else:
                print("Belum ada paket.")
            jeda()
        elif pilihan == "2":
            tambah_paket(pengguna["id_pengguna"])
            jeda()
        elif pilihan == "3":
            tambah_soal(pengguna["id_pengguna"])
            jeda()
        elif pilihan == "4":
            pantau_hasil_pengajar(pengguna["id_pengguna"])
            jeda()
        elif pilihan == "5":
            nonaktifkan_paket(pengguna["id_pengguna"])
            jeda()
        elif pilihan == "6":
            nonaktifkan_soal(pengguna["id_pengguna"])
            jeda()
        elif pilihan == "7":
            aktifkan_paket(pengguna["id_pengguna"])
            jeda()
        elif pilihan == "8":
            aktifkan_soal(pengguna["id_pengguna"])
            jeda()
        else:
            break


# =========================================================
# FUNGSI ADMIN
# =========================================================

def lihat_semua_pengguna():
    garis()
    print("DATA PENGGUNA")
    garis()

    hasil = jalankan_query(
        """
        SELECT p.id_pengguna, p.nama_pengguna, p.email,
               p.username, r.nama_role
        FROM pengguna p
        JOIN role r ON p.id_role = r.id_role
        ORDER BY p.id_pengguna
        """,
        ambil_data=True
    )

    if hasil is None:
        return

    if not hasil:
        print("Belum ada data pengguna.")
        return

    for data in hasil:
        print(
            f"ID: {data[0]} | Nama: {data[1]} | "
            f"Email: {data[2]} | Username: {data[3]} | Role: {data[4]}"
        )


def tambah_pengajar():
    garis()
    print("TAMBAH AKUN PENGAJAR")
    garis()
    print("Ketentuan:")
    print("- Semua data wajib diisi.")
    print("- Gunakan format email yang benar.")
    print("- Password minimal 6 karakter.\n")
    print("- Masukkan 0 kapan saja untuk kembali ke menu admin.\n")

    nama = input_nama(True)
    if nama is None:
        print("Penambahan akun pengajar dibatalkan.")
        return

    email = input_email(True)
    if email is None:
        print("Penambahan akun pengajar dibatalkan.")
        return

    username = input_teks("Username     : ", True)
    if username is None:
        print("Penambahan akun pengajar dibatalkan.")
        return

    password = input_password(True)
    if password is None:
        print("Penambahan akun pengajar dibatalkan.")
        return

    email_duplikat = email_sudah_digunakan(email)
    if email_duplikat is None:
        return
    if email_duplikat:
        print("Email sudah terdaftar. Gunakan email lain.")
        return

    username_duplikat = username_sudah_digunakan(username)
    if username_duplikat is None:
        return
    if username_duplikat:
        print("Username sudah digunakan. Gunakan username lain.")
        return


    hasil = jalankan_query(
        """
            INSERT INTO pengguna
            (nama_pengguna, email, username, password, id_role)
            VALUES (%s, %s, %s, %s, 2)
       """,
        (nama, email, username, password)
    )

    if hasil is not None:
        print("Akun pengajar berhasil ditambahkan.")


def verifikasi_pembayaran():
    garis()
    print("VERIFIKASI PEMBAYARAN")
    garis()

    query = """
        SELECT pb.id_pembayaran, pt.id_pendaftaran,
               u.nama_pengguna, pk.nama_paket,
               pb.jumlah_pembayaran, pb.metode_pembayaran,
               pb.status_pembayaran
        FROM pembayaran pb
        JOIN pendaftaran pt ON pb.id_pendaftaran = pt.id_pendaftaran
        JOIN pengguna u ON pt.id_pengguna = u.id_pengguna
        JOIN paket_tryout pk ON pt.id_paket = pk.id_paket
        WHERE pb.status_pembayaran = 'Menunggu'
        ORDER BY pb.id_pembayaran
    """

    hasil = jalankan_query(query, ambil_data=True)

    if hasil is None:
        return

    if not hasil:
        print("Tidak ada pembayaran yang menunggu verifikasi.")
        return

    for data in hasil:
        print(f"\nID Pembayaran : {data[0]}")
        print(f"ID Pendaftaran: {data[1]}")
        print(f"Peserta       : {data[2]}")
        print(f"Paket         : {data[3]}")
        print(f"Jumlah bayar  : Rp{data[4]:,.0f}")
        print(f"Metode        : {data[5]}")
        print(f"Status        : {data[6]}")

    id_pembayaran = input_angka(
        "\nMasukkan ID pembayaran yang diperiksa: "
    )

    pembayaran = None
    for data in hasil:
        if data[0] == id_pembayaran:
            pembayaran = data
            break

    if pembayaran is None:
        print("ID pembayaran tidak ditemukan dalam daftar.")
        return

    print("\nPastikan pembayaran sudah diperiksa terlebih dahulu.")

    if pembayaran[5] == "Tunai":
        print("Pastikan uang sudah diterima secara langsung.")
    else:
        print("Pastikan bukti transfer sudah diperiksa.")
        print("Pastikan dana sudah masuk melalui layanan bank atau e-wallet.")

    print("\n1. Terima pembayaran")
    print("2. Tolak pembayaran")

    pilihan = input_pilihan("Pilih tindakan: ", ["1", "2"])

    if pilihan == "1":
        status_bayar = "Berhasil"
        status_daftar = "Diterima"
    else:
        status_bayar = "Gagal"
        status_daftar = "Ditolak"

    conn = koneksi_database()

    if conn is None:
        return

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE pembayaran
                SET status_pembayaran = %s
                WHERE id_pembayaran = %s
                  AND status_pembayaran = 'Menunggu'
                """,
                (status_bayar, id_pembayaran)
            )

            if cur.rowcount == 0:
                conn.rollback()
                print("Pembayaran sudah tidak menunggu verifikasi.")
                return

            cur.execute(
                """
                UPDATE pendaftaran
                SET status_pendaftaran = %s
                WHERE id_pendaftaran = %s
                """,
                (status_daftar, pembayaran[1])
            )

        conn.commit()
        print("Status pembayaran dan pendaftaran berhasil diperbarui.")

    except psycopg2.Error:
        conn.rollback()
        print("Verifikasi pembayaran gagal.")
        print("Silakan coba kembali atau periksa koneksi database.")

    finally:
        conn.close()


def menu_admin():
    while True:
        bersihkan_layar()
        garis()
        print("MENU ADMIN")
        garis()
        print("1. Lihat seluruh pengguna")
        print("2. Tambah akun pengajar")
        print("3. Verifikasi pembayaran")
        print("0. Logout")

        pilihan = input_pilihan(
            "Pilih menu: ", ["1", "2", "3", "0"]
        )

        if pilihan == "1":
            lihat_semua_pengguna()
            jeda()
        elif pilihan == "2":
            tambah_pengajar()
            jeda()
        elif pilihan == "3":
            verifikasi_pembayaran()
            jeda()
        else:
            break


# =========================================================
# PROGRAM UTAMA
# =========================================================

def main():
    # Memastikan koneksi database tersedia sebelum menu ditampilkan.
    conn = koneksi_database()

    if conn is None:
        print("Periksa kembali konfigurasi database.")
        return

    conn.close()

    while True:
        bersihkan_layar()
        garis()
        print("EDU TRYOUT")
        print("Sistem Informasi Pendaftaran dan Pengelolaan Tryout")
        garis()
        print("1. Login")
        print("2. Registrasi peserta")
        print("0. Keluar")

        pilihan = input_pilihan("Pilih menu: ", ["1", "2", "0"])

        if pilihan == "1":
            pengguna = login()

            if pengguna:
                if pengguna["role"] == "Peserta":
                    menu_peserta(pengguna)
                elif pengguna["role"] == "Pengajar":
                    menu_pengajar(pengguna)
                elif pengguna["role"] == "Admin":
                    menu_admin()
                else:
                    print("Role pengguna tidak dikenali.")
                    jeda()
            else:
                jeda()

        elif pilihan == "2":
            registrasi_peserta()
            jeda()

        else:
            print("Terima kasih telah menggunakan Edu Tryout.")
            break


if __name__ == "__main__":
    main()
