from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("siae_evaluations", "0012_evaluatedadministrativecriteria_proof_url_to_proof"),
    ]

    operations = [
        migrations.RunSQL(
            "ALTER TABLE siae_evaluations_evaluatedadministrativecriteria DROP COLUMN proof_url",
            elidable=True,
        )
    ]