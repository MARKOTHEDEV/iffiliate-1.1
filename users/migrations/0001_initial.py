# Generated by Django 3.1.7 on 2021-07-14 16:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('userEarnings', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('userPics', models.ImageField(default='user.jpg', null=True, upload_to='user/profilepics/%d/%m/')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, null=True)),
                ('membership_type', models.CharField(choices=[('Gold', 'Gold'), ('Silver', 'Silver'), ('Bronze', 'Bronze'), ('Free', 'Free')], default='Free', max_length=30)),
                ('duration', models.PositiveIntegerField(default=7)),
                ('duration_period', models.CharField(choices=[('Days', 'Days'), ('Week', 'Week'), ('Months', 'Months')], default='Day', max_length=100)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('earningLimit', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MoneyPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('content', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='UserRequestPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10)),
                ('isPaid', models.BooleanField(default=False)),
                ('account_number', models.CharField(max_length=160)),
                ('account_name', models.CharField(blank=True, max_length=150)),
                ('bank_code', models.CharField(blank=True, max_length=10)),
                ('bank_name', models.CharField(blank=True, max_length=50)),
                ('recipient_code', models.CharField(blank=True, max_length=20)),
                ('date_requested', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserMembership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference_code', models.CharField(blank=True, default='', max_length=100)),
                ('membership', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_membership', to='users.membership')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expires_in', models.DateField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('user_membership', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='subscription', to='users.usermembership')),
            ],
        ),
        migrations.CreateModel(
            name='SeenMoneyPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('postSeen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.moneypost')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PayHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paystack_charge_id', models.CharField(blank=True, default='', max_length=100)),
                ('paystack_access_code', models.CharField(blank=True, default='', max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('paid', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('who_is_getting_payed', models.CharField(blank=True, choices=[('Iffilate', 'Iffilate'), ('User', 'User')], max_length=10, null=True)),
                ('payment_for', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.membership')),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
