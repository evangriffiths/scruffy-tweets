import flask
import os

import scruffy_tweets

app = flask.Flask(__name__)

@app.route("/")
def index():
    os.system("make")
    scruffy_tweets.main(model_source="cloud")
    return flask.redirect("https://twitter.com/ScruffyActually")

if __name__ == "__main__":
    app.run()
