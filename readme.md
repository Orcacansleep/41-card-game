# Game 41

## Deskripsi Permainan

Game 41 adalah permainan kartu berbasis GUI (Graphical User Interface) yang dimainkan oleh 4 pemain (1 pemain manusia dan 3 komputer). Tujuan dari permainan ini adalah untuk mendapatkan skor tertinggi dengan mengumpulkan kartu yang memiliki nilai tertinggi dalam satu jenis (suit). Permainan ini dirancang menggunakan Python dengan pustaka tkinter untuk antarmuka pengguna.

---

## Aturan Permainan

1. Setiap pemain memulai dengan 4 kartu.
2. Pemain bermain secara bergiliran searah jarum jam.
3. Di setiap giliran, pemain dapat mengambil kartu dari tumpukan draw (draw pile) dan harus membuang satu kartu ke tumpukan discard (discard pile).
4. Skor dihitung berdasarkan jumlah nilai tertinggi dalam satu jenis kartu (suit) di tangan pemain.
5. Permainan berakhir ketika tumpukan draw habis, dan pemain dengan skor tertinggi dinyatakan sebagai pemenang.

---

## Cara Bermain

### 1. Antarmuka Permainan

- **Player South**: Pemain manusia, kartu ditampilkan di bagian bawah layar.
- **Player North, East, dan West**: Pemain komputer, kartu mereka tidak terlihat oleh manusia (ditampilkan sebagai kartu tertutup).
- **Tumpukan Draw dan Discard**: Ditampilkan di bagian tengah layar.
- **Status**: Menampilkan giliran pemain saat ini.

### 2. Aksi Pemain

- **Draw Card**: Klik tombol "Draw Card" untuk mengambil kartu dari tumpukan draw.
- **Discard Card**: Pilih kartu yang akan dibuang dengan mengklik kartu di tangan, lalu klik tombol "Discard Card".

### 3. Akhir Permainan

- Permainan akan berakhir secara otomatis ketika tumpukan draw habis.
- Pemain dengan skor tertinggi akan diumumkan sebagai pemenang.

---

## Struktur Kode

### 1. Kelas Card

Kelas ini merepresentasikan sebuah kartu dengan atribut:

- `suit`: Jenis kartu (Hearts, Diamonds, Clubs, Spades).
- `value`: Nilai kartu (1-13, dengan As=1, Jack=11, Queen=12, King=13).
- `image_path`: Jalur file gambar kartu untuk ditampilkan di GUI.

### 2. Kelas Game41

Kelas utama yang mengelola logika permainan dan GUI. Fitur utama:

- **create_deck**: Membuat deck kartu (52 kartu).
- **deal_initial_cards**: Membagikan 4 kartu awal kepada setiap pemain.
- **update_player_hand**: Memperbarui tampilan kartu pemain manusia.
- **draw_card & discard_card**: Mengatur aksi mengambil dan membuang kartu.
- **calculate_score**: Menghitung skor berdasarkan nilai kartu tertinggi dalam satu suit.
- **end_game**: Menentukan pemenang di akhir permainan.

---

## Teknologi yang Digunakan

- **Python**: Bahasa pemrograman utama.
- **Tkinter**: Untuk antarmuka grafis (GUI).
- **Pillow (PIL)**: Untuk memuat dan memproses gambar kartu.

---

## Cara Menjalankan Program

1. Pastikan Anda memiliki Python 3.x terinstal di komputer Anda.
2. Pastikan pustaka berikut sudah terinstal:
   - `tkinter`
   - `Pillow`
3. Jalankan file Python `kartu41.py` menggunakan perintah berikut:
   ```bash
   python kartu41.py
   ```
4. Program akan membuka jendela GUI, dan Anda dapat langsung bermain.

---

## Folder Struktur

```
project-directory/
|-- kartu41.py           # File utama untuk menjalankan permainan
|-- cards/               # Folder berisi gambar kartu
    |-- card_hearts_01.png
    |-- card_diamonds_01.png
    |-- ... (gambar kartu lainnya)
```

---

## Catatan Penting

- Pastikan folder `cards/` berisi semua gambar kartu yang diperlukan agar permainan berjalan dengan baik.
- Gambar kartu harus menggunakan format nama: `card_<suit>_<value>.png` (contoh: `card_hearts_01.png` untuk As Hati).

---

## Pengembangan di Masa Depan

1. Menambahkan level kesulitan untuk pemain komputer.
2. Memberikan opsi untuk bermain multiplayer melalui jaringan.
3. Menyediakan mode tutorial untuk pemain baru.
4. Menambahkan efek suara dan animasi untuk pengalaman bermain yang lebih baik.

---

## Kontributor

Program ini dikembangkan oleh ahmad seloa abadi. Jika Anda memiliki pertanyaan atau ingin memberikan masukan, silakan hubungi saya pad halaman profil github saya.
