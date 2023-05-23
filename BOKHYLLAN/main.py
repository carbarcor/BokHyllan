#detta är för att starta programmet
from website import create_app
from flask_socketio import SocketIO

app = create_app()

@app.route('/socket.io')
def socket_io():
    pass

if __name__ =='__main__':
    socketio = SocketIO(app)
    socketio.run(app, debug=True)