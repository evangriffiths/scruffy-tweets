import argparse
import dotenv
import json
import os
import pathlib
import random
import requests
from requests_oauthlib import OAuth1
import subprocess
import time

dotenv.load_dotenv()
consumer_key = os.environ.get("CONSUMER_KEY") # == API key
consumer_secret = os.environ.get("CONSUMER_SECRET")
access_token = os.environ.get("ACCESS_TOKEN")
access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")
deepctl_token = os.environ.get("DEEPCTLTOKEN")

def generate_tweet(prompt: str, model_source: str):
    formatted_prompt = f"[INST] {prompt} [/INST]"

    if model_source == "local":
        build_dir = pathlib.Path(__file__).parent.resolve() / "build"
        program_path = build_dir / 'llama.cpp/main'
        model_path = build_dir / 'llama-2-7b-chat.Q4_K_M.gguf'
        command = [program_path, '-m', model_path, '-p', formatted_prompt, '--log-disable', '--temp', '5']

        completed_process = subprocess.run(
            command, 
            stdout=subprocess.PIPE,  # Capture standard output
            text=True,
            check=True,
        )

        # Remove prompt and other surrounding characters from the response
        tweet = completed_process.stdout.strip()[len(formatted_prompt):].strip().strip('"')
    elif model_source == "cloud":
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {deepctl_token}"
        }
        response = requests.post(
            url="https://api.deepinfra.com/v1/inference/meta-llama/Llama-2-7b-chat-hf",
            headers=headers,
            data=json.dumps(
                {
                    "input": formatted_prompt,
                    "temperature": 0.95,
                }
            )
        )
        if not response.ok:
            raise Exception(response.status_code, response.text)
        tweet = response.json()["results"][0]["generated_text"].strip().strip('"')
    else:
        raise ValueError(f"Invalid model source: {model_source}")

    # Crop to 280 characters to ensure a valid tweet
    tweet = tweet[:280]
    return tweet


def format_response(fact):
    return {"text": fact}


def main(model_source: str = "local", random_delay: int = None, return_tweet_only: bool = False):
    auth = OAuth1(consumer_key, consumer_secret, access_token, access_token_secret)
    action = random.choice(["post"]) # TODO support "reply"
    if random_delay:
        time.sleep(random.randint(0, random_delay))
    if action == "post":
        prompt = "You are Ian McEwan's loyal and intelligent pet cocker spaniel. Write a short tweet that referencing ONLY one of: a fact about Ian McEwan, your relationship with him, or your thoughts on one of his (specifically named) works. Don't be too sentimental in your tweet. Include specific factual detail bout his work where appropriate (e.g. book titles, character names, etc.)."
        tweet = generate_tweet(prompt=prompt, model_source=model_source)
        if return_tweet_only:
            return tweet
        else:
            response = requests.post(
                auth=auth,
                url="https://api.twitter.com/2/tweets",
                json={"text": tweet},
                headers={"Content-Type": "application/json"}
            )
            if not response.ok:
                raise Exception(response.status_code, response.text)

    elif action == "reply":
        # Searching tweets via API requires 'basic'  access ($100/month)!
        # url = 'https://api.twitter.com/1.1/search/tweets.json?q=nasa&result_type=popular'
        # response = requests.get(url, auth=auth)
        raise NotImplementedError("Replies not implemented yet")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-source", type=str, choices=["local", "cloud"], default="local")
    parser.add_argument("--print-only", action="store_true", default=False)
    args = parser.parse_args()
    if args.print_only:
        print(main(model_source=args.model_source, return_tweet_only=True))
    else:
        main(model_source=args.model_source)
