from fabric.api import run
from fabric.context_managers import settings


def _get_manage_dot_py(folder):
    '''получить manage.py'''
    return f'~/shap/sites/superlist/venv/bin/python ~/shap/sites/superlist/source/manage.py'


def reset_database(host):
    '''обнулить базу данных'''
    manage_dot_py = _get_manage_dot_py()
    with settings(host_string=f'shap@{host}'):
        run(f'{manage_dot_py} flush --noinput')


def create_session_on_server(host, email):
    '''создать сеанс на сервере'''
    manage_dot_py = _get_manage_dot_py()
    with settings(host_string=f'shap@{host}'):
        session_key = run(f'{manage_dot_py} create_session {email}')
        return session_key.strip()
