# Generated by Django 4.2.5 on 2023-11-18 15:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Quora', '0011_alter_image_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]