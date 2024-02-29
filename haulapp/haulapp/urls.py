from django.contrib import admin
from django.urls import path
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from haulistic.views import (
    IndexView,
    AddUserView,
    LoginView,
    LogoutView,
    EditUserView,
    UserListView,
    DashboardView,
    AllShoppingListsView,
    AddShoppingListView,
    AddShoppingListElementView,
    DetailShoppingListView,
    EditShoppingListView,
    DeleteShoppingListView,
    EditShoppingListElementView,
    AddToDefaultShoppingListElementView,
    AllToDoListsView,
    AddToDoListView,
    EditToDoListView,
    DeleteToDoListView,
    AddToDoElementView,
    DetailToDoListView,
    AddDefaultToDoElementView,
    EditToDoListElementView
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),   # landing page
    path('accounts/add/', AddUserView.as_view(), name='add-user'), 
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('accounts/edit/', login_required(EditUserView), name='edit-user'),
    path('accounts/show-all/', staff_member_required(UserListView.as_view()), name='show-all-users'), 
    path('dashboard/', login_required(DashboardView.as_view()), name='dashboard'),  # main app page
    path('list/shop/all/', login_required(AllShoppingListsView.as_view()), name='all-shopping-lists'),
    path('list/shop/add/', login_required(AddShoppingListView), name='shopping-list-add'),
    path('list/shop/<int:list_pk>/', login_required(DetailShoppingListView.as_view()), name='shopping-list-details'),
    path('list/shop/<int:list_pk>/edit/', login_required(EditShoppingListView), name='shopping-list-edit'),
    path('list/shop/<int:list_pk>/delete/', login_required(DeleteShoppingListView), name='shopping-list-delete'),
    path('list/shop/<int:list_pk>/add-item/', login_required(AddShoppingListElementView), name='add-item-to-shopping-list'),
    path('list/shop/<int:list_pk>/<int:element_pk>/', login_required(EditShoppingListElementView), name='edit-shopping-list-element'),
    path('list/shop/default/add-item/', login_required(AddToDefaultShoppingListElementView), name='add-item-to-default-shopping-list'),
    path('list/to-do/all/', login_required(AllToDoListsView.as_view()), name='all-to-do-lists'),
    path('list/to-do/add/', login_required(AddToDoListView), name='to-do-list-add'),
    path('list/to-do/<int:list_pk>/', login_required(DetailToDoListView.as_view()), name='to-do-list-details'),
    path('list/to-do/<int:list_pk>/edit/', login_required(EditToDoListView), name='to-do-list-edit'),
    path('list/to-do/<int:list_pk>/delete/', login_required(DeleteToDoListView), name='to-do-list-delete'),
    path('list/to-do/<int:list_pk>/add-item/', login_required(AddToDoElementView), name='add-item-to-to-do-list'),
    path('list/to-do/<int:list_pk>/<int:element_pk>/', login_required(EditToDoListElementView), name='edit-to-do-list-element'),
    path('list/to-do/default/add-item/', login_required(AddDefaultToDoElementView), name='add-item-to-default-to-do-list'),
]

