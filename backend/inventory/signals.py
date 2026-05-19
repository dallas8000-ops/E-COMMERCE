"""Signal: auto-analyze sentiment on ProductReview approval."""
from django.db.models.signals import post_save
from django.dispatch import receiver

from inventory.models import ProductReview


@receiver(post_save, sender=ProductReview)
def analyze_review_sentiment(sender, instance, **kwargs):
    """Run AI sentiment analysis when a review is approved and sentiment is blank."""
    if not instance.is_approved or instance.sentiment:
        return

    try:
        from core.ai_utils import analyze_sentiment
        text = ' '.join(filter(None, [instance.title, instance.comment]))
        sentiment = analyze_sentiment(text)
        ProductReview.objects.filter(pk=instance.pk).update(sentiment=sentiment)
    except Exception:
        pass  # Non-fatal — review remains approved without sentiment tag
