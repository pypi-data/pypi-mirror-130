ARG VERSION
FROM node:$VERSION as build

WORKDIR /app

COPY package.json .
COPY yarn.lock .

RUN yarn

FROM node:$VERSION

WORKDIR /app_deps

COPY --from=build /app/node_modules ./node_modules

WORKDIR /app
COPY entrypoint.sh /usr/local/bin/
ENTRYPOINT ["entrypoint.sh"]
CMD ["yarn", "start"]
