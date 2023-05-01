#syntax=docker/dockerfile:1

FROM node:16.3.0-alpine
WORKDIR /frontend
COPY package.json package.json
COPY package-lock.json package-lock.json
RUN npm install

COPY .env .
COPY /public ./public
COPY /src ./src
CMD ["npm", "run" ,"start"]
