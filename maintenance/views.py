from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import MaintenanceRecord
from .forms import MaintenanceRecordForm
from vehicles.models import Vehicle

class MaintenanceListView(LoginRequiredMixin, ListView):
    model = MaintenanceRecord
    template_name = 'maintenance/maintenance_list.html'
    context_object_name = 'logs'

    def get_queryset(self):
        return MaintenanceRecord.objects.filter(vehicle__user=self.request.user)

class MaintenanceCreateView(LoginRequiredMixin, CreateView):
    model = MaintenanceRecord
    form_class = MaintenanceRecordForm
    template_name = 'maintenance/maintenance_form.html'
    success_url = reverse_lazy('maintenance_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        vehicle_id = self.request.GET.get('vehicle')
        if vehicle_id:
            initial['vehicle'] = get_object_or_404(Vehicle, pk=vehicle_id, user=self.request.user)
        return initial

class MaintenanceUpdateView(LoginRequiredMixin, UpdateView):
    model = MaintenanceRecord
    form_class = MaintenanceRecordForm
    template_name = 'maintenance/maintenance_form.html'
    success_url = reverse_lazy('maintenance_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_queryset(self):
        return MaintenanceRecord.objects.filter(vehicle__user=self.request.user)

class MaintenanceDeleteView(LoginRequiredMixin, DeleteView):
    model = MaintenanceRecord
    template_name = 'maintenance/maintenance_confirm_delete.html'
    success_url = reverse_lazy('maintenance_list')

    def get_queryset(self):
        return MaintenanceRecord.objects.filter(vehicle__user=self.request.user)
