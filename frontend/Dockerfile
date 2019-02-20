FROM node:8.15-alpine

WORKDIR /work

COPY . .

RUN ["npm", "install"]

EXPOSE 8080

ENV HOST=0.0.0.0

CMD ["npm", "run", "dev"]
