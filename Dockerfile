FROM ubuntu:latest
RUN apt update && apt install -y sudo curl nodejs npm vim
RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
RUN echo "deb https://dl.yarnpkg.com/debian/ stable main" |  tee /etc/apt/sources.list.d/yarn.list
RUN apt update; 
RUN apt install -y yarn
RUN npm install --global @nomiclabs/buidler 

COPY . /awesomesauce/
WORKDIR /awesomesauce/


ENTRYPOINT ["/bin/bash"]

