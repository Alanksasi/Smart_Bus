from django.urls import path
from app_dashboard import views

app_name="dashboard"
urlpatterns = [
    path("admins/", views.admins, name="admins"), #admin
    path("admv/", views.admv, name="admv"), #admin view
    path("optr/", views.optr, name="optr"), #operator
    path("", views.guest, name="guest"),
    path("logins/", views.logins, name="login"), #login
    path("reg/", views.reg, name="reg"), # operator registration busv
    path("dlt/<int:name>", views.dlt, name="dlt"),
    path("regi/", views.regi, name="regi"), #passenger registration
    path("psg/", views.psg, name="psg"),
]