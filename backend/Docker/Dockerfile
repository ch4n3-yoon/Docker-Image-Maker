FROM ubuntu:20.04

RUN apt-get update -y
RUN apt-get install -y openssh-server vim

# change root password
RUN echo 'root:admin123' | chpasswd
 
# change ssh configure
RUN echo PermitRootLogin yes >> /etc/ssh/sshd_config && service ssh restart
RUN service ssh restart

CMD tail -f /dev/null
