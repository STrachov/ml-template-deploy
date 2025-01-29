**Installation**
0. Enter the backend folder
1. Check postgres port in .env file
2. pip install poetry
3. poetry install
4. docker-compose up -d
5. alembic upgrade head
6. Check and update the superuser credentials in the .env file
7. python -m app.initial_data
8. python -m app.main
