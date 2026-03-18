from django.urls import path
from .views import (
    MaintenanceListView, MaintenanceCreateView,
    MaintenanceUpdateView, MaintenanceDeleteView
)

urlpatterns = [
    path('', MaintenanceListView.as_view(), name='maintenance_list'),
    path('add/', MaintenanceCreateView.as_view(), name='maintenance_add'),
    path('<int:pk>/edit/', MaintenanceUpdateView.as_view(), name='maintenance_edit'),
    path('<int:pk>/delete/', MaintenanceDeleteView.as_view(), name='maintenance_delete'),
]
