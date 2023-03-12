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

RUN sudo apt-get install -y python3-scapy

RUN git clone https://zachibs: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@github.com/zachibs/ComputerNetworksFinal.git

WORKDIR "/ComputerNetworksFinal"

RUN pip install -r requirements.txt

RUN sudo pip install -r requirements.txt

RUN python3 find_interface.py

RUN sh

EXPOSE 22

CMD ["/usr/sbin/sshd","-D"]

