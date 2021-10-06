# Generated by Django 3.2.7 on 2021-10-05 13:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=80)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email adress')),
                ('phoneNumber', models.CharField(max_length=20)),
                ('company', models.CharField(max_length=120)),
                ('password', models.CharField(max_length=200)),
                ('userType', models.CharField(choices=[('Admin', 'Admin'), ('Office user', 'Office user'), ('Field user', 'Field user')], default='Field user', max_length=30)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CreateUserCode',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Facilities',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=80, unique=True)),
                ('location', models.CharField(max_length=120)),
                ('owner', models.CharField(max_length=80)),
                ('key', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Logs',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('dateTime', models.DateTimeField()),
                ('companyName', models.CharField(max_length=120)),
                ('userName', models.CharField(max_length=80)),
                ('userEmail', models.EmailField(blank=True, max_length=254, null=True)),
                ('facilityName', models.CharField(max_length=80)),
                ('facilityLocation', models.CharField(blank=True, max_length=120, null=True)),
                ('facility', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='website.facilities')),
                ('user', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='JoinTable',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('timer', models.CharField(blank=True, max_length=80, null=True)),
                ('timer_start', models.CharField(blank=True, max_length=80, null=True)),
                ('facility', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='website.facilities')),
                ('user', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
