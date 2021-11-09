# EWE-bachelorproject


## Ved deploy af ny server/hjemme husk 

1. Luk ned for gunicorn (ps -aux // kill -9 "pidnr") og slet mappen inde i django-website

2. Upload ny django 

3. Kør følgende:
```
$ python manager.py makemigration
``` 
```
$ python manage.py migrate
``` 
```
$ python manage.py createsuperuser
``` 
```
$ python manage.py collectstatic
``` 
```
$ pip install gunicorn
``` 
```
$ gunicorn website.wsgi:application –bind 0.0.0.0:8000 --access-logfile /var/log/web_log/gunicorn-access.log --error-logfile /var/log/web_log/gunicorn-error.log
```
4. Gå ind og fix admin og superusers

5. Husk at lave en create user code

6. Sørg for at følgende er tilføjet: 
### Users
| Name     | User Email         | Company    | Phone Number |
| :---     |        :---:       |     :---:  |        :---: |
| admin    | admin@admin.com    | ewe1       | 123456789    |
| office   | office@office.com  | ewe2       | 321654987    |
| field    | field@field.com    | ewe3       | 852369741    |

### Facilities
| Name           | Key   | Location | Owner       |
| :---           | :---: |  :---:   |   :---:     |
| facility pi    | 42    | Herning  | Jan og Marc |
| facility mobil | 69    | Herning  | Marc        |

### Jointable
|Username | Facility name  |
| :---    |      :---:     |
|field    | facility pi    |
|field    | facility mobil |


