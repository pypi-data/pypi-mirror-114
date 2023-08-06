import flask
import time

app = flask.Flask(__name__)

@app.route('/')
def index():
    time.sleep(5)
    return 'hello world'

def main():
    app.run(threaded=True)

if __name__ == "__main__":
    main()
