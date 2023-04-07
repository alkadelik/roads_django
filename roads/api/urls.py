from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.roads_list),
    path('list_routes/', views.routes_list),
    path('roads/<int:pk>', views.roads_detail),
    path('road_status/', views.road_status),
    path('bulk_segments/', views.bulk_segments_upload),
]
