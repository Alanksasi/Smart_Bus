from django.urls import path
from app_operator import views

app_name="operator"
urlpatterns = [
    path("busreg/", views.busreg, name="busreg"), #bus registration
    path("busv/", views.busv, name="busv"), #bus view
    path("busdl/<int:name>", views.busdl, name="busdl"), #bus delete
    path("busup/<int:name>", views.busup, name="busup"), #bus update
    
    path("route/", views.route, name="route"), #route registration
    path("routev/", views.routev, name="routev"), #route view
    path("routedl/<int:name>", views.routedl, name="routedl"), #route delete
    path("routeup/<int:name>", views.routeup, name="routeup"), #route update
    
    path("busroute/", views.busroute, name="busroute"), #busroute registration
    path("broutev/", views.broutev, name="broutev"), #busroute view
    path("broutedl/<int:name>", views.broutedl, name="broutedl"), #busroute delete
    path("brouteup/<int:name>", views.brouteup, name="brouteup"), #busroute update
    
    path("seats/<int:bus_id>/", views.seats, name="seats"),
    
    # NEW — operator creates trips
    path("add_trip/", views.add_trip, name="add_trip"),

    # # NEW — operator trip list
    # path("trip_view/", views.trip_view, name="trip_view"),

    # NEW — update live bus location
    path("updatelocation/<int:trip_id>/",
         views.updatelocation,
         name="updatelocation"),
]