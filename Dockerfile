FROM ubuntu:latest

RUN apt update && apt install  openssh-server sudo -y

RUN useradd -rm -d /home/ubuntu -s /bin/bash -g root -G sudo -u 1000 admin 

RUN  echo 'admin:1234' | chpasswd

RUN service ssh start

RUN sudo apt-get update -y

RUN sudo apt-get install git -y

RUN sudo apt-get install python3 -y

RUN sudo apt-get install pip -y

RUN sudo apt-get install net-tools -y

ENV TZ=Asia/Jerusalem

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN sudo apt-get install -y python3-scapy

WORKDIR "/home/ubuntu/"

RUN git clone https://zachibs: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@github.com/zachibs/ComputerNetworksFinal.git

WORKDIR "/home/ubuntu/ComputerNetworksFinal"

RUN pip install -r requirements.txt

RUN sudo pip install -r requirements.txt

RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

RUN chmod u+x docker_entrypoint.sh

EXPOSE 22

CMD python3 /home/ubuntu/ComputerNetworksFinal/find_interface.py; sh /home/ubuntu/ComputerNetworksFinal/docker_entrypoint.sh; /usr/sbin/sshd -D
