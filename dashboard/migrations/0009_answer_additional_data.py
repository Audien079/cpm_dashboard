# Generated by Django 4.2.1 on 2024-10-25 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_alter_question_info_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='additional_data',
            field=models.JSONField(blank=True, null=True),
        ),
    ]