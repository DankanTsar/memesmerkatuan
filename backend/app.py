from app import app
host = "0.0.0.0"
port = 8080
debug = True
threaded = True

if __name__ == "__main__":
    app.run(host=host, port=port, debug=debug, threaded=threaded)
