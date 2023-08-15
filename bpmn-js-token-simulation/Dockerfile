FROM node:14-alpine

RUN apk update && apk add --no-cache \
    # Install Chromium dependencies
    chromium \
    nss \
    freetype \
    harfbuzz \
    ca-certificates \
    ttf-freefont \
    bash \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY package*.json ./

RUN npm ci --only=production
COPY . .
EXPOSE 8080
CMD [ "npm", "run", "start:example" ]
