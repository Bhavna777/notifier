# Generated by Django 3.1.1 on 2020-11-21 18:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_auto_20201121_2356'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recieve',
            name='date',
        ),
    ]