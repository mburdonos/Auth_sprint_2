#!/usr/bin/env sh

python .\utils\pg_wait.py

python .\utils\redis_wait.py

alembic revision --message="initial" --autogenerate

alembic upgrade head

flask create-superuser admin admin admin@gmail.com Maksim Maksimov

python main.py