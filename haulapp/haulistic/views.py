from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.views.generic import CreateView, FormView, ListView, RedirectView, DetailView
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model, login, logout
from datetime import datetime
from django.contrib import messages

from .models import List_Element, Shopping_List
from .forms import (
    LoginForm,
    AddUserForm,
    AddListForm,
    AddListElementForm,
)


User = get_user_model()


class IndexView(View):
    def get(self, request, *args, **kwargs):
        template_name = "haulistic/index.html"
        ctx = {
            'now': datetime.now().year,
        }
        return render(request, template_name, ctx)


class UserListView(ListView): #trzeba będzie ustawić dostęp tylko dla super usera
    template_name = "haulistic/user_list.html"
    model = User
    context_object_name = "users"


class LoginView(FormView):  #potęcjalnie zmienię na (LoginView)
    template_name = "haulistic/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        user = form.user
        login(self.request, user)
        return super().form_valid(form)


class LogoutView(RedirectView): #potęcjalnie zmienię na (LogoutView)
    url = reverse_lazy("login")

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class AddUserView(CreateView):
    template_name = "haulistic/add_user.html"
    model = User
    form_class = AddUserForm
    success_url = reverse_lazy("login")


class AllListsView(ListView):
    template_name = 'haulistic/all_lists_view.html'
    model = Shopping_List
    context_object_name = "lists"
    

class AddListView(FormView):
    template_name = 'haulistic/add_list.html'
    model = Shopping_List
    form_class = AddListForm
    success_url = reverse_lazy('all-lists')


class AddListElementView(FormView):
    template_name = 'haulistic/add_list_element.html'
    model = List_Element
    form_class = AddListElementForm
    
    def get_success_url(self):
        list_pk = self.kwargs['pk']
        return reverse('add-item-to-list', kwargs={'pk':list_pk})
    
    def form_valid(self, form):
        form.save()
        messages.info(self.request, "Added successfully")   #dunno why no workie
        return super().form_valid(form)
    
    def get_initial(self):
        initial_data = super().get_initial()
        list_pk = self.kwargs['pk']
        initial_data['list_pk'] = list_pk
        
        return initial_data


class DetailListView(DetailView):
    template_name = 'haulistic/detail_list_view.html'
    model = List_Element
    context_object_name = "items"
    # wizualnie zamienić id listy z tablicy elementów na nazwę listy która jest w tabelce list
