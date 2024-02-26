from django.contrib import admin
from django.urls import path
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from haulistic.views import (
    IndexView,
    LoginView,
    LogoutView,
    AddUserView,
    UserListView,
    DashboardView,
    AllShoppingListsView,
    AddShoppingListView,
    AddShoppingListElementView,
    DetailShoppingListView,
    AddToDefaultShoppingListElementView,
    AllToDoListsView,
    AddToDoListView,
    AddToDoElementView,
    DetailToDoListView,
    AddDefaultToDoElementView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),   #landing page
    path('accounts/add/', AddUserView.as_view(), name='add-user'), 
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    # path('accounts/edit/', EditUserView.as_view(), name='edit-user'),  #do zrobienie
    path('accounts/show-all/', staff_member_required(UserListView.as_view()), name='show-all-users'), 
    path('dashboard/', login_required(DashboardView.as_view()), name='dashboard'),  # od dashboarda w dół tylko dla zalogowanych
    path('list/shop/all/', login_required(AllShoppingListsView.as_view()), name='all-shopping-lists'),
    path('list/shop/add/', login_required(AddShoppingListView), name='shopping-list-add'),
    path('list/shop/<int:list_pk>/', login_required(DetailShoppingListView.as_view()), name='shopping-list-details'),
    path('list/shop/<int:list_pk>/add-item/', login_required(AddShoppingListElementView), name='add-item-to-shopping-list'),
    path('list/shop/default/add-item/', login_required(AddToDefaultShoppingListElementView), name='add-item-to-default-shopping-list'),  #do zrobienie
    path('list/to-do/all/', login_required(AllToDoListsView.as_view()), name='all-to-do-lists'),
    path('list/to-do/add/', login_required(AddToDoListView), name='to-do-list-add'),
    path('list/to-do/<int:list_pk>/', login_required(DetailToDoListView.as_view()), name='to-do-list-details'),
    path('list/to-do/<int:list_pk>/add-item/', login_required(AddToDoElementView), name='add-item-to-to-do-list'),
    path('list/to-do/default/add-item/', login_required(AddDefaultToDoElementView), name='add-item-to-default-to-do-list'),  #do zrobienie
]

