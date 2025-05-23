# Generated by Django 5.2 on 2025-05-08 20:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_alter_jobpost_show_salary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='jobPost',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobPost', to='base.jobpost'),
        ),
        migrations.AlterField(
            model_name='application',
            name='jobSeeker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobSeeker', to='base.jobseeker'),
        ),
        migrations.AlterField(
            model_name='application',
            name='resume',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resume', to='base.resume'),
        ),
    ]
