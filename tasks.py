from invoke import task
@task
def update(c):
    c.run('git pull')
    c.run('python manage.py collectstatic --no-input')
    c.run('python manage.py migrate')
    print('restarting gunicorn...')
    c.sudo('systemctl restart gunicorn')
    print('restarting nginx...')
    c.sudo('systemctl restart nginx')
    print('done!')
