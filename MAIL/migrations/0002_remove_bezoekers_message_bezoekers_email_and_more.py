# Generated by Django 4.1.1 on 2023-07-25 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MAIL', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bezoekers',
            name='message',
        ),
        migrations.AddField(
            model_name='bezoekers',
            name='email',
            field=models.CharField(default='e', max_length=70),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bezoekers',
            name='functie',
            field=models.CharField(default='e', max_length=55),
            preserve_default=False,
        ),
    ]
