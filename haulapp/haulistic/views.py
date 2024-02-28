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
    EditUserForm,
    AddShoppingListForm,
    AddShoppingListElementForm,
    AddToDoListForm,
    AddToDoElementForm,
)


class IndexView(View):
    """
    Straight-forward landing page rendering for the application
    """
    def get(self, request, *args, **kwargs):
        template_name = "haulistic/index.html"
        context = {
            'now': datetime.now().year,
        }
        return render(request, template_name, context)


class AddUserView(CreateView):
    """
    New user creation using CreateView and AddUserForm that inherits from UserCreationForm (all authentication
    of passwords, usernames, emails etc. handled by Django middlewares) - basically, Django does the heavy lifting here
    if you provide needed resources based on the documentation
    """
    template_name = "haulistic/add_user.html"
    model = User
    form_class = AddUserForm
    extra_context = {'now': datetime.now().year}
    success_url = reverse_lazy("login")


def EditUserView(request): 
    """ 
    Simple user updating view - no password change is allowed
    """
    form = EditUserForm(instance=request.user)
    if request.method == "POST":
        form = EditUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, "Account " + username +" successfully modified!")
            return redirect('/dashboard/')
    context = {
        "form": form,
        'now': datetime.now().year,
    }
    return render(request, 'haulistic/edit_user.html', context)
        


class UserListView(ListView):
    """
    A basic listing of all created users for staff members that are not super-users
    """
    template_name = "haulistic/user_list.html"
    model = User
    extra_context = {'now': datetime.now().year}
    context_object_name = "users"


class LoginView(FormView):
    """
    Login view that logs you if provided with proper credentials
    """
    template_name = "haulistic/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("dashboard")
    extra_context = {'now': datetime.now().year}

    def form_valid(self, form):
        user = form.user
        login(self.request, user)
        return super().form_valid(form)
    

class LogoutView(RedirectView):
    """
    Logout view that logs out the user
    """
    url = reverse_lazy("index")

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class DashboardView(View):
    """
    Dashboard view that pulls the default lists created for every new account 
    and lists all the elements contained in those default lists
    """
    def get(self, request, *args, **kwargs): 
        messages.info(request, "Welcome " + self.request.user.username +"!")
        logged_user_id = self.request.user.id
        default_sh_list = Shopping_List.objects.all().filter(list_owner=logged_user_id)[0]
        default_td_list = To_Do_List.objects.all().filter(list_owner=logged_user_id)[0]
        sh_list_elements = List_Element.objects.all().filter(list_pk=default_sh_list.id)
        td_list_elements = To_Do_Element.objects.all().filter(list_pk=default_td_list.id)
        context = {
            "sh_list":default_sh_list,
            "sh_elements":sh_list_elements,
            "td_list":default_td_list,
            "td_elements":td_list_elements,
            'now': datetime.now().year,
        }
        return render(request, 'haulistic/dashboard.html', context)


class AllShoppingListsView(View):
    """
    Listing all shopping lists owned by the logged-in user
    """
    def get(self, request, *args, **kwargs):
        logged_user_id = self.request.user.id
        owned_lists = Shopping_List.objects.all().filter(list_owner=logged_user_id)
        messages.info(request, "Click on the name of the list to see details.")
        context = {
            'lists':owned_lists, 
            'now': datetime.now().year,
        }
        return render(request, 'haulistic/all_shopping_lists.html', context)


def AddShoppingListView(request, *args, **kwargs):
    """
    Creation of a new shopping list
    """
    logged_user = request.user
    form = AddShoppingListForm()
    
    if request.method == 'POST':
        form = AddShoppingListForm(request.POST)
        if form.is_valid():
            new_list = form.save(commit=False)
            new_list.list_owner = logged_user
            new_list.save()
            list_name_msg = form.cleaned_data.get('list_name')
            messages.success(request, 'Successfully added new list "' + list_name_msg +'"!')
            return redirect('/list/shop/all/')
    
    context = {
        'form': form,
        'now': datetime.now().year,
    }
    return render(request, 'haulistic/add_shopping_list.html', context)


class DetailShoppingListView(View):
    """
    A view that shows all elements contained in a given list (as the ID of the list is shown in the url
    there's a special if statement to check if the logged-in user is the owner of the selected list)
    """
    def get(self, request, *args, **kwargs):
        list_pk = kwargs['list_pk']
        chosen_list = get_object_or_404(Shopping_List, pk=list_pk)
        list_elements = List_Element.objects.all().filter(list_pk=list_pk)
        if request.user == chosen_list.list_owner:
            context = {
                "list":chosen_list,
                "elements":list_elements,
                'now': datetime.now().year,
            }
            return render(request, 'haulistic/shopping_list_details.html', context)
        else:
            return render(request, 'haulistic/no_access.html', {'now': datetime.now().year})


def EditShoppingListView(request, list_pk):
    """
    A view that lets the owner of the list modify the name or the category of the list (as the ID of the list
    is shown in the url there's a special if statement to check if the logged-in user is the owner of the selected list)
    """
    sh_list = Shopping_List.objects.get(id=list_pk)
    form = AddShoppingListForm(instance=sh_list)
    if request.user == sh_list.list_owner:
        if request.method == 'POST':
            form = AddShoppingListForm(request.POST, instance=sh_list)
            if form.is_valid():
                form.save()
                list_name_msg = form.cleaned_data.get('list_name')
                messages.success(request, 'Successfully modified list "' + list_name_msg +'"!')
                return redirect('/list/shop/all/')
        
        context = {
            'form': form,
            'now': datetime.now().year,
        }
        return render(request, 'haulistic/add_shopping_list.html', context)
    else:
        return render(request, 'haulistic/no_access.html', {'now': datetime.now().year})


def DeleteShoppingListView(request, list_pk):
    """
    A view that lets the owner of the list delete the list (as the ID of the list is shown in the url
    there's a special if statement to check if the logged-in user is the owner of the selected list)
    """
    sh_list = Shopping_List.objects.get(id=list_pk)
    logged_user_id = request.user.id
    default_sh_list = Shopping_List.objects.all().filter(list_owner=logged_user_id)[0]
    if request.user == sh_list.list_owner:
        if request.method == 'POST':
            if default_sh_list.pk == list_pk:
                context = {'now': datetime.now().year, 'list': default_sh_list}
                return render(request, 'haulistic/big_no_no.html', context)
            else:
                sh_list.delete()
                messages.success(request, "List deleted.")
                return redirect('/list/shop/all/')
        context = {
            'list': sh_list,
            'now': datetime.now().year,
        }
        return render(request, 'haulistic/delete.html', context)
    else:
        return render(request, 'haulistic/no_access.html', {'now': datetime.now().year})


def AddShoppingListElementView(request, *args, **kwargs):
    """
    A view that allows the user to add new positions to the list (as the ID of the list is shown in the url
    there's a special if statement to check if the logged-in user is the owner of the selected list)
    """
    active_list = Shopping_List.objects.get(pk=kwargs['list_pk'])
    form = AddShoppingListElementForm()
    # success = False
    if request.user == active_list.list_owner:
        if request.method == 'POST':
            form = AddShoppingListElementForm(request.POST)
            if form.is_valid():
                new_list = form.save(commit=False)
                new_list.list_pk = active_list
                new_list.save()
                element_name_msg = form.cleaned_data.get('element_name')
                messages.success(request, 'Successfully added new product "' + element_name_msg +'" to the list.')
                form = AddShoppingListElementForm()
                # success = True
        
        context = {
            'form': form,
            'now': datetime.now().year,
            'list': active_list,
        }
        return render(request, 'haulistic/add_shopping_list_element.html', context)
    else:
        return render(request, 'haulistic/no_access.html', {'now': datetime.now().year})
    

def AddToDefaultShoppingListElementView(request, *args, **kwargs):
    """
    This view was strictly needed for the quick-access side panel button 'add to default' to work, so the user
    can quickly add something to a default list without searching for the proper one
    """
    logged_user_id = request.user.id
    default_sh_list = Shopping_List.objects.all().filter(list_owner=logged_user_id)[0]
    form = AddShoppingListElementForm()
    # success = False
    
    if request.method == 'POST':
        form = AddShoppingListElementForm(request.POST)
        if form.is_valid():
            new_list = form.save(commit=False)
            new_list.list_pk = default_sh_list
            new_list.save()
            element_name_msg = form.cleaned_data.get('element_name')
            messages.success(request, 'Successfully added new product "' + element_name_msg +'" to the list.')
            form = AddShoppingListElementForm()
            # success = True
    
    context = {
        'form': form,
        'now': datetime.now().year,
        'list': default_sh_list,
    }
    return render(request, 'haulistic/add_shopping_list_element.html', context)


class AllToDoListsView(View):
    """
    Listing all To-Do lists owned by the logged-in user
    """
    def get(self, request, *args, **kwargs):
        logged_user_id = self.request.user.id
        owned_lists = To_Do_List.objects.all().filter(list_owner=logged_user_id)
        messages.info(request, "Click on the name of the list to see details.")
        context = {
            'lists':owned_lists, 
            'now': datetime.now().year,
        }
        return render(request, 'haulistic/all_to_do_lists.html', context)


def AddToDoListView(request, *args, **kwargs):
    """
    Creation of a new To-Do list
    """
    logged_user = request.user
    form = AddToDoListForm()
    
    if request.method == 'POST':
        form = AddToDoListForm(request.POST)
        if form.is_valid():
            new_list = form.save(commit=False)
            new_list.list_owner = logged_user
            new_list.save()
            list_name_msg = form.cleaned_data.get('list_name')
            messages.success(request, 'Successfully added new list "' + list_name_msg +'"!')
            return redirect('/list/to-do/all/')
    
    context = {
        'form': form,
        'now': datetime.now().year,
    }
    return render(request, 'haulistic/add_to_do_list.html', context)


class DetailToDoListView(View):
    """
    A view that shows all elements contained in a given list (as the ID of the list is shown in the url
    there's a special if statement to check if the logged-in user is the owner of the selected list)
    """
    def get(self, request, *args, **kwargs):
        list_pk = kwargs['list_pk']
        chosen_list = get_object_or_404(To_Do_List, pk=list_pk)
        list_elements = To_Do_Element.objects.all().filter(list_pk=list_pk)
        if request.user == chosen_list.list_owner:
            context = {
                "list":chosen_list,
                "elements":list_elements,
                'now': datetime.now().year,
            }
            return render(request, 'haulistic/to_do_list_details.html', context)
        else:
            return render(request, 'haulistic/no_access.html', {'now': datetime.now().year})


def EditToDoListView(request, list_pk):
    """
    A view that lets the owner of the list modify the name or the category of the list (as the ID of the list
    is shown in the url there's a special if statement to check if the logged-in user is the owner of the selected list)
    """
    td_list = To_Do_List.objects.get(id=list_pk)
    form = AddToDoListForm(instance=td_list)
    if request.user == td_list.list_owner:
        if request.method == 'POST':
            form = AddToDoListForm(request.POST, instance=td_list)
            if form.is_valid():
                form.save()
                list_name_msg = form.cleaned_data.get('list_name')
                messages.success(request, 'Successfully modified list "' + list_name_msg +'"!')
                return redirect('/list/to-do/all/')
        
        context = {
            'form': form,
            'now': datetime.now().year,
        }
        return render(request, 'haulistic/add_to_do_list.html', context)
    else:
        return render(request, 'haulistic/no_access.html', {'now': datetime.now().year})


def DeleteToDoListView(request, list_pk):
    """
    A view that lets the owner of the list delete the list (as the ID of the list is shown in the url
    there's a special if statement to check if the logged-in user is the owner of the selected list)
    """
    logged_user_id = request.user.id
    default_td_list = To_Do_List.objects.all().filter(list_owner=logged_user_id)[0]
    td_list = To_Do_List.objects.get(id=list_pk)
    if request.user == td_list.list_owner:
        if request.method == 'POST':
            if default_td_list.pk == list_pk:
                context = {'now': datetime.now().year, 'list': default_td_list}
                return render(request, 'haulistic/big_no_no.html', context)
            else:
                td_list.delete()
                messages.success(request, "List deleted.")
                return redirect('/list/to-do/all/')
        context = {
            'list': td_list,
            'now': datetime.now().year,
        }
        return render(request, 'haulistic/delete.html', context)
    else:
        return render(request, 'haulistic/no_access.html', {'now': datetime.now().year})


def AddToDoElementView(request, *args, **kwargs):
    """
    A view that allows the user to add new positions to the list (as the ID of the list is shown in the url
    there's a special if statement to check if the logged-in user is the owner of the selected list)
    """
    active_list = To_Do_List.objects.get(pk=kwargs['list_pk'])
    form = AddToDoElementForm()
    # success = False
    if request.user == active_list.list_owner:
        if request.method == 'POST':
            form = AddToDoElementForm(request.POST)
            if form.is_valid():
                new_list = form.save(commit=False)
                new_list.list_pk = active_list
                new_list.save()
                element_name_msg = form.cleaned_data.get('element_name')
                messages.success(request, 'Successfully added new task "' + element_name_msg + '" to the list.')
                form = AddToDoElementForm()
                # success = True
        
        context = {
            'form': form,
            'now': datetime.now().year,
            'list': active_list,
        }
        return render(request, 'haulistic/add_to_do_list_element.html', context)
    else:
        return render(request, 'haulistic/no_access.html', {'now': datetime.now().year})


def AddDefaultToDoElementView(request, *args, **kwargs):
    """
    This view was strictly needed for the quick-access side panel button 'add to default' to work, so the user
    can quickly add something to a default list without searching for the proper one
    """
    logged_user_id = request.user.id
    default_td_list = To_Do_List.objects.all().filter(list_owner=logged_user_id)[0]
    form = AddToDoElementForm()
    # success = False
    
    if request.method == 'POST':
        form = AddToDoElementForm(request.POST)
        if form.is_valid():
            new_list = form.save(commit=False)
            new_list.list_pk = default_td_list
            new_list.save()
            element_name_msg = form.cleaned_data.get('element_name')
            messages.success(request, 'Successfully added new task "' + element_name_msg + '" to the list.')
            form = AddToDoElementForm()
            # success = True
    
    context = {
        'form': form,
        'now': datetime.now().year,
        'list': default_td_list,
    }
    return render(request, 'haulistic/add_to_do_list_element.html', context)

