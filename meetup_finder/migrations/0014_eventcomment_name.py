# Generated by Django 3.1.2 on 2020-11-16 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetup_finder', '0013_auto_20201116_1801'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventcomment',
            name='name',
            field=models.CharField(default=5, max_length=80),
            preserve_default=False,
        ),
    ]
