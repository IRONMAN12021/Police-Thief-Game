from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import random

app = Flask(__name__)
socketio = SocketIO(app)

players = {}
leaderboard = {}
game_started = False

@app.route('/')
def index():
    return "Multiplayer Police and Thief Game Server"

@socketio.on('connect')
def handle_connect():
    print('Player connected')

@socketio.on('join_game')
def handle_join_game(data):
    global game_started
    player_id = data['player_id']
    player_type = data['player_type']
    
    if player_id not in players:
        players[player_id] = {
            'type': player_type, 
            'x': random.randint(50, 750), 
            'y': random.randint(50, 550),
            'points': 0,
            'boosters': {'silent_movement': False}
        }
        leaderboard[player_id] = players[player_id]['points']
        emit('player_joined', players[player_id], broadcast=True)
        
        if player_type == 'thief' and not game_started:
            game_started = True
            start_game()
    
    emit('current_players', players)

@socketio.on('move_player')
def handle_move_player(data):
    player_id = data['player_id']
    direction = data['direction']
    
    if player_id in players:
        if players[player_id]['boosters']['silent_movement']:
            movement_speed = 8
        else:
            movement_speed = 5

        if direction == 'left':
            players[player_id]['x'] -= movement_speed
        elif direction == 'right':
            players[player_id]['x'] += movement_speed
        elif direction == 'up':
            players[player_id]['y'] -= movement_speed
        elif direction == 'down':
            players[player_id]['y'] += movement_speed
        
        emit('player_moved', players[player_id], broadcast=True)

def start_game():
    emit('game_started', broadcast=True)

@socketio.on('use_booster')
def handle_use_booster(data):
    player_id = data['player_id']
    booster_type = data['booster_type']
    
    if player_id in players and players[player_id]['points'] >= 10:
        players[player_id]['points'] -= 10
        players[player_id]['boosters'][booster_type] = True
        emit('booster_activated', {'player_id': player_id, 'booster_type': booster_type}, broadcast=True)

@socketio.on('update_points')
def handle_update_points(data):
    player_id = data['player_id']
    points = data['points']
    
    if player_id in players:
        players[player_id]['points'] += points
        leaderboard[player_id] = players[player_id]['points']
        emit('points_updated', {'player_id': player_id, 'points': players[player_id]['points']}, broadcast=True)
        emit('leaderboard_updated', leaderboard, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    print('Player disconnected')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
