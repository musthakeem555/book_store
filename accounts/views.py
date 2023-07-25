from wsgiref import validate
from django.shortcuts import render,redirect
from django.contrib import messages
# from admins.mixins import MessageHandler
from django.contrib.auth.models import User,auth
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from .models import user_details
from . import verify
from django.contrib.auth import authenticate, login as auth_login

# Create your views here.
def signup(request):
    # if request.user.is_authenticated:
    #    return redirect(signup)
    if request.method=='POST':
    
       first_name=request.POST.get('first_name')
    #    last_name=request.POST['last_name']
       email=request.POST.get('email')
       phone_number=request.POST.get('phone_number')
       password=request.POST.get('password')
       password2=request.POST.get('password1')
       print('phone===',phone_number)
       from . import verify


       if password==password2:
            print('hiii')
            if not first_name.isalpha():
                messages.error(request,'Only letters are to be entered in name')
                
                print('1')
                return redirect(signup)
                
            elif len(phone_number)<10 or len(phone_number)>14:
                messages.error(request,'Mobile Or Phone number is wrong')
                print('2')

                return redirect(signup)
            elif user_details.objects.filter(email=email).exists() or user_details.objects.filter(phone_number=phone_number).exists():
                messages.error(request,'Already taken user')
                return redirect(signup)
            
            else:
                myuser=user_details.objects.create(first_name=first_name,email=email,phone_number=phone_number)
                myuser.set_password(password)
                myuser.save()
                verify.send(myuser.phone_number)
                return render(
                request,
                "auth/otp.html",
                {"id": myuser.id, "phone": myuser.phone_number},
            )
       else:
                    messages.info(request,'!! The password is not matching !!')
                    return redirect(signup)
    else:
        # return render(request,'auth/signup.html')
        return render(request,'auth/signup.html')
    
    # return render(request,'auth/signup.html')

def otp_verify(request,id,phone):
    if request.method == "POST":
        code = request.POST.get("otp")
        if verify.check(phone, code):
            user = user_details.objects.filter(id=id).update(is_verified=True)
            return redirect("home")
        else:
            user = user_details.objects.get(id=id)
            user.delete()
            return redirect("signup")
    else:
        return render(request,'auth/otp.html')
    

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            if user.is_active:
                auth_login(request, user)
                # Redirect to a success page or homepage after successful login
                return redirect('home')  # Replace 'home' with the name of your homepage URL pattern
            else:
                messages.error(request, 'Your account is not active.')
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'auth/login.html')

    # return render(request,'auth/login.html')
   