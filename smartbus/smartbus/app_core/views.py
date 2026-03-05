from django.http import HttpResponse
from django.shortcuts import render
from app_core.models import District
from app_passenger.models import BookingMaster
import json

from django.db.models import Count

#--------------------------------------------------District--------------------------------------------------
# def district(request):
#     if request.method=="POST":
#         name = request.POST.get('named')
#         if District.objects.filter(name =name).exists():
#             return HttpResponse("<script>alert('Already Exist');window.location='';</script>")
#         dis=District()
#         dis.name=name
#         dis.save()
#         return HttpResponse("<script>alert('Inserted Successfully');window.location='';</script>")
#     else:
#         return render(request, "district.html")

def district(request):

    if request.method == "POST":
        name = request.POST.get('named')

        if District.objects.filter(name=name).exists():
            return HttpResponse(
                "<script>alert('District already exists');window.location='/core/district/';</script>"
            )

        District.objects.create(name=name)

        return HttpResponse(
            "<script>alert('District inserted successfully');window.location='/core/district/';</script>"
        )

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


#--------------------------------------------------Category--------------------------------------------------
# def cate(request):
#     if request.method=="POST":
#         name = request.POST.get('name')
#         dis = request.POST.get('description')
#         if Category.objects.filter(name=name).exists():
#             return HttpResponse("<script>alert('Already Exist');window.location='';</script>")
#         c=Category()
#         c.name=name
#         c.description=dis
#         if len(request.FILES) !=0:
#             img = request.FILES['img']
#         else:
#             img = 'Images/default.jpg'
#         c.img=img
#         c.save()
#         return HttpResponse("<script>alert('Inserted Successfully');window.location='';</script>")
#     else:
#         return render(request, "category.html")
    
# def catev(request):
#     view = Category.objects.all()
#     return render(request,"categoryview.html",{"catv":view})

# def catedl(request,name):
#     d =Category.objects.get(id =name)
#     d.delete()
#     return HttpResponse("<script>alert('Delete Successfully');window.location='/core/catev/';</script>")

# def cateup(request,name):
#     up = Category.objects.get(id=name)
#     if request.method=="POST":
#         cname = request.POST.get('name')
#         dis = request.POST.get('description')
#         img =request.FILES.get('img')
#         if Category.objects.filter(name=cname).exclude(id=name).exists():
#             return HttpResponse("<script>alert('Already Exist');window.location='';</script>")
#         up.name=name
#         up.description=dis
#         if img:
#             up.img=img
#         up.save()
#         return HttpResponse("<script>alert('Updated Successfully');window.location='/core/catev/';</script>")
#     return render(request,"categoryedit.html",{"catv":up})



def admin_booking_report(request):

    report = (
        BookingMaster.objects
        .values('trip__busroute__rid__name')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    labels = []
    data = []

    for r in report:
        labels.append(r['trip__busroute__rid__name'])
        data.append(r['total'])

    context = {
        "labels": json.dumps(labels),
        "data": json.dumps(data)
    }

    return render(request, "booking_report.html", context)