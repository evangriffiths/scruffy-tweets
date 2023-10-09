FROM python:3.9-slim

WORKDIR /app

COPY . /app

# Install make and gcc, and build llama2.c
RUN apt update && apt install -y make g++
RUN cd /app/build/llama.cpp && make && cd -

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "scruffy_tweets.py"]
