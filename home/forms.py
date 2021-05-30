from django import forms
from users.models import RequestTool
from .models import Review, RATE_CHOICES

class RateForm(forms.ModelForm):
	text = forms.CharField(widget=forms.Textarea(attrs={'class':'materialize-textarea','rows':4}), required=False)
	rate = forms.ChoiceField(choices=RATE_CHOICES, widget=forms.Select(), required=True)

	class Meta:
		model = Review
		fields = ('rate','text')

class RequestToolForm(forms.ModelForm):
	text = forms.CharField(widget=forms.Textarea(attrs={'class':'materialize-textarea','rows':4}),
		initial="I would like to rent your tool for 1 day. Can you borrow me please?", required=False)
	
	class Meta:
		model = RequestTool
		fields = ('text',)