from django.contrib import admin
from django.urls import path
from haulistic.views import (
    IndexView,
    LoginView,
    LogoutView,
    AddUserView,
    UserListView,
    AllShoppingListsView,
    AddShoppingListElementView,
    AddShoppingListView,
    DetailShoppingListView,
    AddToDoListView,
    AddToDoElementView,
    AllToDoListsView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),   #landing page
    path('user/add/', AddUserView.as_view(), name='add-user'),
    path('user/login/', LoginView.as_view(), name='login'),
    path('user/logout/', LogoutView.as_view(), name='logout'),
    # path('user/edit/', EditUserView.as_view(), name='edit-user'),  #do zrobienie
    path('user/show-all/', UserListView.as_view(), name='show-all-users'),
    path('list/shop/all/', AllShoppingListsView.as_view(), name='all-shopping-lists'),
    path('list/shop/add/', AddShoppingListView.as_view(), name='shopping-list-add'),
    path('list/shop/<int:list_pk>/', DetailShoppingListView.as_view(), name='shopping-list-details'),
    path('list/shop/<int:list_pk>/add-item/', AddShoppingListElementView.as_view(), name='add-item-to-shopping-list'),
    # path('list/shop/<int:list_pk>/add-item/', AddToDefaultShoppingListElementView.as_view(), name='add-item-to-default-shopping-list'),  #do zrobienie
    path('list/to-do/all/', AllToDoListsView.as_view(), name='all-to-do-lists'),
    path('list/to-do/add/', AddToDoListView.as_view(), name='to-do-list-add'),
    # path('list/to-do/<int:list_pk>/', DetailToDoListView.as_view(), name='to-do-list-details'),  #do zrobienie
    path('list/to-do/<int:list_pk>/add-item/', AddToDoElementView.as_view(), name='add-item-to-to-do-list'),
    # path('list/to-do/<int:list_pk>/add-item/', AddDefaultToDoElementView.as_view(), name='add-item-to-default-to-do-list'),  #do zrobienie
    
    # dashboard aka main app page pokazujący obie default listy
]

