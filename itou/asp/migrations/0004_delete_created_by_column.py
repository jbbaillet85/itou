# Generated by Django 4.2.5 on 2023-09-12 14:09
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("asp", "0003_remove_commune_created_by_antoine"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="commune",
            name="created_by",
        ),
    ]