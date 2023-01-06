# Integrator service

## Overview



## Local dev

1. [Скачать и настроить PATH для poetry](https://python-poetry.org/docs/) или `pip install poetry`
2. В корне проекта выполнить
   1. `poetry install`
   2. `poetry run uvicorn app.main:app --reload`


## Docker

### Docker on windows 11

1. install [docker desktop](https://www.docker.com/get-started/)
2. enable [wsl2](https://pureinfotech.com/install-windows-subsystem-linux-2-windows-10/)
3. Перейти в корень проекта
4. `docker-compose build`
5. `docker-compose up`