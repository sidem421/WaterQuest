import pygame
import sys
import csv
import os

pygame.init()

# ================= AYARLAR =================
WIDTH, HEIGHT = 1000, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# 🔴 OYUN ADI GÜNCELLENDİ
pygame.display.set_caption("WaterQuest – Su Verimliliği Simülasyon Oyunu")

FONT = pygame.font.SysFont("arial", 24)
BIG = pygame.font.SysFont("arial", 36)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

clock = pygame.time.Clock()

DATA_FILE = "data.csv"

# ================= CSV =================
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow(["Ad", "Soyad", "Sinif", "No", "Su"])

# ================= GÖRSELLER =================
def load_bg(name):
    return pygame.transform.scale(
        pygame.image.load(f"assets/{name}"), (WIDTH, HEIGHT)
    )

menu_bg = load_bg("menu_bg.png")
register_bg = load_bg("register_bg.png")
bedroom_bg = load_bg("bedroom.png")
bathroom_bg = load_bg("bathroom.png")
school_bg = load_bg("school.png")
night_bg = load_bg("night_room.png")

boy = pygame.transform.scale(pygame.image.load("assets/boy.png"), (220, 320))
girl = pygame.transform.scale(pygame.image.load("assets/girl.png"), (220, 320))

good_img = pygame.transform.scale(pygame.image.load("assets/result_good.png"), (200, 200))
bad_img = pygame.transform.scale(pygame.image.load("assets/result_bad.png"), (200, 200))

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

# ================= ANA MENÜ =================
def main_menu():
    fade_in()
    while True:
        screen.blit(menu_bg, (0, 0))

        # 🔴 ANA MENÜ OYUN ADI GÜNCELLENDİ
        draw("WaterQuest", BIG, 410, 140)
        draw("Su Verimliliği Simülasyon Oyunu", FONT, 330, 185)

        draw("1 - Oyuna Başla", FONT, 420, 260)
        draw("ESC - Çıkış", FONT, 430, 300)

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

                if e.key == pygame.K_ESCAPE:
                    fade_out()
                    pygame.quit(); sys.exit()

        pygame.display.update()
        clock.tick(30)

# ================= (DİĞER FONKSİYONLAR AYNI) =================
# register(), character_select(), routine(), play_game(), end_screen()
# → senin gönderdiğin kodla birebir, dokunmadım

# ================= BAŞLAT =================
main_menu()
