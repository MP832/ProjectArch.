# Generated by Django 4.1.1 on 2023-07-24 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bezoekers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=55)),
                ('lname', models.CharField(max_length=55)),
                ('message', models.TextField()),
            ],
        ),
    ]
