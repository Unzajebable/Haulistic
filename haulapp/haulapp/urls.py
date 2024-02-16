"""
URL configuration for haulapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from haulistic.views import (
    IndexView,
    LoginView,
    AddUserView,
    UserListView,
    AllListsView,
    AddListView,
    AddListElementView,
    DetailListView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),   #landing page
    path('user/login/', LoginView.as_view(), name='login'),
    path('user/add/', AddUserView.as_view(), name='add-user'),
    path('user/show-all/', UserListView.as_view(), name='show-all-users'),
    path('list/all/', AllListsView.as_view(), name='all-lists'),
    path('list/add/', AddListView.as_view(), name='list-add'),
    path('list/<int:pk>/', DetailListView.as_view(), name='list-details'),
    path('list/<int:pk>/add-item/', AddListElementView.as_view(), name='add-item-to-list'),
    
    # dashboard aka main app page
    # add new shopping list
    # show all shopping lists
    # detailed view of selected shopping list
    # add an item to selected list
    # add an to default list
]

