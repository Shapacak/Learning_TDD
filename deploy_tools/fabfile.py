from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random


REPO_URL = 'https://github.com/Shapacak/Learning_TDD.git'

def deploy(folder):
    '''развернуть'''
    site_folder = f'/home/sites/{folder}'
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_venv(site_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)


def _create_directory_structure_if_necessary(site_folder):
    '''создать структуру каталогов если нужно'''
    for subfolder in ('database', 'source', 'static', 'venv'):
        run(f'mkdir -p {site_folder}/{subfolder}')


def _get_latest_source(source_folder):
    '''получить последнюю версию исходного кода'''
    if exists(source_folder + '/.git'):
        run(f'cd {source_folder} && git fetch')
    else:
        run(f'git clone {REPO_URL} {source_folder}')
    current_commit = local('git log -n 1 --format=%H%', capture=True)
    run(f'cd {source_folder} && git reset --hard {current_commit[0:9]}')


def _update_settings(source_folder, site_name):
    '''обновление настроек django'''
    settings_path = source_folder + '/superlist/settings.py'
    sed(settings_path, 'DEBUG = True', 'DEBUG = False')
    sed(settings_path,
        'ALLOWED_HOSTS =.+$',
        f'ALLOWED_HOSTS = ["{site_name}"]')
    sed(settings_path,
        'SECRET_KEY =.+$', 'from .secret_key import SECRET_KEY')
    secret_key_file = source_folder + '/superlist/secret_key.py'
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
    append(secret_key_file, f'SECRET_KEY = "django-insecure-{key}"')

def _update_venv(site_folder):
    '''обновелние виртуального окружения python'''
    venv_folder = site_folder + '/venv'
    if not exists(venv_folder + '/bin/pip'):
        run(f'python3 -m venv {venv_folder}')
    run(f'{venv_folder}/bin/pip install -r {site_folder}/source/requirements.txt')


def _update_static_files(source_folder):
    '''обновление статических файлов'''
    run(f'cd {source_folder} && ../venv/bin/python manage.py collectstatic --noinput')


def _update_database(source_folder):
    '''выполнить миграции'''
    run(f'cd {source_folder} && ../venv/bin/python manage.py migrate --noinput')

