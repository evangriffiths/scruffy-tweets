import flask

import scruffy_tweets

app = flask.Flask(__name__)

@app.route("/")
def index():
    # Note 1: cron job times out after 30s: https://blog.cron-job.org/service/2021/12/01/errors-explained-timeout.html
    # so set `random_delay` to <20s to be safe.
    # Note 2: if `model_source` is set to "local", need to call `os.system("make")` first.
    if "do_tweet" in flask.request.args:
        # Require a request arg to prevent tweets from random visitors
        scruffy_tweets.main(model_source="cloud", random_delay=None)
        return flask.redirect("https://twitter.com/ScruffyActually")
    else:
        tweet = scruffy_tweets.main(model_source="cloud", return_tweet_only=True)
        return flask.jsonify(error=f"Tweet contents: {tweet}. To post, add /?do_tweet to the html request"), 400

if __name__ == "__main__":
    app.run()
