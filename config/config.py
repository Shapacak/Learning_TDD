import os


def set_staging_server():
    os.environ['STAGING_SERVER'] = '95.163.243.42'


set_staging_server()