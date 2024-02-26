from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import CreateView, FormView, ListView, RedirectView
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from datetime import datetime
from django.contrib import messages

from .models import User, List_Element, Shopping_List, To_Do_List, To_Do_Element
from .forms import (
    LoginForm,
    AddUserForm,
    AddShoppingListForm,
    AddShoppingListElementForm,
    AddToDoListForm,
    AddToDoElementForm,
)


class IndexView(View):
    def get(self, request, *args, **kwargs):
        template_name = "haulistic/index.html"
        ctx = {
            'now': datetime.now().year,
        }
        return render(request, template_name, ctx)


class AddUserView(CreateView):
    template_name = "haulistic/add_user.html"
    model = User
    form_class = AddUserForm
    success_url = reverse_lazy("login")


class UserListView(ListView):
    template_name = "haulistic/user_list.html"
    model = User
    context_object_name = "users"


class LoginView(FormView):
    template_name = "haulistic/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        user = form.user
        login(self.request, user)
        return super().form_valid(form)
    

class LogoutView(RedirectView):
    url = reverse_lazy("index")

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class DashboardView(View):
    def get(self, request, *args, **kwargs): 
        logged_user_id = self.request.user.id
        default_sh_list = Shopping_List.objects.all().filter(list_owner=logged_user_id)[:1]
        default_td_list = To_Do_List.objects.all().filter(list_owner=logged_user_id)[:1]
        sh_list_elements = List_Element.objects.all().filter(list_pk=default_sh_list[0].id)
        td_list_elements = To_Do_Element.objects.all().filter(list_pk=default_td_list[0].id)
        context = {
            "sh_list":default_sh_list[0],
            "sh_elements":sh_list_elements,
            "td_list":default_td_list[0],
            "td_elements":td_list_elements,
            'now': datetime.now().year,
        }
        return render(request, 'haulistic/dashboard.html', context)


class AllShoppingListsView(View):
    def get(self, request, *args, **kwargs):
        logged_user_id = self.request.user.id
        owned_lists = Shopping_List.objects.all().filter(list_owner=logged_user_id)
        context = {'lists':owned_lists, 'now': datetime.now().year,}
        return render(request, 'haulistic/all_shopping_lists.html', context)


def AddShoppingListView(request, *args, **kwargs):
    logged_user = request.user
    form = AddShoppingListForm()
    
    if request.method == 'POST':
        form = AddShoppingListForm(request.POST)
        if form.is_valid():
            new_list = form.save(commit=False)
            new_list.list_owner = logged_user
            new_list.save()
            return redirect('/list/shop/all/')
    
    context = {
        'form': form,
        'now': datetime.now().year,
    }
    return render(request, 'haulistic/add_shopping_list.html', context)


def AddShoppingListElementView(request, *args, **kwargs):
    active_list = Shopping_List.objects.get(pk=kwargs['list_pk'])
    form = AddShoppingListElementForm()
    # success = False
    
    if request.method == 'POST':
        form = AddShoppingListElementForm(request.POST)
        if form.is_valid():
            new_list = form.save(commit=False)
            new_list.list_pk = active_list
            new_list.save()
            form = AddShoppingListElementForm()
            # success = True
    
    context = {
        'form': form,
        'now': datetime.now().year,
    }
    return render(request, 'haulistic/add_shopping_list_element.html', context)
    

def AddToDefaultShoppingListElementView(request, *args, **kwargs):
    logged_user_id = request.user.id
    default_sh_list = Shopping_List.objects.all().filter(list_owner=logged_user_id)[:1]
    form = AddShoppingListElementForm()
    # success = False
    
    if request.method == 'POST':
        form = AddShoppingListElementForm(request.POST)
        if form.is_valid():
            new_list = form.save(commit=False)
            new_list.list_pk = default_sh_list[0]
            new_list.save()
            form = AddShoppingListElementForm()
            # success = True
    
    context = {
        'form': form,
        'now': datetime.now().year,
    }
    return render(request, 'haulistic/add_shopping_list_element.html', context)


class DetailShoppingListView(View):
    def get(self, request, *args, **kwargs):
        list_pk = kwargs['list_pk']
        chosen_list = get_object_or_404(Shopping_List, pk=list_pk)
        list_elements = List_Element.objects.all().filter(list_pk=list_pk)
        context = {
            "list":chosen_list,
            "elements":list_elements,
        }
        return render(request, 'haulistic/shopping_list_details.html', context)


def AddToDoListView(request, *args, **kwargs):
    logged_user = request.user
    form = AddToDoListForm()
    
    if request.method == 'POST':
        form = AddToDoListForm(request.POST)
        if form.is_valid():
            new_list = form.save(commit=False)
            new_list.list_owner = logged_user
            new_list.save()
            return redirect('/list/to-do/all/')
    
    context = {
        'form': form,
        'now': datetime.now().year,
    }
    return render(request, 'haulistic/add_to_do_list.html', context)


class AllToDoListsView(View):
    def get(self, request, *args, **kwargs):
        logged_user_id = self.request.user.id
        owned_lists = To_Do_List.objects.all().filter(list_owner=logged_user_id)
        context = {'lists':owned_lists, 'now': datetime.now().year,}
        return render(request, 'haulistic/all_to_do_lists.html', context)


def AddToDoElementView(request, *args, **kwargs):
    active_list = To_Do_List.objects.get(pk=kwargs['list_pk'])
    form = AddToDoElementForm()
    # success = False
    
    if request.method == 'POST':
        form = AddToDoElementForm(request.POST)
        if form.is_valid():
            new_list = form.save(commit=False)
            new_list.list_pk = active_list
            new_list.save()
            form = AddToDoElementForm()
            # success = True
    
    context = {
        'form': form,
        'now': datetime.now().year,
    }
    return render(request, 'haulistic/add_to_do_list_element.html', context)


class DetailToDoListView(View):
    def get(self, request, *args, **kwargs):
        list_pk = kwargs['list_pk']
        chosen_list = get_object_or_404(To_Do_List, pk=list_pk)
        list_elements = To_Do_Element.objects.all().filter(list_pk=list_pk)
        context = {
            "list":chosen_list,
            "elements":list_elements,
        }
        return render(request, 'haulistic/to_do_list_details.html', context)


def AddDefaultToDoElementView(request, *args, **kwargs):
    logged_user_id = request.user.id
    default_td_list = To_Do_List.objects.all().filter(list_owner=logged_user_id)[:1]
    form = AddToDoElementForm()
    # success = False
    
    if request.method == 'POST':
        form = AddToDoElementForm(request.POST)
        if form.is_valid():
            new_list = form.save(commit=False)
            new_list.list_pk = default_td_list[0]
            new_list.save()
            form = AddToDoElementForm()
            # success = True
    
    context = {
        'form': form,
        'now': datetime.now().year,
    }
    return render(request, 'haulistic/add_to_do_list_element.html', context)

