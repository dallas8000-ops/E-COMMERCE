from django import forms


class ContactInquiryForm(forms.Form):
	name = forms.CharField(max_length=120)
	email = forms.EmailField()
	subject = forms.CharField(max_length=160)
	message = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}))
