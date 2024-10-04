# Generated by Django 4.2.1 on 2024-10-04 07:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_remove_question_type_name_alter_answer_yes_no_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='order',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='parent_question',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_questions', to='dashboard.question'),
        ),
    ]
