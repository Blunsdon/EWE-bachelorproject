# EWE-bachelorproject


ved deploy af ny server/hjemme husk 

1. luk ned for gunicorn (ps -aux // kill -9 "pidnr") og slet mappen inde i Django-final-server

2. upload ny django 

3. kør følgende
```
$ python manager.py makemigration
$ python manage.py migrate
$ python manage.py createsuperuser
$ python manage.py collectstatic
$ pip install gunicorn
$ gunicorn website.wsgi:application –bind 0.0.0.0:8000 --access-logfile /var/log/web_log/gunicorn-access.log --error-logfile /var/log/web_log/gunicorn-error.log
```
4. Gå ind og fix admin og superusers

5. Sørg for at følgende er tilføjet: 

admin
admin@admin.com
ewe1
123456789

office
office@office.com
ewe2
321654987

field
field@field.com
ewe3
852369741

facility pi
Herning
Jan og Marc
42


facility mobil
Herning
Marc
69

jointable: field -> facility pi
jointable: field -> facility mobil

lave en create user code

