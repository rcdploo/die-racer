import os
import pty
import subprocess
import threading
import select
import flask
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'die-racer-secret')
socketio = SocketIO(app, cors_allowed_origins="*")

GAME_SCRIPT = os.path.join(os.path.dirname(__file__), 'main.py')

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def on_connect():
    """Start the game process when a player connects."""
    sid = flask.request.sid

    # Create a pseudo-terminal so the game gets proper terminal I/O
    master_fd, slave_fd = pty.openpty()

    env = os.environ.copy()
    env['PYTHONUNBUFFERED'] = '1'

    proc = subprocess.Popen(
        ['python3', '-u', GAME_SCRIPT],
        stdin=slave_fd,
        stdout=slave_fd,
        stderr=slave_fd,
        close_fds=True,
        env=env
    )

    os.close(slave_fd)

    # Store per-session state
    app.sessions = getattr(app, 'sessions', {})
    app.sessions[sid] = {'proc': proc, 'master_fd': master_fd}

    def read_output():
        """Read game output and forward to browser."""
        while True:
            try:
                r, _, _ = select.select([master_fd], [], [], 0.1)
                if r:
                    data = os.read(master_fd, 1024)
                    if data:
                        socketio.emit('output', {'data': data.decode('utf-8', errors='replace')}, to=sid)
                elif proc.poll() is not None:
                    socketio.emit('game_over', {}, to=sid)
                    break
            except OSError:
                socketio.emit('game_over', {}, to=sid)
                break

    thread = threading.Thread(target=read_output, daemon=True)
    thread.start()

@socketio.on('input')
def on_input(data):
    """Forward player keystrokes to the game process."""
    sid = flask.request.sid
    sessions = getattr(app, 'sessions', {})
    if sid in sessions:
        master_fd = sessions[sid]['master_fd']
        try:
            os.write(master_fd, data['key'].encode('utf-8'))
        except OSError:
            pass

@socketio.on('disconnect')
def on_disconnect():
    """Clean up when player leaves."""
    sid = flask.request.sid
    sessions = getattr(app, 'sessions', {})
    if sid in sessions:
        try:
            sessions[sid]['proc'].terminate()
            os.close(sessions[sid]['master_fd'])
        except Exception:
            pass
        del sessions[sid]

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port, debug=False)
