import dotenv
import os
import random
import requests
from requests_oauthlib import OAuth1
import subprocess

dotenv.load_dotenv()
consumer_key = os.environ.get("CONSUMER_KEY") # == API key
consumer_secret = os.environ.get("CONSUMER_SECRET")
access_token = os.environ.get("ACCESS_TOKEN")
access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")
bearer_token = os.environ.get("BEARER_TOKEN")
program_path = './build/llama.cpp/main'
model_path = 'build/llama-2-7b-chat.Q4_K_M.gguf'


def generate_tweet(prompt):
    formatted_prompt = f"PRETEXT: {prompt} RESPONSE: "
    command = [program_path, '-m', model_path, '-p', formatted_prompt, '--log-disable']
    completed_process = subprocess.run(
        command, 
        stdout=subprocess.PIPE,  # Capture standard output
        text=True,
        check=True,
    )

    # Remove "PRETEXT: ..." from the response
    return completed_process.stdout[len(formatted_prompt):]


def format_response(fact):
    return {"text": "{}".format(fact)}

def main():
    auth = OAuth1(consumer_key, consumer_secret, access_token, access_token_secret)
    action = random.choice(["post"]) # TODO support "reply"
    if action == "post":
        prompt = "You are Ian McEwan's loyal and intelligent pet cocker spaniel. Write a short tweet that referencing ONLY one of: a fact about Ian McEwan, your relationship with him, or your thoughts on one of his (specifically named) works. Don't be too sentimental in your tweet. Include specific factual detail bout his work where appropriate (e.g. book titles, character names, etc.)."
        request = requests.post(
            auth=auth,
            url="https://api.twitter.com/2/tweets",
            json=format_response(generate_tweet(prompt=prompt)),
            headers={"Content-Type": "application/json"}
        )
        if not request.ok:
            raise Exception(request.status_code, request.text)
    elif action == "reply":
        # Searching tweets via API requires 'basic'  access ($100/month)!
        # url = 'https://api.twitter.com/1.1/search/tweets.json?q=nasa&result_type=popular'
        # response = requests.get(url, auth=auth)
        raise NotImplementedError("Replies not implemented yet")

if __name__ == "__main__":
    main()
