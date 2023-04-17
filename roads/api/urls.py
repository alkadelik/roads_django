from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.load_segments),
    path('roads/<int:pk>', views.roads_detail),
    path('road_status/', views.road_status),
    path('add_bulk_segments/', views.bulk_segments_upload),
    path('update_address/', views.update_address),
    path('update_segment_codes/', views.bulk_segments_upload),
    path('update_coordinates/', views.bulk_segments_upload),
    path('update_status/', views.bulk_segments_upload),
]
