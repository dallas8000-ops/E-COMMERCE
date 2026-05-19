"""Signal: auto-classify ContactInquiry on creation."""
from django.db.models.signals import post_save
from django.dispatch import receiver

from pages.models import ContactInquiry


@receiver(post_save, sender=ContactInquiry)
def auto_classify_inquiry(sender, instance, created, **kwargs):
    """Run AI classifier when a new inquiry is saved without a tag."""
    if not created or instance.inquiry_tag:
        return

    try:
        from core.ai_utils import classify_inquiry
        tag = classify_inquiry(instance.subject, instance.message)
        # Use update() to avoid triggering the signal again and skip full_clean.
        ContactInquiry.objects.filter(pk=instance.pk).update(inquiry_tag=tag)
    except Exception:
        pass  # AI failure is non-fatal — inquiry still saved without tag
