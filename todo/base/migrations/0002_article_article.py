# Generated by Django 4.2.6 on 2023-10-23 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='article',
            field=models.TextField(blank=True, null=True),
        ),
    ]
