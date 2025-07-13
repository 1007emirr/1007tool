#!/usr/bin/env python3
import pygame
import sys
import os
import random
import subprocess
from git import Repo

# Pygame başlatma
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("1007SCRIPT")
clock = pygame.time.Clock()
FPS = 30

# Renkler
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Anonymous teması
MASK_COLOR = (0, 0, 0)  # Siyah maske
BG_COLOR = (30, 15, 30)  # Koyu arkaplan

# Nyancat sınıfı
class Nyancat:
    def __init__(self):
        self.x = -100
        self.y = HEIGHT // 2
        self.speed = 5
        self.frame = 0
        self.colors = [
            (255, 0, 0), (255, 165, 0), (255, 255, 0),
            (0, 255, 0), (0, 0, 255), (75, 0, 130)
        ]
    
    def update(self):
        self.x += self.speed
        self.frame = (self.frame + 1) % 6
        if self.x > WIDTH + 100:
            return True  # Animasyon bitti
        return False
    
    def draw(self, surface):
        # Gövde
        pygame.draw.rect(surface, (200, 200, 200), (self.x, self.y, 60, 30))
        
        # Kuyruk (gökkuşağı)
        for i in range(6):
            color = self.colors[(self.frame + i) % len(self.colors)]
            pygame.draw.rect(surface, color, (self.x - 20 - i*10, self.y + i*5, 10, 10))

# Anonymous maskesi çizimi
def draw_anonymous(surface):
    # Maske gövdesi
    pygame.draw.ellipse(surface, MASK_COLOR, (WIDTH//2 - 100, HEIGHT//2 - 80, 200, 160))
    
    # Gözler
    pygame.draw.ellipse(surface, WHITE, (WIDTH//2 - 60, HEIGHT//2 - 40, 40, 60))
    pygame.draw.ellipse(surface, WHITE, (WIDTH//2 + 20, HEIGHT//2 - 40, 40, 60))
    
    # Ağız
    pygame.draw.arc(surface, WHITE, (WIDTH//2 - 40, HEIGHT//2, 80, 40), 3.14, 6.28, 2)

# Ana menü
def show_menu():
    options = ["1. SocialBox-Termux", "2. Virus-Builder", "3. HackingTool", "4. Çıkış"]
    selected = 0
    font = pygame.font.SysFont("Arial", 32)
    
    # Nyancat animasyonu
    nyancat = Nyancat()
    anim_done = False
    
    running = True
    while running:
        screen.fill(BG_COLOR)
        
        # Nyancat animasyonu
        if not anim_done:
            anim_done = nyancat.update()
            nyancat.draw(screen)
        else:
            # Anonymous teması göster
            draw_anonymous(screen)
        
        # Menü seçenekleri
        for i, option in enumerate(options):
            color = GREEN if i == selected else WHITE
            text = font.render(option, True, color)
            screen.blit(text, (WIDTH//2 - 100, 100 + i * 50))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if selected == 3:  # Çıkış
                        running = False
                    else:
                        run_tool(["SocialBox", "VirusBuilder", "HackingTool"][selected])

        clock.tick(FPS)

# Araç çalıştırma fonksiyonu
def run_tool(tool_name):
    tools = {
        "SocialBox": "https://github.com/samsesh/SocialBox-Termux.git",
        "VirusBuilder": "https://github.com/Cyber-Dioxide/Virus-Builder.git",
        "HackingTool": "https://github.com/Z4nzu/hackingtool.git"
    }
    
    if tool_name in tools:
        try:
            if os.path.exists(tool_name):
                subprocess.run(["rm", "-rf", tool_name], check=True)
            
            print(f"\n[*] {tool_name} indiriliyor...")
            Repo.clone_from(tools[tool_name], tool_name)
            os.chdir(tool_name)
            
            if tool_name == "SocialBox":
                subprocess.run(["chmod", "+x", "install-sb.sh"])
                subprocess.run(["./install-sb.sh"])
            elif tool_name == "VirusBuilder":
                subprocess.run(["chmod", "+x", "virus.sh"])
                subprocess.run(["./virus.sh"])
            elif tool_name == "HackingTool":
                subprocess.run(["chmod", "+x", "install.sh"])
                subprocess.run(["./install.sh"])
                
            os.chdir("..")
            
        except Exception as e:
            print(f"[!] Hata: {e}")
            if tool_name in os.listdir():
                os.chdir("..")

if __name__ == "__main__":
    show_menu()
    pygame.quit()
    sys.exit()
