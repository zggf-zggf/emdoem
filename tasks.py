from invoke import task
@task
def update(c):
    c.run('git pull')
    c.run('python manage.py collectstatic')
    c.run('python manage.py migrate')
    c.sudo('systemctl restart gunicorn')
    c.sudo('systemctl restart nginx')
