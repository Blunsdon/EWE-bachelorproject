# EWE-bachelorproject


## Step guide for deploying eller ændring af hjemmesiden på serveren: 

1. Luk ned for gunicorn (ps -aux // kill -9 "pidnr")
   - kun hvis hjemmesiden allerede kører <br/><br/>

1. Upload ny django 
   - i tilfælde af der allerede er et django setup, kan filerne bare overskrives, istedet for at blive slettet. <br/><br/>

1. Kør følgende kommandoer:

*lav database og indsæt tabeller:*
```
$ python manager.py makemigration
``` 
```
$ python manage.py migrate
``` 

*lav admin brugerne:*
```
$ python manage.py createsuperuser
``` 

*indsammel static filer til NGINX brug:*
```
$ python manage.py collectstatic
``` 

*indsæt opgaver til scheduler:*
```
$ python manage.py crontab add
``` 

*installer gunicorn, hvis ikke allerede installeret:*
```
$ pip install gunicorn
``` 

*kør django hjemmesiden gennem gunicorn:*
```
$ gunicorn website.wsgi:application –bind 0.0.0.0:8000 --access-logfile /var/log/web_log/gunicorn-access.log --error-logfile /var/log/web_log/gunicorn-error.log
```

4. Gå ind og fix admin brugere, og opret andre eventuelle brugere gennem admin siden <br/><br/>

5. Husk at lave en create user code 
   - hvis glemmes bliver den oprettet til midnat <br/><br/>

6. Sørg for at følgende er tilføjet i databasen, hvis beskrevende test's i diverse dokumenter vil køres: 
### Users *(Kan tilføjes gennem admin siden)*
| Name     | User Email         | Company    | Phone Number |
| :---     |        :---:       |     :---:  |        :---: |
| admin    | admin@admin.com    | ewe1       | 123456789    |
| office   | office@office.com  | ewe2       | 321654987    |
| field    | field@field.com    | ewe3       | 852369741    |

### Facilities *(Kan tilføjes gennem admin siden, eller office bruger siden)*
| Name           | Key   | Location | Owner       |
| :---           | :---: |  :---:   |   :---:     |
| facility pi    | 42    | Herning  | Jan og Marc |
| facility mobil | 69    | Herning  | Marc        |

### Jointable *(Kan tilføjes gennem admin siden, eller office bruger siden)*
|Username | Facility name  |
| :---    |      :---:     |
|field    | facility pi    |
|field    | facility mobil |


