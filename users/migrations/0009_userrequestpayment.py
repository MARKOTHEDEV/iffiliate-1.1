# Generated by Django 3.1.7 on 2021-05-19 01:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_seenmoneypost'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserRequestPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('isPaid', models.BooleanField(default=False)),
                ('account_number', models.CharField(max_length=160)),
                ('account_name', models.CharField(max_length=150)),
                ('bank_code', models.CharField(max_length=10)),
                ('bank_name', models.CharField(max_length=50)),
                ('recipient_code', models.CharField(max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
