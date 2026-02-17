from django.http import HttpResponse
from django.shortcuts import render
from app_core.models import Category, District, Location

#--------------------------------------------------District--------------------------------------------------
def district(request):
    if request.method=="POST":
        name = request.POST.get('named')
        if District.objects.filter(name =name).exists():
            return HttpResponse("<script>alert('Already Exist');window.location='';</script>")
        dis=District()
        dis.name=name
        dis.save()
        return HttpResponse("<script>alert('Inserted Successfully');window.location='';</script>")
    else:
        return render(request, "district.html")
    
def disview(request):
    view = District.objects.all()
    return render(request,"districtview.html",{"disv":view})

def disdl(request,name):
    d = District.objects.get(id=name)
    d.delete()
    return HttpResponse("<script>alert('Delete Successfully');window.location='/core/disview/';</script>")

def disup(request,name):
    up = District.objects.get(id=name)
    if request.method=="POST":
        name = request.POST.get('named')
        if District.objects.filter(name =name).exists():
            return HttpResponse("<script>alert('Already Exist');window.location='';</script>")
        up.name=name
        up.save()
        return HttpResponse("<script>alert('Updated Successfully');window.location='/core/disview/';</script>")
    return render(request,"districtedit.html",{"disv":up})
    
#--------------------------------------------------Location--------------------------------------------------
def locations(request):
    if request.method=="POST":
        loc = request.POST.get('namel')
        dis = request.POST.get('named')
        if Location.objects.filter( loc=loc, dis=dis ).exists():
            return HttpResponse("<script>alert('Already Exist');window.location='';</script>")
        l = Location()
        l.loc = loc
        l.dis = District.objects.get(id = dis)
        l.save()
        return HttpResponse("<script>alert('Inserted Successfully');window.location='/core/locations/';</script>")
    else:
        v = District.objects.all()
        return render(request, "location.html", {"list":v})
    
def locview(request):
    view = Location.objects.all()
    return render(request,"locationview.html",{"locv":view})

def locdlt(request,name):
    d = Location.objects.get(id=name)
    d.delete()
    return HttpResponse("<script>alert('Delete Successfully');window.location='/core/locview/';</script>")

def locup(request,name):
    up = Location.objects.get(id=name)
    if request.method=="POST":
        loc = request.POST.get('namel')
        dis = request.POST.get('named')
        if Location.objects.filter( loc=loc, dis=dis ).exists():
            return HttpResponse("<script>alert('Already Exist');window.location='';</script>")
        up.loc = loc
        up.dis = Location.objects.get(id = dis)
        up.save()
        return HttpResponse("<script>alert('Updated Successfully');window.location='/core/locview/';</script>")
    list=District.objects.all()
    return render(request,"locationedit.html",{"locv":up,"list":list})

#--------------------------------------------------Category--------------------------------------------------
def cate(request):
    if request.method=="POST":
        name = request.POST.get('name')
        dis = request.POST.get('description')
        if Category.objects.filter(name=name).exists():
            return HttpResponse("<script>alert('Already Exist');window.location='';</script>")
        c=Category()
        c.name=name
        c.description=dis
        if len(request.FILES) !=0:
            img = request.FILES['img']
        else:
            img = 'Images/default.jpg'
        c.img=img
        c.save()
        return HttpResponse("<script>alert('Inserted Successfully');window.location='';</script>")
    else:
        return render(request, "category.html")
    
def catev(request):
    view = Category.objects.all()
    return render(request,"categoryview.html",{"catv":view})

def catedl(request,name):
    d =Category.objects.get(id =name)
    d.delete()
    return HttpResponse("<script>alert('Delete Successfully');window.location='/core/catev/';</script>")

def cateup(request,name):
    up = Category.objects.get(id=name)
    if request.method=="POST":
        cname = request.POST.get('name')
        dis = request.POST.get('description')
        img =request.FILES.get('img')
        if Category.objects.filter(name=cname).exclude(id=name).exists():
            return HttpResponse("<script>alert('Already Exist');window.location='';</script>")
        up.name=name
        up.description=dis
        if img:
            up.img=img
        up.save()
        return HttpResponse("<script>alert('Updated Successfully');window.location='/core/catev/';</script>")
    return render(request,"categoryedit.html",{"catv":up})



def seller_booking_pie_chart(request): 
    seller_data = (BookingDetails.objects.values('material__seller__seller_name') 
                   .annotate(booking_count=Count('booking_master', distinct=True)) 
                   .order_by('-booking_count')) 
    labels = [item['material__seller__seller_name'] 
    for item in seller_data if item['material__seller__seller_name']] 
    data = [item['booking_count'] 
            for item in seller_data if 
            item['material__seller__seller_name']] 
    context = { 'labels': labels, 
               'data': data, 
               } 
    return render(request, 'Admin/booking_report.html', context)