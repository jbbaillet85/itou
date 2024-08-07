# Generated by Django 5.0.3 on 2024-03-23 08:30

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="QPV",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("code", models.CharField(max_length=8, verbose_name="code")),
                ("name", models.CharField(max_length=254, verbose_name="référence")),
                ("communes_info", models.CharField(max_length=254, verbose_name="nom des communes du QPV")),
                (
                    "geometry",
                    django.contrib.gis.db.models.fields.MultiPolygonField(
                        srid=4326, verbose_name="contour géométrique du QPV"
                    ),
                ),
            ],
            options={
                "verbose_name": "quartier de la politique de la ville",
                "verbose_name_plural": "quartiers de la politique de la ville",
                "indexes": [models.Index(fields=["code"], name="geo_qpv_code_8236a4_idx")],
            },
        ),
        migrations.CreateModel(
            name="ZRR",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("insee_code", models.CharField(max_length=5, verbose_name="code INSEE de la commune")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("C", "Classée en ZRR"),
                            ("NC", "Non-classée en ZRR"),
                            ("PC", "Partiellement classée en ZRR"),
                        ],
                        max_length=2,
                        verbose_name="classement en ZRR",
                    ),
                ),
            ],
            options={
                "verbose_name": "classification en Zone de Revitalisation Rurale (ZRR)",
                "verbose_name_plural": "classifications en Zone de Revitalisation Rurale (ZRR)",
                "indexes": [
                    models.Index(fields=["insee_code"], name="geo_zrr_insee_c_75da81_idx"),
                    models.Index(fields=["status"], name="geo_zrr_status_04ec0b_idx"),
                ],
            },
        ),
    ]
