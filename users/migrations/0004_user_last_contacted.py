# Generated by Django 4.2.1 on 2024-09-25 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_address_user_date_of_birth'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_contacted',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]