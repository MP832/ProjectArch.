# Generated by Django 4.1.1 on 2023-07-30 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MAIL', '0015_alter_evenement_mailtemplate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evenement',
            name='mailtemplate',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='evenement',
            name='mailtemplateoutlook',
            field=models.TextField(),
        ),
    ]
