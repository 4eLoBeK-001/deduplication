# DeDuplication
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi) ![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white) ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
## Как запустить.

1. Клонируйте себе репозиторий
    ```
    git clone https://github.com/4eLoBeK-001/deduplication.git
    ```

2. Перейдите вглубь директории
    ```
    cd deduplication
    ```

3. Настройте переменные окружения

    Создайте и настройте .env файл по примеру `.env.example`

4. Запускаете компоус.
    ```
    docker compose up --build
    ```

5. Первааоичная авторизация

    Для того чтобы авторизоваться надо скопировать код авторизации который живёт 20 минут, и использовать его в эндпоинте `initial_auth` или по url адресу `http://{ВАШ_IP:8000}/initial_auth?auth_code={ВАШ_КОД}`
