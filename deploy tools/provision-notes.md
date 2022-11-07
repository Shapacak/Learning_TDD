Обеспечение работы нового сайта
===============================
## Необходимые пакеты
* nginx
* python
* venv + pip
* Git

Например в Ubuntu:
    sudo add-apt-repository ppa:fkrull//deadsnakes
    sudo apt-get install nginx git python3.10 python3.10-venv

## Конфигурация нового узла Nginx
* Смотреть файл nginx.template.conf
* Заменить SITENAME

## Служба systemd
* Смотреть gunicorn_systemd_*.template.conf файлы
* Заменить SITENAME

## Структура папок
/home/sites
└──SITENAME
    ├──database
    ├──source
    ├──static
    └──venv