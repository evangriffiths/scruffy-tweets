# Scruffy Tweets

A twitter bot that tweets about life as Ian McEwan's pet cocker spaniel.

![Scruffy profile](scruffy_profile.png)

Uses Llama2-7B-chat to generate the tweet content.

## Setup

Clone the repo and install dependencies:

```bash
python3 -m venv .venv/
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file containing your twitter dev keys:

```bash
CONSUMER_KEY="..." # == API key
CONSUMER_SECRET="..."
ACCESS_TOKEN="..."
ACCESS_TOKEN_SECRET="..."
```

## Build llama.cpp and download (4GB!) model parameters

```bash
make

# Verify this has worked
./build/llama.cpp/main -m build/llama-2-7b-chat.Q4_K_M.gguf --random-prompt --log-disable
```

## Run

To make a tweet as scruffy the dog:

```bash
python scruffy_tweets.py
```

## Deployment

### Deployed on Render as a docker container

Built docker image (see Dockerfile):

```bash
docker build -t scruffy-tweets-app .
docker run scruffy-tweets-app # Verify it works
docker tag egriffiths/scruffy-tweets-app:20231009-1300
docker push egriffiths/scruffy-tweets-app:20231009-1300
```

Image URL [here](https://hub.docker.com/layers/egriffiths/scruffy-tweets-app/20231009-1300/images/sha256-55fb2a144dd511a5fd10c1d06e4408917bca68b51a4415d0d9a08cc2159b4ac4?context=repo
) on dockerhub.

TODO this is unusable currently as the image is ~4GB, whereas Render's free tier allocates 512MB RAM for the web service.

### Deployed using cloud-hosted Llama2 model

While figuring out how to free-host the model and serve queries by executing the compiled llama.cpp binary, we can use [Deepinfra's cloud service](https://deepinfra.com/meta-llama/Llama-2-7b-chat-hf). With pricing at $0.0002/Ktoken, it's basically free for our needs.

We use this by specifying the command-line arg `--model-source cloud`.

Add a new environment variable to you `.env` file to enable html requests to Deepinfra:

```bash
DEEPCTLTOKEN="..."
```

The Flask web app `app.py` (hosted on [Render](https://scruffy-tweets.onrender.com)) makes a tweet when launched. This is scheduled to run daily (at 9am with a random delay) via a [cron job](https://console.cron-job.org/).
