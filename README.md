# Фонд Проекта помощи котикам!

### Супер-проект по созданию проектов и пожертвований и их распределения по открытым проектам. Наслаждайтесь :)

Клонировать репозиторий и перейти в него в командной строке:

```
git clone 
```

```
cd cat_charity_fund
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Сделать миграции:
```alembic upgrade heads```

Запустить приложение:
```uvicorn app.main:app```

Enjoy :)