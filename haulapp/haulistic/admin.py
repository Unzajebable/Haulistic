from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Shopping_List, List_Element, To_Do_List, To_Do_Element

admin.site.register(User, UserAdmin)
admin.site.register(Shopping_List)
admin.site.register(List_Element)
admin.site.register(To_Do_List)
admin.site.register(To_Do_Element)
