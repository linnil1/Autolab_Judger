From python:3.8-slim
RUN apt update && apt install -y docker.io && \
    rm -rf /var/lib/apt/lists/*
ADD requirements.txt /opt
RUN pip3 install -r /opt/requirements.txt
WORKDIR /app
