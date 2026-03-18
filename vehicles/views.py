from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Sum, Count, Max
from django.utils import timezone
from datetime import timedelta
import json

from .models import Vehicle
from .forms import VehicleForm
from maintenance.models import MaintenanceRecord

class VehicleListView(LoginRequiredMixin, ListView):
    model = Vehicle
    template_name = 'vehicles/vehicle_list.html'
    context_object_name = 'vehicles'

    def get_queryset(self):
        return Vehicle.objects.filter(user=self.request.user)

class VehicleCreateView(LoginRequiredMixin, CreateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = 'vehicles/vehicle_form.html'
    success_url = reverse_lazy('vehicle_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class VehicleUpdateView(LoginRequiredMixin, UpdateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = 'vehicles/vehicle_form.html'
    success_url = reverse_lazy('vehicle_list')

    def get_queryset(self):
        return Vehicle.objects.filter(user=self.request.user)

class VehicleDeleteView(LoginRequiredMixin, DeleteView):
    model = Vehicle
    template_name = 'vehicles/vehicle_confirm_delete.html'
    success_url = reverse_lazy('vehicle_list')

    def get_queryset(self):
        return Vehicle.objects.filter(user=self.request.user)

class DashboardView(LoginRequiredMixin, ListView):
    model = Vehicle
    template_name = 'dashboard.html'
    context_object_name = 'vehicles'

    def get_queryset(self):
        return Vehicle.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_vehicles = self.get_queryset()
        
        # Summary Stats
        context['total_vehicles'] = user_vehicles.count()
        
        maintenance_records = MaintenanceRecord.objects.filter(vehicle__user=self.request.user)
        context['total_cost'] = maintenance_records.aggregate(Sum('cost'))['cost__sum'] or 0
        
        today = timezone.now().date()
        upcoming_reminders = maintenance_records.filter(next_service_date__gte=today).order_by('next_service_date')
        context['upcoming_reminders'] = upcoming_reminders
        context['upcoming_count'] = upcoming_reminders.count()
        
        # Overdue alerts
        context['overdue_count'] = maintenance_records.filter(next_service_date__lt=today).count()
        
        # Recent activity
        context['recent_logs'] = maintenance_records.order_by('-date')[:5]
        
        # Health Scores (Simplified logic)
        vehicle_health = []
        for v in user_vehicles:
            last_service = maintenance_records.filter(vehicle=v).aggregate(Max('date'))['date__max']
            if last_service:
                days_since = (today - last_service).days
                # 100% if < 180 days, linearly decrease to 0% at 730 days (2 years)
                # (days_since - 180) / (730 - 180) * 100
                score = max(0, min(100, 100 - (max(0, days_since - 180) / 5.5)))
            else:
                score = 0
            vehicle_health.append({'name': v.name, 'score': int(score)})
        context['vehicle_health'] = vehicle_health
        context['today'] = today
        
        return context

class AnalyticsView(LoginRequiredMixin, TemplateView):
    template_name = 'analytics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_vehicles = Vehicle.objects.filter(user=self.request.user)
        maintenance_records = MaintenanceRecord.objects.filter(vehicle__user=self.request.user).order_by('date')
        
        # Summary Stats
        total_cost = maintenance_records.aggregate(Sum('cost'))['cost__sum'] or 0
        total_vehicles = user_vehicles.count()
        average_cost = total_cost / maintenance_records.count() if maintenance_records.count() > 0 else 0
        
        context['total_cost'] = total_cost
        context['total_vehicles'] = total_vehicles
        context['average_cost'] = average_cost
        
        # Cost by Service Type
        cost_by_type = maintenance_records.values('service_type').annotate(total=Sum('cost'))
        type_labels = [dict(MaintenanceRecord.SERVICE_CHOICES).get(item['service_type']) for item in cost_by_type]
        type_data = [float(item['total']) for item in cost_by_type]
        
        context['type_labels'] = type_labels
        context['type_data'] = type_data
        
        # Monthly Cost Trend
        monthly_costs = {}
        for record in maintenance_records:
            month_str = record.date.strftime('%b %Y') # e.g. "Mar 2026"
            monthly_costs[month_str] = monthly_costs.get(month_str, 0) + float(record.cost)
        
        # Keep insertion order from historical records, then take last 6
        trend_labels = list(monthly_costs.keys())[-6:]
        trend_data = [monthly_costs[label] for label in trend_labels]
        
        context['trend_labels'] = trend_labels
        context['trend_data'] = trend_data
        
        return context

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'
