from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import SignUpForm
import requests
from .models import Account
from django.contrib.auth.decorators import login_required


# Create your views here.

def home(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have successfully signed in")
            user_name = request.user.username
            email = request.user.email

            account = Account.objects.get(user_id=request.user.id)
            print(user_name,email,account)
            return render(request, 'home.html', {'username': user_name, 'email': email, 'account': account})


        else:
            messages.error(request, "There was an error while signing in")
            return redirect('home')
    else:
        return render(request, 'home.html')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Information saved successfully! Verify phone number to continue")
            user_id = request.user.id
            return redirect('phone_verification')
    else:
        form = SignUpForm()

    return render(request, 'register.html', {'form': form})

@login_required
def verify_phone_number(request):
    if request.method == 'POST':
        # Process the phone number, send verification code through WhatsApp, and set verification_code_sent to True.
        # Code to send the verification code goes here.
        phone = request.POST.get('phone_number')
        url = 'http://13.51.196.90:3000/trigger-function'
        payload = {'phone_number': phone}
        user_id = request.user.id
        phone_number = phone
        verified = False
        account = Account(user_id=user_id, phone_number=phone_number, verified=verified)
        account.save()


        try:
            response = requests.get(url, params=payload)
            response.raise_for_status()
            code = response.text.replace('Message successfully sent. Verification code is: ', '')

            # Store the code in the session
            request.session['verification_code'] = code

            return render(request, 'mobile.html', {'verification_code_sent': True})

        except requests.exceptions.RequestException as e:
            messages.error(request, 'Error while sending verification code.')
            print(f"Error: {e}")
            return render(request, 'mobile.html', {'verification_code_sent': False})

    else:
        return render(request, 'mobile.html', {'verification_code_sent': False})


def verify_code(request):
    if request.method == 'POST':
        # Retrieve the code from the session
        code = request.session.get('verification_code', None)
        if not code:
            # Handle the case where the code is not found in the session
            # Redirect or show an error message, etc.
            return redirect('verify_phone_number')

        # Process the code and check if it matches the user input.
        user_input_code = request.POST.get('verification_code')
        if code == user_input_code:
            messages.success(request, "Phone number successfully Verified")
            account = Account.objects.get(user_id=request.user.id)
            account.verified = True
            account.save()
            logout(request)
            return redirect('home')  # Replace 'success_page' with the URL of the success page.
        else:
            # Code is incorrect, display an error message, or redirect back to the verification page.
            messages.success(request, "Verification code entered is incorrect.")
            logout(request)
            return redirect('phone_verification')

    else:
        return redirect('verify_phone_number')


def resend_code(request):
    # Code to resend the verification code goes here.
    return redirect('verify_phone_number')


def change_number(request):
    # Code to allow the user to change their phone number goes here.
    return redirect('verify_phone_number')
