# django-school-project

![python linting](https://github.com/code-n-cry/django-school-project/actions/workflows/python-linting.yml/badge.svg)

![python testing](https://github.com/code-n-cry/django-school-project/actions/workflows/python-testing.yml/badge.svg)

## Описание
Выпускной проект для интенисов академии яндекса🎓

## Технологии📜
- Django
- Tailwind

## TODOs🏷️
- [ ] Сделать возможность выбрать лидера(ов), который будет назначать задачи команде(при этом каждый член команды может создавать задачи себе)
- [ ] Создание открытых команд и возможность другим пользователям присоединиться к ним через поиск
- [ ] Сбор статистики по пользователю и команде
- [ ] Создание проектов, объединяющих несколько команд
- [ ] Рейтинг лидеров и сотрудников
- [ ] Календарь митапов
По возможности:
- [ ] Отслеживание времени, проведённого в работе над заданием и дедлайна(общее и по участникам команды)
- [ ] Создание чата для обсуждения вопросов


## Руководство по запуску🔑
Для включения в git-режиме:
- Клонировать репозиторий с помощью git

  Для этого в консоль ввести команду:
  ```Shell
  git clone https://github.com/code-n-cry/django-school-project.git
  ```
  Она **скопирует папку с кодом** из GitHub

- Перейти в папку **django-school-project**

- Создать venv(ниже код в консоли для этого):
  | **Linux/MaxOS** | Windows |
  | --------------- | ------- |
  | ```python3 -m venv /<имя_папки> ``` | ``` python -m venv \<имя_папки> ``` |
  
  Команда создаст вирутальное окружение Python, позволяющее устанавливать нужные версии библиотек без конфликтов с уже установленными.

- Активировать venv
  | **Linux/MaxOS** | Windows |
  | --------------- | ------- |
  | ``` source <имя_папки_с_venv>/bin/activate ``` | ``` <имя_папки_c_venv>\Scripts\activate.bat ``` |
  
  Немного левее текущей строки в скобках должно появиться имя папки c venv - это говорит о том, что команда сработала и вы вошли в окружение.

- Установить зависимости(библиотеки, необходимые для работы проекта) 
  | **Linux/MaxOS** | Windows |
  | --------------- | ------- |
  | ``` pip3 install -r requirements/basic-requirements.txt ``` | ``` pip install -r requirements/basic-requirements.txt ``` |
  | ``` pip3 install -r requirements/dev-requirements.txt ``` | ``` pip install -r requirements/dev-requirements.txt ``` |
  | ``` pip3 install -r requirements/test-requirements.txt ``` | ``` pip install -r requirements/test-requirements.txt ``` |
  
  Зачем нужен каждый из файлов?
  
  - **basic-requirements.txt** - здесь находятся самые приоритетные для работы проекта библиотеки корневые(однако, без установки трёх файлов зависимостей запустить вы его всё равно не сможете😅)
  
  - **dev-requirements.txt** - здесь находятся библиотеки, которые помогают разработке проекта
  
  - **test-requirements.txt** - библиотеки, необходимые для тестирования
  
- Запустить сервер:
  | **Linux/MaxOS** | Windows |
  | --------------- | ------- |
  | ``` python3 manage.py runserver ``` | ``` python manage.py runserver ``` |
  
  Для этого необходимо находиться в одной директории с файлом manage.py(в консоли)

- Критичные для безопасности проекта и конфигурационные переменные находятся в файле example.env. Скопируйте его с помощью консольной команды
  ``` cp .env.example .env ```

  и, при необходимости, отредактируйте.
 
 ## Запуск БД
 - Обнаружить изменения в коде моделей:
  | **Linux/MaxOS** | Windows |
  | --------------- | ------- |
  | ``` python3 manage.py makemigrations ``` | ``` python manage.py makemigrations ``` |
  
- Применить все миграции, включая начальную:
  | **Linux/MaxOS** | Windows |
  | --------------- | ------- |
  | ``` python3 manage.py migrate ``` | ``` python manage.py migrate ``` |
  
 Здесь ещё будет ER-диаграмма и не только! Возвращайтесь😻
