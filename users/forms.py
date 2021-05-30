from django import forms
from .models import Profile,RequestTool,ReplayTool,Contract
from home.models import Post
from django.contrib.auth import get_user_model

class Profileform(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'

class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()

	class Meta:
		model = get_user_model()
		fields = ['first_name','last_name','email','phone','address']

class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['image']

class RejectNotiForm(forms.ModelForm):
	text = forms.CharField(widget=forms.Textarea(attrs={'class':'materialize-textarea','rows':4}),
		initial="Sorry, the tool is not available now for some reasons.", required=False)
	
	class Meta:
		model = ReplayTool
		fields = ('text',)

class AcceptNotiForm(forms.ModelForm):
	text = forms.CharField(widget=forms.Textarea(attrs={'class':'materialize-textarea','rows':4}),
		initial="I accept your reruest for _ days. You can send me the contract details.", required=False)
	
	class Meta:
		model = ReplayTool
		fields = ('text',)

# class DateInput(forms.DateInput):
# 	input_type = 'date'

class Calculate(forms.ModelForm):
	# start_date = forms.DateField(disabled=True,default=) #widget=DateInput,
	period = forms.DecimalField(required=True)
	
	class Meta:
		model = Contract
		fields = ['period']

class StartContractForm(forms.ModelForm):
	# start_date = forms.DateField(disabled=True,default=) #widget=DateInput,
	period = forms.DecimalField(required=True)
	
	class Meta:
		model = Contract
		fields = ['period']