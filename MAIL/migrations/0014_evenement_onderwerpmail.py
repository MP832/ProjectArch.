# Generated by Django 4.1.1 on 2023-07-30 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MAIL', '0013_evenement_mailtemplateoutlook'),
    ]

    operations = [
        migrations.AddField(
            model_name='evenement',
            name='onderwerpmail',
            field=models.CharField(default='Registreer Uw aanwezigheid', max_length=70),
            preserve_default=False,
        ),
    ]
