# Generated by Django 3.1.7 on 2021-07-03 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('raffleDraw', '0005_raffledrawplayer_payment_reference'),
    ]

    operations = [
        migrations.AddField(
            model_name='raffledrawplayer',
            name='is_winner',
            field=models.BooleanField(default=False),
        ),
    ]
