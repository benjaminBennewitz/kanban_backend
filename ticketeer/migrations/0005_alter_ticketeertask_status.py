# Generated by Django 5.0.6 on 2024-06-26 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketeer', '0004_alter_ticketeertask_prio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticketeertask',
            name='status',
            field=models.CharField(choices=[('urgent', 'Urgent'), ('todo', 'To Do'), ('inProgress', 'In Progress'), ('done', 'Done')], default='todo', max_length=10),
        ),
    ]
