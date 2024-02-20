from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.views.generic import CreateView, FormView, ListView, RedirectView, DetailView
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model, login, logout
from datetime import datetime
from django.contrib import messages

from .models import List_Element, Shopping_List, To_Do_List, To_Do_Element
from .forms import (
    LoginForm,
    AddUserForm,
    AddShoppingListForm,
    AddShoppingListElementForm,
    AddToDoListForm,
    AddToDoElementForm,
)


User = get_user_model()


class IndexView(View):
    def get(self, request, *args, **kwargs):
        template_name = "haulistic/index.html"
        ctx = {
            'now': datetime.now().year,
            # 'pfpurl': 'https://ih1.redbubble.net/image.1213947686.0806/bg,f8f8f8-flat,750x,075,f-pad,750x1000,f8f8f8.jpg'
            'pfpurl': '/static/pfp_default.png'
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


class AllShoppingListsView(ListView):
    template_name = 'haulistic/all_shopping_lists.html'
    model = Shopping_List
    context_object_name = "lists"
    

class AddShoppingListView(FormView):
    template_name = 'haulistic/add_shopping_list.html'
    model = Shopping_List
    form_class = AddShoppingListForm
    success_url = reverse_lazy('all-shopping-lists')


class AddShoppingListElementView(FormView):
    template_name = 'haulistic/add_shopping_list_element.html'
    model = List_Element
    form_class = AddShoppingListElementForm
    
    def get_success_url(self):
        list_pk = self.kwargs['list_pk']
        return reverse('add-item-to-shopping-list', kwargs={'list_pk':list_pk})
    
    def form_valid(self, form):
        form.save()
        messages.info(self.request, "Added successfully")   #dunno why no workie
        return super().form_valid(form)
    
    def get_initial(self):
        initial_data = super().get_initial()
        list_pk = self.kwargs['list_pk']
        initial_data['list_pk'] = list_pk
        
        return initial_data


class DetailShoppingListView(DetailView):
    template_name = 'haulistic/shopping_list_details.html'
    model = List_Element
    pk_url_kwarg = 'list_pk'
    context_object_name = "item"
    """wizualnie zamienić id listy z tablicy elementów na nazwę listy która jest w tabelce list;
    mam wrażenie że łatwiej bedzie to napisać funkcją i w zapytaniu do bazy wyciągnąć nazwę i 
    kategorię listy zakupowej a potem wszystkie elementy z id listy z której wyciągnięta została nazwa
    i przekazać to poprzez context
    https://stackoverflow.com/questions/72463459/django-get-objects-from-one-table-who-belong-to-another-objects-in-other-table
    https://forum.djangoproject.com/t/django-orm-inner-join-query-on-2-tables-that-share-same-fk-to-user-model/21019/4
    https://forum.djangoproject.com/t/how-do-i-load-multiple-models-items-into-a-single-view/919
    select_related()?
    """


class AddToDoListView(FormView):
    template_name = 'haulistic/add_to_do_list.html'
    model = To_Do_List
    form_class = AddToDoListForm
    success_url = reverse_lazy('all-to-do-lists')


class AllToDoListsView(ListView):
    template_name = 'haulistic/all_to_do_lists.html'
    model = To_Do_List
    context_object_name = "lists"


class AddToDoElementView(FormView):
    template_name = 'haulistic/add_to_do_list_element.html'
    model = To_Do_Element
    form_class = AddToDoElementForm
    
    def get_success_url(self):
        list_pk = self.kwargs['list_pk']
        return reverse('add-item-to-to-do-list', kwargs={'list_pk':list_pk})
    
    def form_valid(self, form):
        form.save()
        messages.info(self.request, "Added successfully")   #dunno why no workie
        return super().form_valid(form)
    
    def get_initial(self):
        initial_data = super().get_initial()
        list_pk = self.kwargs['list_pk']
        initial_data['list_pk'] = list_pk
        
        return initial_data





