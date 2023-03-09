#!/bin/bash

if test -d ./dist; then rm -r ./dist; fi
if test -d ./panels/emailChannel; then rm -r ./panels/emailChannel; fi
npm i
npm run build
cp -r ./dist ./panels/emailChannel

ls ./panels/
ls ./panels/emailChannel

python3 ./build.py
rm -r ./dist