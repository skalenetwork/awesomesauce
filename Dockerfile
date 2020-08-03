FROM ubuntu:18.04 
RUN apt update && apt install -y apt-utils sudo gnupg2 git curl vim python3
RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
RUN curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -
RUN echo "deb https://dl.yarnpkg.com/debian/ stable main" |  tee /etc/apt/sources.list.d/yarn.list
RUN apt update; 
RUN apt install -y nodejs yarn
RUN apt install -y build-essential gcc g++
COPY . /awesomesauce/
RUN cp /awesomesauce/insecure_test_keys.env /awesomesauce/skale-manager/.env
WORKDIR /awesomesauce/skale-manager
RUN yarn install;
RUN npm install --global @nomiclabs/buidler
RUN npx buidler compile
#RUN npx buidler test

ENTRYPOINT ["/bin/bash", "-c"]
CMD ["npx buidler node"]
