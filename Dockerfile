FROM ubuntu:20.04
RUN apt update && apt install -y apt-utils sudo curl nodejs npm vim python3
RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
RUN echo "deb https://dl.yarnpkg.com/debian/ stable main" |  tee /etc/apt/sources.list.d/yarn.list
RUN apt update; 
RUN apt install -y yarn
RUN npm install --global @nomiclabs/buidler
COPY . /awesomesauce/
WORKDIR /awesomesauce/skale-manager
RUN yarn install;
RUN npx buidler compile
RUN npx buidler test

ENTRYPOINT ["/bin/bash"]

