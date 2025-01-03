from citext import CIEmailField
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.indexes import GinIndex
from django.db import models
from django.utils import timezone


class Email(models.Model):
    to = ArrayField(CIEmailField(), blank=True, verbose_name="à")
    cc = ArrayField(CIEmailField(), blank=True, default=list, verbose_name="cc")
    bcc = ArrayField(CIEmailField(), blank=True, default=list, verbose_name="cci")
    subject = models.TextField(verbose_name="sujet", blank=True)
    body_text = models.TextField(verbose_name="message", blank=True)
    from_email = CIEmailField(verbose_name="de")
    reply_to = ArrayField(CIEmailField(), blank=True, default=list, verbose_name="répondre à")
    created_at = models.DateTimeField(default=timezone.now, db_index=True, verbose_name="demande d’envoi à")
    esp_response = models.JSONField(null=True, verbose_name="réponse du fournisseur d’e-mail")

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            GinIndex(name="recipients_idx", fields=["to", "cc", "bcc"]),
        ]

    def __str__(self):
        return f"email {self.pk}: {self.subject}"

    @staticmethod
    def from_email_message(email_message):
        return Email(
            from_email=email_message.from_email,
            reply_to=email_message.reply_to,
            to=email_message.to,
            cc=email_message.cc,
            bcc=email_message.bcc,
            subject=email_message.subject,
            body_text=email_message.body,
        )
