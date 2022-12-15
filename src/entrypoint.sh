#!/usr/bin/env sh

gunicorn main:app --reload -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000