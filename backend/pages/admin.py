from django.contrib import admin

from .models import ContactInquiry


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
	list_display = ('name', 'email', 'subject', 'created_at')
	search_fields = ('name', 'email', 'subject', 'message')
	readonly_fields = ('created_at',)
