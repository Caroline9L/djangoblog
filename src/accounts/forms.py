from django import forms
from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout,
)

User = get_user_model()

class UserLoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput) #PI obfuscates password

	def clean(self, *args, **kwargs):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")
		# user = authenticate(username=username, password=password) #verifying user exists, not logging them in
		#alternatively, filter users:
		# user_qs = User.objects.filter(username=username) #alternative way to check user exists -- can filter through whichever field you like
		# if user_qs.count() == 1:
		# 	user = user_qs.first()
		if username and password:
			user = authenticate(username=username, password=password)
			if not user:
				raise forms.ValidationError("This user does not exist")
			if not user.check_password(password): #authenticate overrides this, filter needs it 
				raise forms.ValidationError("Incorrect Password")
			if not user.is_active:
				raise forms.ValidationError("This user is no longer active")
		return super(UserLoginForm, self).clean(*args, **kwargs) #default


class UserRegisterForm(forms.ModelForm):
	email = forms.EmailField(label="Email")
	email2 = forms.EmailField(label="Confirm Email") #change order in fields below
	password = forms.CharField(widget=forms.PasswordInput) #PI obfuscates password

	class Meta: #anything that isn't a field
		model = User
		fields = [ #order matters for function in here!
			'username',
			'email',
			'email2',
			'password',
		]

	# def clean(self, *args, **kwargs): #not on field -- general error box vs under field 
	# 	email = self.cleaned_data.get('email')
	# 	email2 = self.cleaned_data.get('email2')
	# 	print(email, email2)
	# 	if email != email2:
	# 		raise forms.ValidationError("Email addresses do not match")
	# 	email_qs = User.objects.filter(email=email)
	# 	if email_qs.exists():
	# 		raise forms.ValidationError("This address is already in use")
	# 	return super(UserRegisterForm, self).clean(*args, **kwargs) #default

	def clean_email2(self): #checks that input matches
		email = self.cleaned_data.get('email')
		email2 = self.cleaned_data.get('email2')
		if email != email2:
			raise forms.ValidationError("Email addresses do not match")
		email_qs = User.objects.filter(email=email)
		if email_qs.exists():
			raise forms.ValidationError("This address is already in use")
		return email
