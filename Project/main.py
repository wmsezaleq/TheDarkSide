from flask_socketio import SocketIO
from app import create_app, io


app = create_app()


if __name__ == "__main__":
    io.run(app, debug=True)