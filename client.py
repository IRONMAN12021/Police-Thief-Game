import pygame
from pygame.locals import *
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Police and Thief Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Fonts
font = pygame.font.Font(None, 36)
title_font = pygame.font.Font(None, 64)

# Load Images
police_img = pygame.image.load("police.png")
thief_img = pygame.image.load("thief.png")
background_img = pygame.image.load("background.png")

# Resizing Images
police_img = pygame.transform.scale(police_img, (50, 50))
thief_img = pygame.transform.scale(thief_img, (50, 50))
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Game states
START_SCREEN = "start"
HOME_SCREEN = "home"
GAME_SCREEN = "game"
MENU_SCREEN = "menu"
LEADERBOARD_SCREEN = "leaderboard"
SETTINGS_SCREEN = "settings"

game_state = START_SCREEN

# Utility functions
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def start_screen():
    screen.blit(background_img, (0, 0))
    draw_text("Police and Thief Game", title_font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
    draw_text("Press Enter to Start", font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    pygame.display.update()

def home_screen():
    screen.fill(GREEN)
    draw_text("Home Screen", title_font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
    draw_text("Press 'S' to Start Game", font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    draw_text("Press 'L' to View Leaderboard", font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
    draw_text("Press 'O' for Settings", font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
    pygame.display.update()

def game_screen():
    screen.fill(BLUE)
    draw_text("Game Screen - Police and Thief", title_font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
    # Game logic here
    pygame.display.update()

def menu_screen():
    screen.fill(RED)
    draw_text("Menu Screen", title_font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
    draw_text("Press 'R' to Resume", font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    draw_text("Press 'Q' to Quit", font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
    pygame.display.update()

def leaderboard_screen():
    screen.fill(YELLOW)
    draw_text("Leaderboard", title_font, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
    # Leaderboard logic here
    pygame.display.update()

def settings_screen():
    screen.fill(BLACK)
    draw_text("Settings", title_font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
    draw_text("Adjust settings here", font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    pygame.display.update()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if game_state == START_SCREEN:
                if event.key == K_RETURN:
                    game_state = HOME_SCREEN
            elif game_state == HOME_SCREEN:
                if event.key == K_s:
                    game_state = GAME_SCREEN
                elif event.key == K_l:
                    game_state = LEADERBOARD_SCREEN
                elif event.key == K_o:
                    game_state = SETTINGS_SCREEN
            elif game_state == MENU_SCREEN:
                if event.key == K_r:
                    game_state = GAME_SCREEN
                elif event.key == K_q:
                    running = False

    if game_state == START_SCREEN:
        start_screen()
    elif game_state == HOME_SCREEN:
        home_screen()
    elif game_state == GAME_SCREEN:
        game_screen()
    elif game_state == MENU_SCREEN:
        menu_screen()
    elif game_state == LEADERBOARD_SCREEN:
        leaderboard_screen()
    elif game_state == SETTINGS_SCREEN:
        settings_screen()

pygame.quit()

