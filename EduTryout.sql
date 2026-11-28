
CREATE TABLE role (
id_role INTEGER PRIMARY KEY,
nama_role VARCHAR(30) NOT NULL
);

INSERT INTO role (id_role, nama_role)
VALUES
(1, 'Admin'),
(2, 'Pengajar'),
(3, 'Peserta');

CREATE TABLE pengguna (
id_pengguna INTEGER PRIMARY KEY,
nama_pengguna VARCHAR(100) NOT NULL,
email VARCHAR(100) UNIQUE NOT NULL,
username VARCHAR(50) UNIQUE NOT NULL,
password VARCHAR(255) NOT NULL,
id_role INTEGER NOT NULL,
FOREIGN KEY (id_role) REFERENCES role(id_role)
);

INSERT INTO pengguna
(id_pengguna, nama_pengguna, email, username, password, id_role)
VALUES
(1, 'Admin EduTryout', 'admin@edutryout.com', 'admin', 'admin123', 1);

INSERT INTO pengguna
(id_pengguna, nama_pengguna, email, username, password, id_role)
VALUES
(2, 'Budi Santoso', 'budi@gmail.com', 'budi', 'budi123', 2),
(3, 'Andi Pratama', 'andi@gmail.com', 'andi', 'andi123', 2),
(4, 'Dewi Lestari', 'dewi@gmail.com', 'dewi', 'dewi123', 2);

INSERT INTO pengguna
(id_pengguna, nama_pengguna, email, username, password, id_role)
VALUES
(5, 'Kayvan Putri', 'kayvan@gmail.com', 'kayvanp', 'putri123', 3),
(6, 'Rizky Ramadhan', 'rizky@gmail.com', 'rizky', 'rizky123', 3),
(7, 'Fransiska Amelia', 'amelia@gmail.com', 'fransiska', 'frans123', 3);


SELECT * FROM role; 
SELECT * FROM pengguna;

CREATE TABLE paket_tryout (
    id_paket INTEGER PRIMARY KEY,
    nama_paket VARCHAR(100) NOT NULL,
    deskripsi_paket TEXT,
    harga_paket NUMERIC(12, 2) NOT NULL CHECK (harga_paket >= 0),
    durasi_waktu INTEGER NOT NULL CHECK (durasi_waktu > 0),
    id_pengguna INTEGER NOT NULL,
	FOREIGN KEY (id_pengguna) REFERENCES pengguna(id_pengguna)
);

INSERT INTO paket_tryout
(id_paket, nama_paket, deskripsi_paket, harga_paket, durasi_waktu, id_pengguna)
VALUES
(1, 'Paket UTBK', 'Latihan soal persiapan UTBK', 50000, 90, 2),
(2, 'Paket Matematika', 'Latihan soal matematika', 30000, 60, 3),
(3, 'Paket Bahasa Indonesia', 'Latihan soal bahasa Indonesia', 25000, 60, 4);

SELECT * FROM paket_tryout;

CREATE TABLE soal (
    id_soal INTEGER PRIMARY KEY,
    pertanyaan TEXT NOT NULL,
    pilihan_a TEXT NOT NULL,
    pilihan_b TEXT NOT NULL,
    pilihan_c TEXT NOT NULL,
    pilihan_d TEXT NOT NULL,
    kunci_jawaban CHAR(1) NOT NULL
    CHECK (kunci_jawaban IN ('A', 'B', 'C', 'D')),
    id_paket INTEGER NOT NULL REFERENCES paket_tryout(id_paket)
);

INSERT INTO soal
(id_soal, pertanyaan, pilihan_a, pilihan_b, pilihan_c, pilihan_d, kunci_jawaban, id_paket)
VALUES
(1, 'Perhatikan pola bilangan berikut: 3, 7, 15, 31, ... Bilangan berikutnya adalah ...',
 '47', '55', '63', '65', 'C', 1),

(2, 'Sebuah barang mengalami kenaikan harga sebesar 20%, kemudian mendapatkan diskon 20% dari harga setelah kenaikan. Jika harga awal barang Rp250.000, berapakah harga akhirnya?',
 'Rp200.000', 'Rp240.000', 'Rp250.000', 'Rp260.000', 'B', 1),

(3, 'Hubungan kata yang paling tepat untuk melengkapi analogi berikut adalah: Dokter : Pasien = Guru : ...',
 'Sekolah', 'Buku', 'Murid', 'Pelajaran', 'C', 1),

(4, 'Jika 2x + 3 = 15, maka nilai x adalah ...',
 '5', '6', '7', '9', 'B', 2),

(5, 'Sebuah persegi panjang memiliki keliling 34 cm. Jika panjangnya 10 cm, berapakah luasnya?',
 '60 cm²', '65 cm²', '70 cm²', '75 cm²', 'C', 2),

(6, 'Kalimat yang paling efektif adalah ...',
 'Para siswa-siswa diwajibkan untuk hadir tepat waktu.',
 'Seluruh siswa diwajibkan hadir tepat waktu.',
 'Semua para siswa wajib untuk hadir tepat waktu.',
 'Siswa-siswa semuanya diwajibkan agar hadir tepat waktu.',
 'B', 3),
(7, 'Bacalah pernyataan berikut: "Perkembangan teknologi digital memudahkan masyarakat memperoleh informasi. Namun, kemudahan tersebut harus diimbangi dengan kemampuan memeriksa kebenaran informasi agar masyarakat tidak mudah terpengaruh berita palsu." Kesimpulan yang tepat adalah ...',
 'Teknologi digital selalu menyebarkan informasi palsu.',
 'Masyarakat sebaiknya menghindari penggunaan teknologi digital.',
 'Kemudahan memperoleh informasi perlu disertai sikap kritis dalam memeriksa kebenarannya.',
 'Semua informasi di internet dapat dipercaya.',
 'C', 3);
SELECT * FROM soal;

CREATE TYPE status_pendaftaran_enum AS ENUM (
    'Menunggu',
    'Diterima',
    'Ditolak'
);

CREATE TABLE pendaftaran (
    id_pendaftaran INTEGER PRIMARY KEY,
    tanggal_pendaftaran DATE NOT NULL,
    status_pendaftaran status_pendaftaran_enum NOT NULL,
    id_pengguna INTEGER NOT NULL,
	FOREIGN KEY (id_pengguna) REFERENCES pengguna(id_pengguna),
    id_paket INTEGER NOT NULL,
	FOREIGN KEY (id_paket) REFERENCES paket_tryout(id_paket)
);

INSERT INTO pendaftaran
(id_pendaftaran, tanggal_pendaftaran, status_pendaftaran, id_pengguna, id_paket)
VALUES
(1, '2026-11-15', 'Diterima', 5, 1),
(2, '2026-11-16', 'Diterima', 6, 2),
(3, '2026-11-17', 'Diterima', 7, 3);
SELECT * FROM pendaftaran;


CREATE TYPE status_pembayaran_enum AS ENUM (
    'Menunggu',
    'Berhasil',
    'Gagal',
    'Dikembalikan'
);

CREATE TABLE pembayaran (
    id_pembayaran INTEGER PRIMARY KEY,
    tanggal_pembayaran TIMESTAMP,
    jumlah_pembayaran NUMERIC(12, 2) NOT NULL 
    CHECK (jumlah_pembayaran >= 0),
    metode_pembayaran VARCHAR(30) NOT NULL,
    status_pembayaran status_pembayaran_enum NOT NULL,
    id_pendaftaran INTEGER NOT NULL,
	FOREIGN KEY (id_pendaftaran) REFERENCES
pendaftaran(id_pendaftaran)
);

INSERT INTO pembayaran
(id_pembayaran, tanggal_pembayaran, jumlah_pembayaran, metode_pembayaran, status_pembayaran, id_pendaftaran)
VALUES
(1, '2026-11-15 09:00:00', 50000, 'Tunai', 'Berhasil', 1),
(2, '2026-11-16 10:00:00', 30000, 'Non Tunai', 'Berhasil', 2),
(3, '2026-11-17 11:00:00', 25000, 'Tunai', 'Berhasil', 3);

--UPDATE pembayaran
--SET metode_pembayaran = 'Tunai'
--WHERE id_pembayaran = 1;

--UPDATE pembayaran
--SET metode_pembayaran = 'Non Tunai'
--WHERE id_pembayaran = 2;

--UPDATE pembayaran
--SET metode_pembayaran = 'Tunai'
--WHERE id_pembayaran = 3;

SELECT * FROM pembayaran
ORDER BY id_pembayaran ASC;

SELECT * FROM pembayaran;


CREATE TYPE status_pengerjaan_enum AS ENUM (
    'Belum Dimulai',
    'Sedang Berlangsung',
    'Selesai',
    'Dibatalkan'
);

CREATE TABLE pengerjaan_tryout (
    id_pengerjaan INTEGER PRIMARY KEY,
    waktu_mulai TIMESTAMP,
    waktu_selesai TIMESTAMP,
    status_pengerjaan status_pengerjaan_enum NOT NULL,
    id_pendaftaran INTEGER NOT NULL,
	FOREIGN KEY (id_pendaftaran) REFERENCES pendaftaran(id_pendaftaran)
);

INSERT INTO pengerjaan_tryout
(id_pengerjaan, waktu_mulai, waktu_selesai, status_pengerjaan, id_pendaftaran)
VALUES
(1, '2026-11-15 09:30:00', '2026-11-15 10:30:00', 'Selesai', 1),
(2, '2026-11-16 10:30:00', '2026-11-16 11:15:00', 'Selesai', 2),
(3, '2026-11-17 11:30:00', '2026-11-17 12:15:00', 'Selesai', 3);
SELECT * FROM pengerjaan_tryout;

CREATE TABLE jawaban (
    id_jawaban INTEGER PRIMARY KEY,
    jawaban_peserta CHAR(1) NOT NULL
    CHECK (jawaban_peserta IN ('A', 'B', 'C', 'D')),
    status_benar BOOLEAN NOT NULL,
    id_pengerjaan INTEGER NOT NULL,
	FOREIGN KEY (id_pengerjaan) REFERENCES pengerjaan_tryout(id_pengerjaan),
    id_soal INTEGER NOT NULL,
	FOREIGN KEY (id_soal) REFERENCES soal(id_soal)
);

INSERT INTO jawaban
(id_jawaban, jawaban_peserta, status_benar, id_pengerjaan, id_soal)
VALUES
(1, 'C', TRUE, 1, 1),
(2, 'B', TRUE, 1, 2),
(3, 'A', FALSE, 1, 3),

(4, 'B', TRUE, 2, 4),
(5, 'A', FALSE, 2, 5),

(6, 'B', TRUE, 3, 6),
(7, 'C', TRUE, 3, 7);
SELECT * FROM jawaban;

CREATE TABLE hasil_tryout (
    id_hasil INTEGER PRIMARY KEY,
    nilai NUMERIC(5, 2) NOT NULL CHECK (nilai BETWEEN 0 AND 100),
    jumlah_benar INTEGER NOT NULL,
    jumlah_salah INTEGER NOT NULL,
    tanggal_penilaian TIMESTAMP NOT NULL,
    id_pengerjaan INTEGER NOT NULL,
	FOREIGN KEY (id_pengerjaan) REFERENCES pengerjaan_tryout(id_pengerjaan)
);

INSERT INTO hasil_tryout
(id_hasil, nilai, jumlah_benar, jumlah_salah, tanggal_penilaian, id_pengerjaan)
VALUES
(1, 66.67, 2, 1, '2026-11-15 10:35:00', 1),
(2, 50.00, 1, 1, '2026-11-16 11:20:00', 2),
(3, 100.00, 2, 0, '2026-11-17 12:20:00', 3);
SELECT * FROM hasil_tryout;

--perbaikan id yg jadi pk biar auto increment 
-- 1. Tabel role
CREATE SEQUENCE IF NOT EXISTS role_id_role_seq;

ALTER TABLE role
ALTER COLUMN id_role SET DEFAULT nextval('role_id_role_seq');

ALTER SEQUENCE role_id_role_seq
OWNED BY role.id_role;

SELECT setval(
    'role_id_role_seq',
    COALESCE((SELECT MAX(id_role) FROM role), 1),
    EXISTS (SELECT 1 FROM role)
);


-- 2. Tabel pengguna
CREATE SEQUENCE IF NOT EXISTS pengguna_id_pengguna_seq;

ALTER TABLE pengguna
ALTER COLUMN id_pengguna SET DEFAULT nextval('pengguna_id_pengguna_seq');

ALTER SEQUENCE pengguna_id_pengguna_seq
OWNED BY pengguna.id_pengguna;

SELECT setval(
    'pengguna_id_pengguna_seq',
    COALESCE((SELECT MAX(id_pengguna) FROM pengguna), 1),
    EXISTS (SELECT 1 FROM pengguna)
);


-- 3. Tabel paket_tryout
CREATE SEQUENCE IF NOT EXISTS paket_tryout_id_paket_seq;

ALTER TABLE paket_tryout
ALTER COLUMN id_paket SET DEFAULT nextval('paket_tryout_id_paket_seq');

ALTER SEQUENCE paket_tryout_id_paket_seq
OWNED BY paket_tryout.id_paket;

SELECT setval(
    'paket_tryout_id_paket_seq',
    COALESCE((SELECT MAX(id_paket) FROM paket_tryout), 1),
    EXISTS (SELECT 1 FROM paket_tryout)
);


-- 4. Tabel soal
CREATE SEQUENCE IF NOT EXISTS soal_id_soal_seq;

ALTER TABLE soal
ALTER COLUMN id_soal SET DEFAULT nextval('soal_id_soal_seq');

ALTER SEQUENCE soal_id_soal_seq
OWNED BY soal.id_soal;

SELECT setval(
    'soal_id_soal_seq',
    COALESCE((SELECT MAX(id_soal) FROM soal), 1),
    EXISTS (SELECT 1 FROM soal)
);


-- 5. Tabel pendaftaran
CREATE SEQUENCE IF NOT EXISTS pendaftaran_id_pendaftaran_seq;

ALTER TABLE pendaftaran
ALTER COLUMN id_pendaftaran SET DEFAULT nextval('pendaftaran_id_pendaftaran_seq');

ALTER SEQUENCE pendaftaran_id_pendaftaran_seq
OWNED BY pendaftaran.id_pendaftaran;

SELECT setval(
    'pendaftaran_id_pendaftaran_seq',
    COALESCE((SELECT MAX(id_pendaftaran) FROM pendaftaran), 1),
    EXISTS (SELECT 1 FROM pendaftaran)
);


-- 6. Tabel pembayaran
CREATE SEQUENCE IF NOT EXISTS pembayaran_id_pembayaran_seq;

ALTER TABLE pembayaran
ALTER COLUMN id_pembayaran SET DEFAULT nextval('pembayaran_id_pembayaran_seq');

ALTER SEQUENCE pembayaran_id_pembayaran_seq
OWNED BY pembayaran.id_pembayaran;

SELECT setval(
    'pembayaran_id_pembayaran_seq',
    COALESCE((SELECT MAX(id_pembayaran) FROM pembayaran), 1),
    EXISTS (SELECT 1 FROM pembayaran)
);


-- 7. Tabel pengerjaan_tryout
CREATE SEQUENCE IF NOT EXISTS pengerjaan_tryout_id_pengerjaan_seq;

ALTER TABLE pengerjaan_tryout
ALTER COLUMN id_pengerjaan SET DEFAULT nextval('pengerjaan_tryout_id_pengerjaan_seq');

ALTER SEQUENCE pengerjaan_tryout_id_pengerjaan_seq
OWNED BY pengerjaan_tryout.id_pengerjaan;

SELECT setval(
    'pengerjaan_tryout_id_pengerjaan_seq',
    COALESCE((SELECT MAX(id_pengerjaan) FROM pengerjaan_tryout), 1),
    EXISTS (SELECT 1 FROM pengerjaan_tryout)
);


-- 8. Tabel jawaban
CREATE SEQUENCE IF NOT EXISTS jawaban_id_jawaban_seq;

ALTER TABLE jawaban
ALTER COLUMN id_jawaban SET DEFAULT nextval('jawaban_id_jawaban_seq');

ALTER SEQUENCE jawaban_id_jawaban_seq
OWNED BY jawaban.id_jawaban;

SELECT setval(
    'jawaban_id_jawaban_seq',
    COALESCE((SELECT MAX(id_jawaban) FROM jawaban), 1),
    EXISTS (SELECT 1 FROM jawaban)
);


-- 9. Tabel hasil_tryout
CREATE SEQUENCE IF NOT EXISTS hasil_tryout_id_hasil_seq;

ALTER TABLE hasil_tryout
ALTER COLUMN id_hasil SET DEFAULT nextval('hasil_tryout_id_hasil_seq');

ALTER SEQUENCE hasil_tryout_id_hasil_seq
OWNED BY hasil_tryout.id_hasil;

SELECT setval(
    'hasil_tryout_id_hasil_seq',
    COALESCE((SELECT MAX(id_hasil) FROM hasil_tryout), 1),
    EXISTS (SELECT 1 FROM hasil_tryout)
);

--periksa
SELECT
    column_name,
    column_default
FROM information_schema.columns
WHERE table_name = 'pengguna'
AND column_name = 'id_pengguna';

SELECT
    table_name,
    column_name,
    column_default
FROM information_schema.columns
WHERE column_name IN (
    'id_role',
    'id_pengguna',
    'id_paket',
    'id_soal',
    'id_pendaftaran',
    'id_pembayaran',
    'id_pengerjaan',
    'id_jawaban',
    'id_hasil'
)
ORDER BY table_name;

SELECT
    conname AS nama_constraint,
    pg_get_constraintdef(oid) AS aturan
FROM pg_constraint
WHERE conrelid = 'paket_tryout'::regclass
  AND contype = 'c';

SELECT id_paket, nama_paket, harga_paket
FROM paket_tryout
WHERE harga_paket < 10000;

SELECT id_paket, nama_paket, durasi_waktu
FROM paket_tryout
WHERE durasi_waktu < 10;

--ganti constraint
ALTER TABLE paket_tryout
DROP CONSTRAINT paket_tryout_harga_paket_check,
DROP CONSTRAINT paket_tryout_durasi_waktu_check;

ALTER TABLE paket_tryout
ADD CONSTRAINT paket_tryout_harga_paket_check
CHECK (harga_paket >= 10000);

ALTER TABLE paket_tryout
ADD CONSTRAINT paket_tryout_durasi_waktu_check
CHECK (durasi_waktu >= 10);

--
UPDATE paket_tryout
SET harga_paket = 10000,
    durasi_waktu = 10
WHERE id_paket = 5;

--
SELECT
    conname AS nama_constraint,
    pg_get_constraintdef(oid) AS aturan
FROM pg_constraint
WHERE conrelid = 'paket_tryout'::regclass
  AND contype = 'c';

ALTER TABLE paket_tryout
ADD COLUMN status_aktif BOOLEAN NOT NULL DEFAULT TRUE;

ALTER TABLE soal
ADD COLUMN status_aktif BOOLEAN NOT NULL DEFAULT TRUE;

--cek
SELECT id_paket, nama_paket, status_aktif
FROM paket_tryout
ORDER BY id_paket;

SELECT
    p.id_paket,
    p.nama_paket,
    p.id_pengguna,
    u.nama_pengguna
FROM paket_tryout p
JOIN pengguna u ON p.id_pengguna = u.id_pengguna
WHERE p.id_paket = 6;

--soalnya klo not null itu dari awal peserta ngerjain udh ke record padahal blm selesai ngerjain
ALTER TABLE pengerjaan_tryout
ALTER COLUMN waktu_selesai DROP NOT NULL;