from django.shortcuts import render,redirect,get_object_or_404
from .forms import RegistrationForm, UserForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from .models import Account, UserProfile

from django.contrib import messages,auth
# Create your views here.
def home(request):
     if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name    =form.cleaned_data['first_name']
            last_name     =form.cleaned_data['last_name']
            email         =form.cleaned_data['email']
            phone_number  =form.cleaned_data['phone_number']
            password      =form.cleaned_data['password']
            username      =form.cleaned_data['username']
            address      =form.cleaned_data['address']


            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number= phone_number
            user.address= address
            user.is_active = True
            user.save()

            # Create a user profile
            profile = UserProfile()
            profile.user_id = user.id
            profile.profile_picture = 'default/default_user.png'
            profile.save()

            messages.success(request, 'You are now Registered')
            return redirect('login')
     else:
         form = RegistrationForm()
         context = {
            'form': form,
         }
     return render(request, 'index.html', context)

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)


        if user is not None:
            auth.login(request,user)


            messages.success(request, 'you are now logged in')
            return redirect('edit_profile')
        else:
            messages.error(request, 'invalid credentials')
            return redirect('login')
    return render(request, 'login.html')


@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out ')
    return redirect('login')




@login_required(login_url='login')
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile,
    }
    return render(request, 'edit_profile.html', context)
