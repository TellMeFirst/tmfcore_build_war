#!/bin/sh -e
curl -s -d "@test/input.json" -H 'Content-Type: application/json' \
    http://127.0.0.1:8080/2.0/classify \
  |python -m json.tool
