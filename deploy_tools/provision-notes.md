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
* sudo -u www-data stat /home/USERNAME/sites/SITENAME/static # проверка на права доступа Nginx к статическим файлам
* sudo gpasswd -a www-data USERNAME # добваление username в группу www-data, что бы Nginx мог получить доступ к статическим файлам

## Служба Gunicorn в systemd/system
* Смотреть gunicorn_systemd_*.template.conf файлы
* Заменить SITENAME
* Файл в tmp имеет расширение .sock

## Структура папок
/home/sites
└──SITENAME
    ├──database
    ├──source
    ├──static
    └──venv