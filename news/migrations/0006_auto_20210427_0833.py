# Generated by Django 3.1.7 on 2021-04-27 08:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_auto_20210427_0819'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comments',
            options={'ordering': ['date_time'], 'verbose_name_plural': 'Comments'},
        ),
    ]
