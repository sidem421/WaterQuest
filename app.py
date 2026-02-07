import pygame
import sys
import csv
import os

pygame.init()

# ================= AYARLAR =================
WIDTH, HEIGHT = 1000, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("WaterQuest")

FONT = pygame.font.SysFont("arial", 22)
BIG = pygame.font.SysFont("arial", 36)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (220, 220, 220)

clock = pygame.time.Clock()
DATA_FILE = "data.csv"
ADMIN_PASSWORD = "1234"

# ================= CSV =================
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow(["Ad", "Soyad", "Sinif", "No", "Su"])

# ================= GÖRSELLER =================
def load_bg(name):
    path = f"assets/{name}"
    if os.path.exists(path):
        return pygame.transform.scale(pygame.image.load(path), (WIDTH, HEIGHT))
    else:
        print(f"Uyarı: Görsel bulunamadı: {name}")
        return pygame.Surface((WIDTH, HEIGHT))

menu_bg = load_bg("menu_bg.png")
register_bg = load_bg("register_bg.png")
bedroom_bg = load_bg("bedroom.png")
bathroom_bg = load_bg("bathroom.png")
school_bg = load_bg("school.png")
night_bg = load_bg("night_room.png")

def load_character(name, size=(220, 320)):
    path = f"assets/{name}"
    if os.path.exists(path):
        return pygame.transform.scale(pygame.image.load(path), size)
    else:
        print(f"Uyarı: Karakter görseli bulunamadı: {name}")
        surf = pygame.Surface(size)
        surf.fill(GRAY)
        return surf

boy = load_character("boy.png")
girl = load_character("girl.png")

good_img = load_character("result_good.png", (200, 200))
bad_img = load_character("result_bad.png", (200, 200))

# ================= GLOBAL =================
player = {}
water_used = 0

# ================= YARDIMCI =================
def draw(text, font, x, y):
    screen.blit(font.render(text, True, BLACK), (x, y))

# ================= FADE =================
def fade_out(speed=15):
    fade = pygame.Surface((WIDTH, HEIGHT))
    fade.fill(BLACK)
    for alpha in range(0, 256, speed):
        fade.set_alpha(alpha)
        screen.blit(fade, (0, 0))
        pygame.display.update()
        clock.tick(60)

def fade_in(speed=15):
    fade = pygame.Surface((WIDTH, HEIGHT))
    fade.fill(BLACK)
    for alpha in range(255, -1, -speed):
        fade.set_alpha(alpha)
        screen.blit(fade, (0, 0))
        pygame.display.update()
        clock.tick(60)

# ================= KAYIT =================
def register():
    fields = ["Ad", "Soyad", "Sınıf", "Numara"]
    values = ["", "", "", ""]
    index = 0

    fade_in()
    while True:
        screen.blit(register_bg, (0, 0))
        draw("Öğrenci Kayıt", BIG, 380, 40)

        for i, f in enumerate(fields):
            draw(f"{f}: {values[i]}", FONT, 300, 180 + i * 50)

        draw("ENTER → Devam", FONT, 400, 450)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    index += 1
                    if index >= len(values):
                        # Güvenli atama
                        try:
                            player["ad"], player["soyad"] = values[0], values[1]
                            player["sinif"], player["no"] = int(values[2]), int(values[3])
                        except:
                            player["ad"], player["soyad"], player["sinif"], player["no"] = values
                        fade_out()
                        return
                elif e.key == pygame.K_BACKSPACE:
                    if index < len(values):
                        values[index] = values[index][:-1]
                else:
                    if index < len(values):
                        values[index] += e.unicode

        pygame.display.update()
        clock.tick(30)

# ================= KARAKTER =================
def character_select():
    fade_in()
    while True:
        screen.fill(WHITE)
        draw("Karakterini Seç", BIG, 380, 40)

        boy_rect = pygame.Rect(200, 200, 220, 320)
        girl_rect = pygame.Rect(580, 200, 220, 320)

        screen.blit(boy, boy_rect)
        screen.blit(girl, girl_rect)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if boy_rect.collidepoint(e.pos):
                    player["char"] = "Erkek"
                    fade_out()
                    return
                if girl_rect.collidepoint(e.pos):
                    player["char"] = "Kadın"
                    fade_out()
                    return

        pygame.display.update()
        clock.tick(30)

# ================= RUTİN =================
def routine(bg, title, options):
    global water_used
    fade_in()

    buttons = [pygame.Rect(250, 200 + i * 80, 500, 60) for i in range(len(options))]

    while True:
        screen.blit(bg, (0, 0))
        draw(title, BIG, 350, 40)

        for i, rect in enumerate(buttons):
            pygame.draw.rect(screen, GRAY, rect, border_radius=10)
            draw(options[i][0], FONT, rect.x + 20, rect.y + 18)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(buttons):
                    if rect.collidepoint(e.pos):
                        water_used += options[i][1]
                        fade_out()
                        return

        pygame.display.update()
        clock.tick(30)

# ================= OYUN =================
def play_game():
    global water_used
    water_used = 0

    routine(bedroom_bg, "Sabah Rutini", [
        ("Musluk açık yüz yıkama", 10),
        ("Musluk kapalı yüz yıkama", 3),
        ("Islak mendil", 1)
    ])

    routine(bathroom_bg, "Diş Fırçalama", [
        ("Musluk açık", 15),
        ("Bardakla", 4),
        ("Musluk kapalı", 2)
    ])

    routine(school_bg, "Okulda Su Kullanımı", [
        ("Uzun el yıkama", 8),
        ("Kısa el yıkama", 4),
        ("Dezenfektan", 1)
    ])

    routine(night_bg, "Akşam Rutini", [
        ("Uzun duş", 30),
        ("Kısa duş", 15),
        ("Duş almadan", 0)
    ])

    with open(DATA_FILE, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([
            player.get("ad",""), player.get("soyad",""),
            player.get("sinif",""), player.get("no",""),
            water_used
        ])

# ================= SON =================
def end_screen():
    fade_in()
    while True:
        screen.fill(WHITE)
        draw(f"Günlük Su Tüketimin: {water_used} L", BIG, 300, 150)

        if water_used <= 50:
            screen.blit(good_img, (400, 250))
            draw("Tebrikler! Bilinçli kullandın 🎉", FONT, 320, 470)
        else:
            screen.blit(bad_img, (400, 250))
            draw("Daha az su kullanabilirdin", FONT, 340, 470)

        draw("ESC → Çıkış", FONT, 420, 560)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                pygame.quit(); sys.exit()

        pygame.display.update()
        clock.tick(30)

# ================= YÖNETİCİ PANELİ =================
def admin_panel():
    password = ""
    fade_in()

    while True:
        screen.fill(WHITE)
        draw("Yönetici Girişi", BIG, 380, 100)
        draw("Şifre: " + "*" * len(password), FONT, 380, 200)
        draw("ENTER → Giriş | ESC → Geri", FONT, 320, 260)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    if password == ADMIN_PASSWORD:
                        show_results()
                        return
                    else:
                        password = ""
                elif e.key == pygame.K_BACKSPACE:
                    password = password[:-1]
                elif e.key == pygame.K_ESCAPE:
                    return
                else:
                    password += e.unicode

        pygame.display.update()
        clock.tick(30)

def show_results():
    fade_in()
    results = []

    with open(DATA_FILE, encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        results = list(reader)

    while True:
        screen.fill(WHITE)
        draw("Öğrenci Sonuçları", BIG, 350, 40)

        y = 120
        for r in results:
            draw(f"{r[0]} {r[1]} | {r[2]} | {r[3]} | {r[4]} L", FONT, 120, y)
            y += 30

        draw("ESC → Geri", FONT, 430, 580)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                fade_out()
                return

        pygame.display.update()
        clock.tick(30)

# ================= ANA MENÜ =================
def main_menu():
    fade_in()
    while True:
        screen.blit(menu_bg, (0, 0))
        draw("WaterQuest", BIG, 340, 150)
        draw("1 - Oyuna Başla", FONT, 420, 260)
        draw("2 - Yönetici Paneli", FONT, 410, 300)
        draw("ESC - Çıkış", FONT, 430, 340)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_1:
                    fade_out()
                    register()
                    character_select()
                    play_game()
                    end_screen()
                if e.key == pygame.K_2:
                    fade_out()
                    admin_panel()
                if e.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()

        pygame.display.update()
        clock.tick(30)

# ================= BAŞLAT =================
main_menu()
