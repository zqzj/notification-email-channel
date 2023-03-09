#!/bin/bash

docker build --no-cache -t gcr.io/viewo-g/piper/agent/runner/cpu/node14:latest -f Dockerfile .
docker push gcr.io/viewo-g/piper/agent/runner/cpu/node14:latest