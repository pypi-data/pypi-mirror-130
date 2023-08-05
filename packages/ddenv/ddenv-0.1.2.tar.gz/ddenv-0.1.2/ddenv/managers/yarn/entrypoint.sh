#!/bin/sh

ln -s /app_deps/node_modules /app/node_modules
"$@"
rm /app/node_modules
