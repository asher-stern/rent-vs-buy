from flask import Flask


app = Flask(__name__)


class AppContents(object):
    def __init__(self):
        with open('html/index.html') as f:
            self.index_contents = f.read()
        with open('html/result.html') as f:
            self.result = f.read()


app_contents = AppContents()


@app.route("/")
def index():
    return app_contents.index_contents


@app.route("/result")
def result():
    return app_contents.index_contents


if __name__ == "__main__":
    app.run()

