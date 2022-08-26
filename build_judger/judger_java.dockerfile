FROM openjdk:14-slim
RUN apt update -y && \
    apt install -y procps make python3 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /home
RUN mkdir autolab output && useradd autolab && \
    chmod o-rwx /boot /media /opt /root /sbin /dev /mnt /proc /run /srv /tmp /var
# /lib64 /etc /lib /bin /sys /usr /home 
ENV LANGUAGE=java
CMD /bin/bash
