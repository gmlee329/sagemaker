#!/bin/bash

payload=$1
content=${2:-text/csv}

curl -F "img=@${payload}" -v http://localhost:8888/invocations
