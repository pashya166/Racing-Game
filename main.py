# Import library Pygame, Time (untuk jeda), dan Random (untuk posisi acak)
import pygame
import time
import random

# Inisialisasi Pygame: wajib dipanggil di awal untuk menjalankan semua modul Pygame
pygame.init()

# --- Konfigurasi Layar Game ---
display_width = 800
display_height = 600

# Membuat objek display/layar dengan ukuran yang sudah ditentukan
gameDisplay = pygame.display.set_mode((display_width, display_height))
# Menentukan judul jendela game
pygame.display.set_caption('Racing Game - Mode Bertahan')

# --- Definisi Warna (RGB) ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
GRAY = (50, 50, 50)

# --- Parameter Mobil Player dan Musuh ---
# Ukuran Lebar dan Tinggi gambar mobil di layar (Dibiarkan 250x150 agar gambar tidak gepeng)
car_width = 300
car_height = 150

# Membuat objek Clock untuk mengatur frame rate (FPS) game
clock = pygame.time.Clock()

# ==========================================
# BAGIAN LOAD GAMBAR
# ==========================================
try:
    # 1. Load Mobil Player dan mengubah ukurannya sesuai car_width/car_height
    carImg = pygame.image.load('Racer.png')
    carImg = pygame.transform.scale(carImg, (car_width, car_height))

    # 2. Load Mobil Musuh (ukurannya akan di-scale dinamis di fungsi things())
    enemyImg = pygame.image.load('Enemy.png')
except:
    # Fallback: Jika gambar tidak ditemukan, buat kotak biru (player) dan merah (musuh)
    print("WARNING: Gambar 'mobil_keren.png' atau 'musuh.png' gak ketemu!")
    carImg = pygame.Surface((car_width, car_height))
    carImg.fill((0, 0, 255)) # Biru
    enemyImg = pygame.Surface((250, 150))
    enemyImg.fill(RED)       # Merah

# ==========================================

# Fungsi untuk menampilkan skor di pojok kiri atas
def things_dodged(count):
    font = pygame.font.SysFont(None, 25)
    # Merender (mengubah) angka skor menjadi objek teks berwarna putih
    text = font.render("Score: " + str(count), True, WHITE)
    # Menempatkan teks di layar pada koordinat (0, 0)
    gameDisplay.blit(text, (0, 0))

# Fungsi untuk menggambar rintangan (musuh)
def things(thingx, thingy, thingw, thingh, color):
    # Mengubah ukuran gambar musuh agar sesuai dengan ukuran rintangan saat ini
    scaled_enemy = pygame.transform.scale(enemyImg, (int(thingw), int(thingh)))
    # Menampilkan gambar musuh di koordinat yang ditentukan
    gameDisplay.blit(scaled_enemy, (thingx, thingy))

# Fungsi untuk menggambar mobil pemain
def car(x, y):
    # Menampilkan gambar mobil pemain (carImg) di koordinat (x, y)
    gameDisplay.blit(carImg, (x, y))

# Fungsi pembantu untuk membuat objek teks (surface dan rect)
def text_objects(text, font):
    # Merender teks menjadi objek Surface (tampilan visual)
    textSurface = font.render(text, True, WHITE)
    # Mendapatkan Rect (kotak pembatas) dari teks
    return textSurface, textSurface.get_rect()

# Fungsi untuk menampilkan pesan besar di tengah layar (misalnya pesan Crash)
def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf', 50)
    # Membuat Surface dan Rect dari teks
    TextSurf, TextRect = text_objects(text, largeText)
    # Menetapkan posisi Rect agar berada di tengah layar
    TextRect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(TextSurf, TextRect)
    # Memperbarui tampilan layar
    pygame.display.update()
    # Memberi jeda 2 detik
    time.sleep(2)
    # Memanggil game_loop() untuk mereset/memulai game baru
    game_loop()

# Fungsi yang dipanggil saat terjadi tabrakan
def crash():
    message_display('Kamu Tabrakan!')

# ==========================================
# FUNGSI UTAMA GAME LOOP
# ==========================================
def game_loop():
    # Posisi X awal mobil: di tengah layar
    x = (display_width / 2) - (car_width / 2)
    # Posisi Y awal mobil: di bagian bawah layar
    y = (display_height * 0.65)

    # Variabel untuk menyimpan perubahan posisi X (kecepatan horizontal)
    x_change = 0

    # --- Parameter Awal Musuh ---
    thing_startx = random.randrange(0, display_width) # Posisi X acak
    thing_starty = -600                              # Mulai dari luar atas layar
    thing_speed = 4                                  # Kecepatan awal
    thing_width = car_width                          # Lebar musuh (disamakan dengan mobil)
    thing_height = car_height                        # Tinggi musuh (disamakan dengan mobil)

    dodged = 0       # Skor
    gameExit = False # Flag untuk mengontrol loop

    # Loop utama game: akan terus berjalan selama gameExit = False
    while not gameExit:

        # Menganalisis semua event (input) yang terjadi
        for event in pygame.event.get():
            # Jika user mengklik tombol Close Window
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # Jika tombol keyboard ditekan
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -8 # Bergerak ke kiri
                if event.key == pygame.K_RIGHT:
                    x_change = 8  # Bergerak ke kanan

            # Jika tombol keyboard dilepas
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0  # Berhenti bergerak

        # Update posisi X mobil
        x += x_change

        # Menggambar latar belakang (aspal)
        gameDisplay.fill(GRAY)

        # Menggambar Garis Jalan (Dipertahankan)
        line_y = (thing_starty * 2) % display_height
        pygame.draw.rect(gameDisplay, WHITE, [display_width/2 - 5, line_y, 10, 100])
        pygame.draw.rect(gameDisplay, WHITE, [display_width/2 - 5, line_y - 200, 10, 100])
        pygame.draw.rect(gameDisplay, WHITE, [display_width/2 - 5, line_y - 400, 10, 100])
        pygame.draw.rect(gameDisplay, WHITE, [display_width/2 - 5, line_y + 200, 10, 100])

        # Menggambar dan menggerakkan Musuh
        things(thing_startx, thing_starty, thing_width, thing_height, RED)
        thing_starty += thing_speed # Musuh bergerak ke bawah

        # Menggambar Mobil Player dan Skor
        car(x, y)
        things_dodged(dodged)

        # Logika Batasan Layar (agar mobil tidak keluar layar, tidak crash)
        if x > display_width - car_width:
            x = display_width - car_width
        if x < 0:
            x = 0

        # Logika Reset Musuh (ketika musuh sudah melewati layar)
        if thing_starty > display_height:
            thing_starty = 0 - thing_height # Reset posisi Y ke atas
            # Reset posisi X secara acak (memastikan di dalam batas layar)
            thing_startx = random.randrange(0, display_width - thing_width)
            dodged += 1       # Tambah skor
            thing_speed += 0.5 # Tingkatkan kecepatan

        # --- LOGIKA TABRAKAN (HITBOX ASIMETRIS) ---
        # Definisikan pengurangan (reduction) Hitbox agar ramping
        lebar_hitbox_reduction = -200 
        tinggi_hitbox_reduction = -50  

        # Membuat Hitbox untuk Player: Menggunakan ukuran mobil asli tapi di-inflate agar ramping
        player_rect = pygame.Rect(x, y, car_width, car_height).inflate(lebar_hitbox_reduction, tinggi_hitbox_reduction)
        # Membuat Hitbox untuk Musuh
        enemy_rect = pygame.Rect(thing_startx, thing_starty, thing_width, thing_height).inflate(lebar_hitbox_reduction, tinggi_hitbox_reduction)

        # Cek Tabrakan: colliderect() akan TRUE jika kedua kotak bersentuhan
        if player_rect.colliderect(enemy_rect):
              crash()

        # ==========================================
        # DEBUG MODE: GAMBAR HITBOX (Sekarang Dihapus/Transparan)
        # ==========================================
        # pygame.draw.rect(gameDisplay, (0, 255, 0), player_rect, 2)
        # pygame.draw.rect(gameDisplay, (255, 0, 0), enemy_rect, 2)
        # ==========================================

        # Memperbarui seluruh layar untuk menampilkan semua perubahan
        pygame.display.update()
        # Mengatur Frame Rate (FPS) agar game berjalan mulus
        clock.tick(60)

# Memulai game pertama kali
game_loop()
# Perintah keluar dari Pygame dan Python
pygame.quit()
quit()