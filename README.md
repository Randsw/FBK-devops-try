# Выполненое тестовое задание на должность Devops Engineer в ФБК

## Задание

* Напишите на Python скрипт, который будет из POST запроса писать значение в базу данных (использовать Postgres).
* Скрипт и БД должны быть упакованы в Docker.
* Настройте nginx, который будет запрещать GET-запросы к скрипту.
* Все должно запускаться из docker-compose.yml.
* Все сервисы должны общаться между собой через внутреннюю сеть Docker. Nginx должен быть доступен на порту 8080.

## Решение

Создано 3 контейнера:

* ***http_server*** - содержит http сервер, слушающий на порту 8000, а также адаптер к БД Postgres. При старте создает тестовую БД, если таковой нет.

* ***db*** - контейнер с БД Postgres

* ***reverse_proxy*** - контейнер с Nginx, работающий как обратный прокси-сервер на порту 8080. На уровне обратного прокси-сервера осуществляется блокировка GET запросов.

При запуске создается тестовая база данных *players* в которую будут записываться значения из POST запросов

## Запуск примера

* ```docker-compose up --build -d```

## Примеры POST запросов

* ```curl --header "Content-Type: application/json" --request POST -d '{"id":1,"name":"Pogba","role":"cm","country":"France","number":6}' http://127.0.0.1:8080```

* ```curl --header "Content-Type: application/json" --request POST -d '{"id":2,"name":"Rashford","role":"st","country":"England","number":10}' http://127.0.0.1:8080```

* ```curl --header "Content-Type: application/json" --request POST -d '{"id":3,"name":"Shaw","role":"ld","country":"England","number":23}' http://127.0.0.1:8080```