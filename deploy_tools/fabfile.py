from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run, sudo
import random

REPO_URL = 'https://github.com/mattkohl/the_right_rhymes_beta.git'


def deploy():
    site_folder = '/home/{}'.format(env.user)
    virtualenv_folder = site_folder + "/.virtualenvs/the_right_rhymes_beta"
    source_folder = site_folder + '/the_right_rhymes_beta'
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(virtualenv_folder, source_folder)
    _update_static_files(virtualenv_folder, source_folder)
    _update_database(virtualenv_folder, source_folder)
    _restart_apache()


def _get_latest_source(source_folder):
    if exists(source_folder + '/.git'):
        run('cd {} && git fetch'.format(source_folder))
    else:
        run('git clone {} {}'.format(REPO_URL, source_folder))
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run('cd {} && git reset --hard {}'.format(source_folder, current_commit))


def _update_settings(source_folder, site_name):
    settings_path = source_folder + '/dictionary/dictionary/settings.py'
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    sed(settings_path,
        'ALLOWED_HOSTS =.+$',
        'ALLOWED_HOSTS = ["{}"]'.format(site_name)
        )
    secret_key_file = source_folder + '/dictionary/dictionary/secret_key.py'
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, 'SECRET_KEY = "{}"'.format(key))
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')


def _update_virtualenv(virtualenv_folder, source_folder):
    run('{}/bin/pip install -r {}/requirements.txt'.format(virtualenv_folder, source_folder))


def _update_static_files(virtualenv_folder, source_folder):
    run('source /etc/apache2/envvars && cd {}/dictionary'.format(source_folder) + ' && {}/bin/python manage.py collectstatic --noinput'.format(virtualenv_folder))


def _update_database(virtualenv_folder, source_folder):
    run('source /etc/apache2/envvars && cd {}/dictionary'.format(source_folder) + ' && {}/bin/python manage.py migrate --noinput'.format(virtualenv_folder))


def _restart_apache():
    sudo('systemctl restart apache2')
