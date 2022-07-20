#!/usr/bin/env bash

sleep 15
alembic upgrade head
exec uvicorn main:app --host 0.0.0.0 --port 8640
