from django.contrib import messages
from django.contrib.auth.decorators import login_required
from app_passenger.models import BookingMaster

from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login, logout
from app_dashboard.models import Operator, Passenger  
from app_operator.models import Routes
from app_core.models import District
from smartbus.users.models import User
from django.core.mail import send_mail

# from django.contrib.auth.decorators import login_required
# from django.views.decorators.cache import never_cache
# from django.contrib.auth import logout

# Create your views here.
# def admins(request):
#     return render(request,"admindashboard.html")

@login_required(login_url='dashboard:login')
def admins(request):
    if request.user.role != "Admin":
        return redirect('dashboard:guest')
    return render(request, "admindashboard.html")

def guest(request):
    return render(request, "guestdashboard.html")

# @never_cache
# @login_required(login_url='/logins/')
# def logins(request):
#     if request.method=="POST":
#         name = request.POST.get('username')
#         pswd = request.POST.get('password')
#         user=authenticate(request,username=name,password=pswd)
#         if user is not None:
#             if user.role=="Admin":
#                 login(request,user)
#                 return HttpResponse("<script>alert('login successfull');window.location='/admins/';</script>")
#             elif user.role=="Bus operator":
#                 login(request,user)
#                 return HttpResponse("<script>alert('login successfull');window.location='/optr/';</script>")
#             elif user.role=="Passengers":
#                 login(request,user)
#                 return HttpResponse("<script>alert('login successfull');window.location='/psg/';</script>")
#         else:
#             return HttpResponse("<script>alert('invalid');window.location='/logins/';</script>")
#     # else:
#     return render(request, "login.html")


def logins(request):
    if request.method == "POST":
        name = request.POST.get('username')
        pswd = request.POST.get('password')

        user = authenticate(request, username=name, password=pswd)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful")

            if user.role == "Admin":
                return redirect('dashboard:admins')

            elif user.role == "Bus operator":
                return redirect('dashboard:optr')

            elif user.role == "Passengers":
                return redirect('dashboard:psg')

        else:
            messages.error(request, "Invalid username or password")
            return redirect('dashboard:login')

    return render(request, "login.html")
  
def reg(request):
    if request.method=="POST":
        name = request.POST.get('name')
        username = request.POST.get('username')
        pswd = request.POST.get('password')
        dis= request.POST.get('dis')
        mail = request.POST.get('email')
        con = request.POST.get('contact')        
        if not username or not pswd:
            return HttpResponse("<script>alert('Username and password are required');window.location='/dashboard/reg/';</script>")       
        if User.objects.filter(username=username).exists():
            return HttpResponse("<script>alert('Username already exists');window.location='/dashboard/reg/';</script>")
        user = User(username=username,name=name,email=mail)
        user.set_password(pswd)
        user.role="Bus operator"
        user.save()
        Operator.objects.create(user=user, contact=con,dis = District.objects.get(id = dis))
        return HttpResponse("<script>alert('Successfully Registration.');window.location='/optr/';</script>")
    else:
        v = District.objects.all()
        return render(request, "register.html", {"list":v})

# def optr(request):
#     return render(request, "operatordashboard.html")


@login_required(login_url='dashboard:login')
def optr(request):
    if request.user.role != "Bus operator":
        return redirect('dashboard:guest')
    return render(request, "operator_dashboard.html")

def admv(request):
    view = Operator.objects.all()
    return render(request,"view.html",{"admv":view})

def dlt(request,name):
    d = Operator.objects.get(id=name)
    d.delete()
    return HttpResponse("<script>alert('Delete Successfully');window.location='/admv/';</script>")

def regi(request):
    if request.method=="POST":
        name = request.POST.get('name')
        username = request.POST.get('username')
        pswd = request.POST.get('password')
        mail = request.POST.get('email')
        con = request.POST.get('contact')        
        if not username or not pswd:
            return HttpResponse("<script>alert('Username and password are required');window.location='/dashboard/regi/';</script>")       
        if User.objects.filter(username=username).exists():
            return HttpResponse("<script>alert('Username already exists');window.location='/dashboard/regi/';</script>")
        user = User(username=username,name=name,email=mail)
        user.set_password(pswd)
        user.role="Passengers"
        user.save()
        send_mail(
        subject="Welcome to Our Platform",
        message=f"Hi {name},\n\nYour account has been successfully created.",
        from_email=None,  
        recipient_list=[user.email],
    )
        # send_mail(subject="Registration Successfull", message=f"hi{name}, welcome to site", from_email="", recipient_list=[mail])
        Passenger.objects.create(user=user, contact=con)
        return HttpResponse("<script>alert('Successfully Registration.');window.location='/logins/';</script>")
    else:
        return render(request,"registerpass.html")

# def psg(request):
    # routev = Routes.objects.all()
    # return render(request, "guestdashboard.html",{"routev":routev})
    
def psg(request):
    bookings = BookingMaster.objects.filter(passenger__user=request.user).order_by('-booked_at')
    # order_by('-booking_date')[:5]
    return render(request, "dashboard.html", {
        "bookings": bookings
    })

# def logout_view(request):
#     logout(request)
#     return HttpResponse("<script>alert('Logged out successfully');window.location='/logins/';</script>")

def logout_view(request):
    logout(request)
    return redirect('dashboard:guest')