from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.load_segments),
    path('roads/<int:pk>', views.roads_detail),
    path('road_status/', views.road_status),
    path('add_bulk_segments/', views.bulk_segments_upload),
    path('update_address/', views.update_address),
    path('update_code/', views.update_code),
    path('update_coordinates/', views.update_coordinates),
    path('update_status/', views.bulk_segments_upload),
    path('update_state/', views.update_state),
    path('update_name/', views.update_name),
    path('update_motorability/', views.update_motorability),
]
