# Generated by Django 5.0.3 on 2024-03-21 08:49

import time

from django.db import migrations
from django.db.models import Max


def _fill_approval_updated_at(apps, schema_editor):
    Approval = apps.get_model("approvals", "Approval")
    LogEntry = apps.get_model("admin", "LogEntry")
    ContentType = apps.get_model("contenttypes", "ContentType")

    approval_content_type, _created = ContentType.objects.get_or_create(app_label="approvals", model="approval")

    approvals_to_migrate = Approval.objects.filter(updated_at__isnull=True).prefetch_related(
        "prolongation_set", "suspension_set"
    )

    approvals_nb = 0
    start = time.perf_counter()
    while batch_approvals := approvals_to_migrate[:1000]:
        log_entries_updated_at = {
            info["object_id"]: info["updated_at"]
            for info in LogEntry.objects.filter(
                content_type=approval_content_type,
                object_id__in=[approval.pk for approval in batch_approvals],
            )
            .values("object_id")
            .annotate(updated_at=Max("action_time"))
        }
        approvals = []
        for approval in batch_approvals:
            updated_at = approval.created_at
            suspension_updated_at = max(
                [susp.updated_at for susp in approval.suspension_set.all()], default=updated_at
            )
            prolongation_updated_at = max(
                [prol.updated_at for prol in approval.prolongation_set.all()], default=updated_at
            )
            log_entry_updated_at = log_entries_updated_at.get(approval.pk, updated_at)
            approval.updated_at = max(updated_at, prolongation_updated_at, suspension_updated_at, log_entry_updated_at)
            approvals.append(approval)
        approvals_nb += Approval.objects.bulk_update(approvals, {"updated_at"})
        print(f"{approvals_nb} approvals migrated in {time.perf_counter() - start:.2f} sec")


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ("approvals", "0001_initial"),
        ("admin", "0003_logentry_add_action_flag_choices"),
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.RunPython(_fill_approval_updated_at, migrations.RunPython.noop, elidable=True),
    ]