#!/bin/bash
docker run -d -p 6000:5000 --restart always --name registry registry


docker build -t runner .
docker tag runner localhost:6000/runner
docker push localhost:6000/runner

nomad job run runner.nomad

