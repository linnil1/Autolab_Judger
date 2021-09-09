FROM ubuntu:20.04
RUN apt update -y && \
    apt install -y procps make sudo python3-pip python3-dev git wget curl unzip && \
    useradd autolab && \
    echo "autolab ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && \
    mkdir -p /home/autolab && chown autolab:autolab /home/autolab
WORKDIR /home/autolab
USER autolab
