from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.shortcuts import redirect
from django.utils.decorators import method_decorator

from apps.commons.utils import get_base_url
from .pagination import CustomPagination

from apps.core.models import Job, JobApplication, Category
from .forms import ContactForm

# Create your views here.
class HomeView(ListView):
    template_name = "core/home.html"
    pagination_class = CustomPagination

    def get_pagination(self):
        return self.pagination_class()

    def get_queryset(self):
        category = self.request.GET.get('category')
        search = self.request.GET.get('search')
        job_filter = {"is_active": True}
        exclude = dict()
        if self.request.user.is_authenticated:
            exclude = {"job_applications__user": self.request.user}
        if category:
            job_filter.update(category__uuid=category)
        if search:
            job_filter.update(title__icontains=search)
        return Job.objects.filter(**job_filter).exclude(**exclude).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Home"
        pagination = self.get_pagination()
        qs = pagination.get_paginated_qs(view=self)
        paginated_qs = pagination.get_nested_pagination(qs, nested_size=2)
        context['job_lists'] = paginated_qs
        context['categories'] = Category.objects.all()
        page_number, page_str = pagination.get_current_page(view=self)
        context[page_str] = 'active'
        context["next_page"] = page_number + 1
        context["prev_page"] = page_number - 1
        context['base_url'] = get_base_url(request=self.request)
        if page_number >= pagination.get_last_page(view=self):
            context["next"] = "disabled"
        if page_number <= 1:
            context["prev"] = "disabled"
        context['home_active'] = 'active'
        return context

class ContactView(CreateView):
    template_name = 'core/contact.html'
    success_url = reverse_lazy('contact')
    form_class = ContactForm

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            messages.success(request, "We Have Received Your Response")
            return self.form_valid(form)
        else:
            messages.error(request, "Something Went Wrong")
            return self.form_invalid(form)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Contact Us"
        context['contact_active'] = 'active'
        return context