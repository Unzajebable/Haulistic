import pytest
from .models import User, List_Element, Shopping_List, To_Do_List, To_Do_Element
from datetime import datetime


"""
Passed instead of dots (we like those) and names of tests : pytest -v
with a report of what it's doing or sth : pytest -rP -v
Without the header (best one, use this) : pytest -v --no-header
"""

# Landing page test

@pytest.mark.django_db
def test_index_view(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.context['now'] == datetime.now().year

# Account interaction tests

@pytest.mark.django_db
def test_login_view(client, fake_user):
    response = client.post(
        "/accounts/login/",
        {
            'username': fake_user.username,
            'password': fake_user.password
        }
    )
    assert response.status_code == 200
    assert User.objects.get(username="fake_user") == fake_user


@pytest.mark.django_db
def test_logout_view(client, fake_user):
    client.force_login(fake_user)
    response1 = client.get("/accounts/logout/")
    assert response1.status_code == 302
    response2 = client.get("/dashboard/")
    assert response2.url == '/accounts/login/?next=/dashboard/'


@pytest.mark.django_db
def test_add_user_view(client):
    response = client.post(
        "/accounts/add/",
        {
            'username': 'fake_user',
            'password1': 'fakePass1`',
            'password2': 'fakePass1`',
            'email': 'fake@email.com',
            'pfpurl': 'fake_link'
        }
    )
    assert response.status_code == 302
    assert User.objects.get(username="fake_user")


@pytest.mark.django_db
def test_edit_user_view(client, fake_user):
    client.force_login(fake_user)   # mucho importante without this it will always redirect to login page with HTTP:200
    response = client.post(
        "/accounts/edit/",
        {
            'username': 'fake_user1',
            'email': 'fake@email.com',
            'pfpurl': 'fake_link_123'
        }
    )
    assert response.status_code == 302
    assert User.objects.get(username="fake_user1")


@pytest.mark.django_db
def test_user_list_view(client, fake_staff):
    client.force_login(fake_staff)
    response = client.get("/accounts/show-all/")
    assert response.status_code == 200
    assert response.context['users'][0].username == "fake_staff"
    assert response.context['users'][0].email == 'fake@staff.com'

# Dashboard test

@pytest.mark.django_db
def test_dashboard_view(client, fake_user):
    client.force_login(fake_user)
    response = client.get("/dashboard/")
    assert response.status_code == 200
    assert response.context['sh_list'].list_name == "Default Shopping List"
    assert response.context['td_list'].list_name == "Default To-Do List"

# Shopping Tests

@pytest.mark.django_db
def test_shopping_list_view(client, fake_user, fake_shopping_list):
    client.force_login(fake_user)
    response = client.get("/list/shop/all/")
    owner = User.objects.get(username="fake_user")
    assert response.status_code == 200
    assert response.context['lists'][0].list_name == "Default Shopping List"
    assert response.context['lists'][0].list_owner == owner
    assert response.context['lists'][1].list_name == "fake name1 shopping"


@pytest.mark.django_db
def test_add_shopping_list_view(client, fake_user):
    client.force_login(fake_user)   # mucho importante without this it will always redirect to login page with HTTP:200
    response = client.post(
        "/list/shop/add/",
        {
            "list_name": "fake name4 shopping",
            "list_category": "fake4 category1"
        }
    )
    assert response.status_code == 302
    assert Shopping_List.objects.get(list_name='fake name4 shopping')


@pytest.mark.django_db
def test_shopping_list_detail_view(client, fake_user, fake_shopping_list, fake_list_elements):
    client.force_login(fake_user)
    response = client.get(f"/list/shop/{fake_shopping_list.pk}/")
    assert response.context['list'].list_name == "fake name1 shopping"
    assert response.context['list'].list_category == "fake category1"
    assert response.context['elements'][0].element_name == 'nazwa3'
    assert response.context['elements'][0].bought == 0
    assert response.context['elements'][1].element_description == 'desc1'
    assert response.context['elements'][1].amount == 2
    assert response.status_code == 200


@pytest.mark.django_db
def test_edit_shopping_list_view(client, fake_user, fake_shopping_list2):
    client.force_login(fake_user)   # mucho importante without this it will always redirect to login page with HTTP:200
    response = client.post(
        f"/list/shop/{fake_shopping_list2.pk}/edit/",
        {
            'list_name' : "fake name10 shopping edited",
            'list_category' : "fake category10 edited",
        }
    )
    assert response.status_code == 302
    assert Shopping_List.objects.get(list_name='fake name10 shopping edited')
    assert Shopping_List.objects.get(list_category='fake category10 edited')


@pytest.mark.django_db
def test_delete_shopping_list_view(client, fake_user, fake_shopping_list2):
    client.force_login(fake_user)   # mucho importante without this it will always redirect to login page with HTTP:200
    response1 = client.post(f"/list/shop/{fake_shopping_list2.pk}/delete/")
    assert response1.status_code == 302
    response2 = client.get(f"/list/shop/{fake_shopping_list2.pk}/")
    assert response2.status_code == 404


@pytest.mark.django_db
def test_add_shopping_list_element_view(client, fake_user, fake_shopping_list):
    client.force_login(fake_user)
    response = client.post(
        f"/list/shop/{fake_shopping_list.pk}/add-item/",
        {
            "element_name": "fake elem name",
            "element_description": "Fake elem desc",
            "amount": 2,
            "list_pk": fake_shopping_list,
            "bought": 0,
        }
    )
    assert response.status_code == 200
    assert List_Element.objects.get(element_name="fake elem name")
    assert List_Element.objects.get(amount=2)


@pytest.mark.django_db
def test_edit_shopping_list_element_view(client, fake_user, fake_shopping_list, fake_list_elements):
    client.force_login(fake_user)   # mucho importante without this it will always redirect to login page with HTTP:200
    element = List_Element.objects.all().filter(list_pk=fake_shopping_list)[0]
    response = client.post(
        f"/list/shop/{fake_shopping_list.pk}/{element.pk}/",
        {
            'element_name' : "nazwa5_edited",
            'amount' : 5,
        }
    )
    assert response.status_code == 302
    assert List_Element.objects.get(element_name='nazwa5_edited')


@pytest.mark.django_db
def test_add_shopping_list_element_to_default_view(client, fake_user):
    client.force_login(fake_user)
    response = client.post(
        f"/list/shop/default/add-item/",
        {
            "element_name": "fake elem name def",
            "element_description": "Fake elem desc",
            "amount": 2,
            "bought": 0,
        }
    )
    assert response.status_code == 200
    assert List_Element.objects.get(element_name="fake elem name def")
    assert List_Element.objects.get(amount=2)

# To-Do Tests

@pytest.mark.django_db
def test_to_do_list_view(client, fake_user, fake_to_do_list):
    client.force_login(fake_user)
    response = client.get("/list/to-do/all/")
    owner = User.objects.get(username="fake_user")
    assert response.status_code == 200
    assert response.context['lists'][0].list_name == "Default To-Do List"
    assert response.context['lists'][1].list_category == "Fake category1"
    assert response.context['lists'][1].list_name == "fake name1 to do"


@pytest.mark.django_db
def test_add_to_do_list_view(client, fake_user):
    client.force_login(fake_user)   # mucho importante without this it will always redirect to login page with HTTP:200
    response = client.post(
        "/list/to-do/add/",
        {
            "list_name": "fake name4 to do",
            "list_category": "fake4 category1"
        }
    )
    assert response.status_code == 302
    assert To_Do_List.objects.get(list_name='fake name4 to do')


@pytest.mark.django_db
def test_to_do_list_detail_view(client, fake_user, fake_to_do_list, fake_to_do_list_elements):
    client.force_login(fake_user)
    response = client.get(f"/list/to-do/{fake_to_do_list.pk}/")
    assert response.context['list'].list_name == "fake name1 to do"
    assert response.context['list'].list_category == "Fake category1"
    assert response.context['elements'][0].element_name == 'nazwa1 to do'
    assert response.context['elements'][0].completed == 0
    assert response.context['elements'][1].element_description == 'desc3'
    assert response.context['elements'][2].completed == 1
    assert response.status_code == 200


@pytest.mark.django_db
def test_edit_to_do_list_view(client, fake_user, fake_to_do_list2):
    client.force_login(fake_user)   # mucho importante without this it will always redirect to login page with HTTP:200
    response = client.post(
        f"/list/to-do/{fake_to_do_list2.pk}/edit/",
        {
            'list_name' : "fake name10 to do edited",
            'list_category' : "fake category10 edited",
        }
    )
    assert response.status_code == 302
    assert To_Do_List.objects.get(list_name='fake name10 to do edited')
    assert To_Do_List.objects.get(list_category='fake category10 edited')


@pytest.mark.django_db
def test_delete_to_do_list_view(client, fake_user, fake_to_do_list2):
    client.force_login(fake_user)   # mucho importante without this it will always redirect to login page with HTTP:200
    response1 = client.post(f"/list/to-do/{fake_to_do_list2.pk}/delete/")
    assert response1.status_code == 302
    response2 = client.get(f"/list/to-do/{fake_to_do_list2.pk}/")
    assert response2.status_code == 404


@pytest.mark.django_db
def test_add_to_do_list_element_view(client, fake_user, fake_to_do_list):
    client.force_login(fake_user)
    response = client.post(
        f"/list/to-do/{fake_to_do_list.pk}/add-item/",
        {
            "element_name": "fake elem name",
            "element_description": "Fake elem desc",
            "list_pk": fake_to_do_list,
            "completed": 0,
        }
    )
    assert response.status_code == 200
    assert To_Do_Element.objects.get(element_name="fake elem name")
    assert To_Do_Element.objects.get(element_description='Fake elem desc')


@pytest.mark.django_db
def test_edit_to_do_list_element_view(client, fake_user, fake_to_do_list, fake_to_do_list_elements):
    client.force_login(fake_user)   # mucho importante without this it will always redirect to login page with HTTP:200
    element = To_Do_Element.objects.all().filter(list_pk=fake_to_do_list)[0]
    response = client.post(
        f"/list/to-do/{fake_to_do_list.pk}/{element.pk}/",
        {
            'element_name' : "nazwa5_edited",
            'completed' : 1,
        }
    )
    assert response.status_code == 302
    assert To_Do_Element.objects.get(element_name='nazwa5_edited')


@pytest.mark.django_db
def test_add_to_do_list_element_to_default_view(client, fake_user):
    client.force_login(fake_user)
    response = client.post(
        f"/list/to-do/default/add-item/",
        {
            "element_name": "fake elem name def",
            "element_description": "Fake elem desc",
            "completed": 1,
        }
    )
    assert response.status_code == 200
    assert To_Do_Element.objects.get(element_name="fake elem name def")
    assert To_Do_Element.objects.get(element_description='Fake elem desc')

# No access redirect test

@pytest.mark.django_db
def test_no_access_to_list_statement(client, fake_user, fake_staff):
    client.force_login(fake_user)
    no_access_list = Shopping_List.objects.all().filter(list_owner=fake_staff)[0]
    response = client.get(f"/list/shop/{no_access_list.pk}/")
    assert response.context['access'] == 'no_access'