# Generated by Django 5.0.6 on 2024-05-29 13:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_courseprerequisite_courseschedules_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courses',
            name='schedule_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.courseschedules'),
        ),
    ]
