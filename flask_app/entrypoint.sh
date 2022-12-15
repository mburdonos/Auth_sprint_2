#!/usr/bin/env sh

python pg_wait.py

python redis_wait.py

alembic revision --message="initial" --autogenerate

alembic upgrade head

flask create-superuser admin admin admin@gmail.com Maksim Maksimov

python main.py