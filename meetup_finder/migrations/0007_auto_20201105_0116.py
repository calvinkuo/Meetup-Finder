# Generated by Django 3.1.1 on 2020-11-05 06:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetup_finder', '0006_auto_20201105_0029'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='events',
            options={'permissions': (('can_delete', 'Can delete event'),)},
        ),
    ]
