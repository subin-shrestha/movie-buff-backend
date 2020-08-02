# Generated by Django 2.2.2 on 2020-08-02 17:17

from django.db import migrations
import shortuuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('autho', '0004_auto_20200802_1235'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='idx',
            field=shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22, unique=True),
        ),
    ]
