# Generated by Django 5.1 on 2024-09-02 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_customerprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerprofile',
            name='phone_number',
            field=models.IntegerField(default=0),
        ),
    ]
