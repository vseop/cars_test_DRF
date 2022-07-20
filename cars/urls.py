from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('car/', views.CarViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('car/<int:pk>/', views.CarViewSet.as_view({'put': 'update', 'delete': 'destroy', 'get': 'retrieve'})),
    path('car/export/', views.CarViewSet.as_view({'get': 'export'})),
    path('car/import/', views.CarViewSet.as_view({'post': 'import_data'})),
    path('drf-auth/', include('rest_framework.urls')),
    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
