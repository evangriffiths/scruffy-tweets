# Scruffy Tweets

A twitter bot that tweets about life as Ian McEwan's pet cocker spaniel.

Uses Llama2 to generate the tweet content.

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
