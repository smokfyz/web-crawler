FROM node:16

WORKDIR /code

COPY . .
RUN npm install
RUN npm run build

RUN rm -rf ./node_modules
