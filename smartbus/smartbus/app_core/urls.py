from django.urls import path
from app_core import views


app_name = "core"
urlpatterns = [
    path("district/", views.district, name = "dis"), # district registration
    path("disview/", views.disview, name = "disv"), # district view
    path("disdl/<int:name>", views.disdl, name = "ddlt"), # district delete
    path("disup/<int:name>", views.disup, name="dupt"), # district edit
    
    path("locations/", views.locations, name = "loc"),  # location registration
    path("locview/", views.locview, name = "locv"), # location view
    path("locdlt/<int:name>", views.locdlt, name = "ldlt"), # location delete
    path("locup/<int:name>", views.locup, name="lup"), # location edit
    
    path("cate/", views.cate, name="cat"),
    path("catev/", views.catev, name="catv"),
    path("catedl/<int:name>", views.catedl, name="catdl"),
    path("cateup/<int:name>", views.cateup, name="catup"),
    
    path('admin_booking_report/', views.seller_booking_pie_chart, name= 'admin_booking_report'),
]

