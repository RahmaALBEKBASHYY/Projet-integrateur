import socket
import psutil

def kill_games():
    for process in psutil.process_iter():
        if process.cmdline() == ['python3', 'game/game.py']:
            print('Process found. Terminating it.')
            process.terminate()
            process_found = True

def connect_server():
    sockDB = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockDB.connect(("0.0.0.0", 10001))
    return socket

# on ferme tout les games
kill_games()
# on se connect au seveur qui va dectecter la demande de maintenance
socket = connect_server()
