import pygame
import requests
from flask_socketio import SocketIO
from threading import Thread
import random

# Pygame Setup
pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Online Police and Thief Game")

clock = pygame.time.Clock()

# Load images
police_img = pygame.image.load("police.png")
thief_img = pygame.image.load("thief.png")

# Resize images
police_img = pygame.transform.scale(police_img, (50, 50))
thief_img = pygame.transform.scale(thief_img, (50, 50))

# Flask-SocketIO Setup
socketio = SocketIO(message_queue='http://localhost:5000')

player_id = random.randint(1000, 9999)
player_type = 'police' if random.choice([True, False]) else 'thief'
players = {}
leaderboard = {}
thief_position = None
points = 0

def handle_player_joined(data):
    players[data['player_id']] = data

def handle_current_players(data):
    global players
    players = data

def handle_player_moved(data):
    players[data['player_id']] = data

def handle_game_started(data):
    global thief_position
    thief_position = (random.randint(50, 750), random.randint(50, 550))

def handle_booster_activated(data):
    if data['player_id'] == player_id and data['booster_type'] == 'silent_movement':
        print("Silent Movement Booster Activated")

def handle_points_updated(data):
    if data['player_id'] == player_id:
        global points
        points = data['points']

def handle_leaderboard_updated(data):
    global leaderboard
    leaderboard = data

socketio.on_event('player_joined', handle_player_joined)
socketio.on_event('current_players', handle_current_players)
socketio.on_event('player_moved', handle_player_moved)
socketio.on_event('game_started', handle_game_started)
socketio.on_event('booster_activated', handle_booster_activated)
socketio.on_event('points_updated', handle_points_updated)
socketio.on_event('leaderboard_updated', handle_leaderboard_updated)

def move_player(direction):
    socketio.emit('move_player', {'player_id': player_id, 'direction': direction})

def use_booster(booster_type):
    socketio.emit('use_booster', {'player_id': player_id, 'booster_type': booster_type})

def draw_leaderboard():
    font = pygame.font.Font(None, 36)
    y_offset = 20
    for pid, points in sorted(leaderboard.items(), key=lambda item: item[1], reverse=True):
        leaderboard_text = font.render(f"Player {pid}: {points} pts", True, BLACK)
        screen.blit(leaderboard_text, (600, y_offset))
        y_offset += 40

def main():
    global player_id, player_type, points
    socketio.emit('join_game', {'player_id': player_id, 'player_type': player_type})
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            move_player('left')
        if keys[pygame.K_RIGHT]:
            move_player('right')
        if keys[pygame.K_UP]:
            move_player('up')
        if keys[pygame.K_DOWN]:
            move_player('down')
        if keys[pygame.K_SPACE]:
            use_booster('silent_movement')
        
        screen.fill(WHITE)
        
        # Draw players
        for pid, pdata in players.items():
            if pdata['type'] == 'police':
                screen.blit(police_img, (pdata['x'], pdata['y']))
            else:
                screen.blit(thief_img, (pdata['x'], pdata['y']))

        # Draw leaderboard
        draw_leaderboard()

        # Draw player points
        font = pygame.font.Font(None, 36)
        points_text = font.render(f"Points: {points}", True, YELLOW)
        screen.blit(points_text, (20, 20))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

# Run the client
if __name__ == '__main__':
    thread = Thread(target=main)
    thread.start()
    socketio.run(app)
