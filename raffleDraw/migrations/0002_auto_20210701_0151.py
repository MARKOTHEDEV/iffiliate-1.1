# Generated by Django 3.1.7 on 2021-06-30 17:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('raffleDraw', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='raffledrawplayer',
            name='raffle_draw_batch',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='raffleDraw.raffledrawbatch'),
        ),
        migrations.AlterField(
            model_name='raffledrawplayer',
            name='account_number',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]