# Generated by Django 4.2.5 on 2023-10-22 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Quora', '0008_profile_end_year_alter_profile_start_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, default='avatar/default profile.jpg', null=True, upload_to='avatar'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='end_year',
            field=models.DateField(blank=True, help_text='time you stopped working for the company ', null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='grad_year',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='start_year',
            field=models.DateField(blank=True, help_text='time you started working for the company ', null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='topic',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
