# Generated by Django 3.1.7 on 2021-07-16 03:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('raffleDraw', '0002_raffledrawplayer_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='raffledrawbatch',
            name='when',
        ),
    ]