# Generated by Django 4.2.4 on 2023-09-09 08:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_alter_choice_votes_alter_question_pub_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='pub_date',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='date published'),
        ),
    ]
