# Generated by Django 2.1.2 on 2018-10-12 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contacts',
            name='email',
            field=models.CharField(max_length=100),
        ),
    ]
