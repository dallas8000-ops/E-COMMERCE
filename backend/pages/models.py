
from django.db import models


class ContactInquiry(models.Model):
	INQUIRY_TAGS = [
		('bulk_order', 'Bulk order'),
		('delivery', 'Delivery'),
		('complaint', 'Complaint'),
		('general', 'General'),
	]

	name = models.CharField(max_length=120)
	email = models.EmailField()
	subject = models.CharField(max_length=160)
	message = models.TextField()
	inquiry_tag = models.CharField(
		max_length=20,
		blank=True,
		choices=INQUIRY_TAGS,
		help_text='Auto-classified by AI on save.',
	)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-created_at']
		verbose_name_plural = 'Contact inquiries'

	def __str__(self):
		return f'{self.name} - {self.subject}'
