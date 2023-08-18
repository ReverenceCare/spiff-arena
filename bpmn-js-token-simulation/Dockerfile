FROM node:14-alpine

RUN mkdir /app
# RUN apk update && apk add --no-cache \
#     # Install Chromium dependencies
#     chromium \
#     nss \
#     freetype \
#     harfbuzz \
#     ca-certificates \
#     ttf-freefont \
#     bash \
#     git \
#     && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY package.json /app
# RUN npm install -g webpack webpack-cli
RUN npm install

# COPY package*.json ./

# RUN npm install
COPY . /app
EXPOSE 8080
CMD [ "npm", "run", "start:example" ]
