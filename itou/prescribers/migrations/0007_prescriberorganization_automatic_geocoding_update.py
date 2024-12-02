# Generated by Django 5.0.9 on 2024-10-10 09:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("prescribers", "0006_prescriberorganization_prevent_validated_authorization_if_other"),
    ]

    operations = [
        migrations.AddField(
            model_name="prescriberorganization",
            name="automatic_geocoding_update",
            field=models.BooleanField(
                default=True,
                help_text="Si cette case est cochée, les coordonnées géographiques seront mises à jour si l'adresse "
                "est correctement renseignée dans le formulaire d'admin.",
                verbose_name="recalculer le geocoding",
            ),
        ),
    ]