# Generated by Django 4.2.5 on 2023-10-20 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Quora', '0007_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='end_year',
            field=models.DateField(help_text='time you stopped working for the company ', null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='start_year',
            field=models.DateField(help_text='time you started working for the company ', null=True),
        ),
    ]
