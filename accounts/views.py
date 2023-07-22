from django.shortcuts import render
from wsgiref import validate
from django.shortcuts import render,redirect
from django.contrib import messages
# from admins.mixins import MessageHandler
from django.contrib.auth.models import User,auth
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from .models import user_details
from . import verify

# Create your views here.
def signup(request):
    # if request.user.is_authenticated:
    #    return redirect(signup)
    if request.method=='POST':
    
       first_name=request.POST['first_name']
    #    last_name=request.POST['last_name']
       email=request.POST['email']
       phone_number=request.POST['phone_number']
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
                user=user_details.objects.create(first_name=first_name,email=email,phone_number=phone_number)
                user.set_password(password)
                # user.save()
                verify.send(user.phone_number)
                return render(request,'auth/otp.html')
            #     print('hii')
            #     otp=1
            #     message_handler=MessageHandler(phone_number,otp).sent_otp_on_phone()
            #     context = {'first_name':first_name,'email':email,'phone_number':phone_number,'password':password}
            #     return render(request,'otpsignincheck.html',context)
       else:
                    messages.info(request,'!! The password is not matching !!')
                    return redirect(signup)
    else:
        # return render(request,'auth/signup.html')
        return render(request,'auth/signup.html')
    
    # return render(request,'auth/signup.html')

def otp_verify(request):
    if request.method == 'POST':
            otp=request.POST['otp']    
            if verify.check(request.user.phone_number, otp):
                # request.user.is_verified = True
                request.user.save()
                return redirect('index')
    else:
        return render(request,'auth/otp.html')
    
   