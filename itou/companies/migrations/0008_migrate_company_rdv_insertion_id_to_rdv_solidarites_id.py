# Generated by Django 5.0.9 on 2024-09-12 09:02
import time

from django.db import migrations
from django.db.models import F


def set_companies_rdv_solidarites_id(apps, schema_editor):
    start = time.perf_counter()
    companies_processed = (
        apps.get_model("companies", "Company")
        .objects.exclude(rdv_insertion_id__isnull=True)
        .update(rdv_solidarites_id=F("rdv_insertion_id"))
    )
    print(f"{companies_processed} companies migrated in {time.perf_counter() - start:.2f} sec")


def set_companies_rdv_insertion_id(apps, schema_editor):
    start = time.perf_counter()
    companies_processed = (
        apps.get_model("companies", "Company")
        .objects.exclude(rdv_solidarites_id__isnull=True)
        .update(rdv_insertion_id=F("rdv_solidarites_id"))
    )
    print(f"{companies_processed} companies migrated in {time.perf_counter() - start:.2f} sec")


class Migration(migrations.Migration):
    dependencies = [
        ("companies", "0007_company_rdv_solidarites_id"),
    ]

    operations = [
        migrations.RunPython(set_companies_rdv_solidarites_id, set_companies_rdv_insertion_id, elidable=True),
    ]