# Generated by Django 2.0.3 on 2018-04-03 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0002_photo_mod_num'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='editted',
            field=models.BooleanField(default=False),
        ),
    ]
