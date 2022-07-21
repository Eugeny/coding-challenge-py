#!/bin/sh
docker run -it -v $(pwd):/app python python /app/main.py
