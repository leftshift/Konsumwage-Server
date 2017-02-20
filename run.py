from main import create_app, socketio, test


app = create_app(debug=False, testing=True)

if __name__ == '__main__':
    socketio.run(app)
