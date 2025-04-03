# Телеграм бот для приюта животных

<p align="center">
  <img src="https://predannoeserdce.ru/wp-content/themes/catheart/img/kot_reporting.gif" alt="Animal Shelter logo">
</p>

Чат бот предназначен для координации действий посетителей и волонтеров приюта. Поиска участников, волонтеров для мероприятий, сбор пожертвований для определенных нужд, подачи информации. Пользователь бота может просматривать нужды приюта, откликаться на призывы донатить, участвовать в мероприятиях, откликаться на анонсы. Узнавать информацию, которая его интересует, проходить по ссылкам, смотреть фото, присылать фото.

******

## Техническое задание

Подробная информация о задаче в [ТЗ](./TASK.md)

******

## Структура проекта

```
animal-shelter-bot/
├── animal_shelter_bot/
│   └── main.py
├── .env
├── .gitignore
├── pyproject.toml
├── README.md
└── TASK.md
```

******

## Начало работы с проектом

1. Клонировать репозиторий:

```bash
git clone https://github.com/Gouzhurou/animal-shelter-bot.git
```

2. Установите Poetry (если нет):

```bash
pip install poetry
```

3. Установите зависимости:

```bash
poetry install
```

***

## Разработка

1. Создать новую ветку на основе main:

```bash
git checkout -b main <feature/branch_name>
```

2. Начать внесение изменений в своей новосозданной ветке: в ветке main не работаем!

3. Когда вы закончите редактирование и локальное тестирование, проверьте код:

```bash
poetry run pylint animal_shelter_bot/
```

4. Сохраните изменения

```bash
git add modified_files
git commit
```

5. Залейте изменения на удаленный репозиторий:

```bash
git push
```

*****

## Запуск

```bash
poetry run python -m animal_shelter_bot.main
```

*****

## Соглашения по разработке

* branch: `<feature/my-branch>`
* commit: `feat: commit message`
* один PR = один commit
  * Создаете новый commit
  * Делаете squash с предыдущим
  * `git push -f`
* одна feature = один PR
* актуальные изменения из `main` подтягиваем с помощью rebase, не merge!
