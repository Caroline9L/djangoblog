from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render

from .forms import SignUpForm, ContactForm

# Create your views here.
def home_view(request):
	title = "Welcome"
	if request.user.is_authenticated():
		title = "Welcome %s" %(request.user)

	form = SignUpForm(request.POST or None)
	context = {
		"title": title,
		"form": form,
	}

	if form.is_valid():
		# form.save()
		instance = form.save(commit=False)
		full_name = form.cleaned_data.get("full_name")
		if not full_name:
			full_name = "New Full Name"
		instance.full_name = full_name
		instance.save()
		context = {
			"title": "Thank You"
		}
		# print(instance.email)
		# print(instance.timestamp)
	return render(request, "home.html", context)

def contact(request):
	title = "Contact Us"
	title_align_center = True
	form = ContactForm(request.POST or None)
	if form.is_valid():
		email = form.cleaned_data.get("email")
		message = form.cleaned_data.get("message")
		full_name = form.cleaned_data.get("full_name")
		subject = "contact form"
		from_email = settings.EMAIL_HOST_USER
		to_email = [from_email, 'claporta@crossroadstech.net']
		contact_message = "%s:%s via %s"%(
				full_name, 
				message, 
				email)
		send_mail(subject, 
				contact_message, 
				from_email, 
				to_email, 
				fail_silently=False)
		
	context = {
		"title": title,
		"title_align_center": title_align_center,
		"form": form,
	}
	return render(request, "forms.html", context)