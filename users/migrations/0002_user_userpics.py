# Generated by Django 3.1.7 on 2021-03-16 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='userPics',
            field=models.ImageField(default='user.PNG', null=True, upload_to='user/profilepics/%d/%m/'),
        ),
    ]
