# Generated by Django 4.2.7 on 2023-11-07 10:52

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("companies", "0009_rename_siaejobdescription_jobdescription"),
        ("api", "0002_alter_siaeapitoken_siaes"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="SiaeApiToken",
            new_name="CompanyApiToken",
        ),
    ]