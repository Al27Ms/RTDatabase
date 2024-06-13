from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('temples/', views.temple_list, name='temple_list'),
    path('temple/<int:temple_id>/', views.temple_detail, name='temple_detail'),
    path('map/', views.map_view, name='map'),
    path('info/', views.info_view, name='info')

]
