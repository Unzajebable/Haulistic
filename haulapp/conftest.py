import pytest
from haulistic.models import User, List_Element, Shopping_List, To_Do_List, To_Do_Element


@pytest.fixture
def fake_user(db):
    fuser = User.objects.create(
        username = 'fake_user',
        password = 'fakePass1',
        email = 'fake@email.com',
        pfpurl = 'fake_link'
    )
    return fuser


@pytest.fixture
def fake_staff(db):
    fuser = User.objects.create(
        username = 'fake_staff',
        password = 'fakePass1',
        email = 'fake@staff.com',
        pfpurl = 'fake_link_staff',
        is_staff = True
    )
    return fuser


@pytest.fixture
def fake_shopping_list(db):
    owner = User.objects.get(username="fake_user")
    flist = Shopping_List.objects.create(
        list_name = "fake name1 shopping",
        list_category = "fake category1",
        list_owner = owner
    )
    return flist


@pytest.fixture
def fake_shopping_list_staff(db):
    owner = User.objects.get(username="fake_staff")
    flist = Shopping_List.objects.create(
        list_name = "fake name1 shopping",
        list_category = "fake category1",
        list_owner = owner
    )
    return flist


@pytest.fixture
def fake_shopping_list2(db):
    owner = User.objects.get(username="fake_user")
    flist = Shopping_List.objects.create(
        list_name = "fake name10 shopping",
        list_category = "fake category10",
        list_owner = owner
    )
    return flist


@pytest.fixture
def fake_list_elements(db):
    flist = Shopping_List.objects.get(list_name = "fake name1 shopping")
    List_Element.objects.create(
        list_pk = flist,
        element_name = "nazwa1",
        element_description= "desc1",
        amount= 2,
        bought = 1
    )
    List_Element.objects.create(
        list_pk = flist,   #możliwe że fake_shopping_list.pk we'll see (prawdopodobnie nie)
        element_name = "nazwa2",
        element_description= "desc2",
        amount= 4,
        bought = 1
    )
    List_Element.objects.create(
        list_pk = flist,
        element_name = "nazwa3",
        element_description= "desc3",
        amount= 3,
        bought = 0
    )


@pytest.fixture
def fake_to_do_list(db):
    owner = User.objects.get(username="fake_user")
    flist = To_Do_List.objects.create(
        list_name = "fake name1 to do",
        list_category = "Fake category1",
        list_owner = owner
    )
    return flist


@pytest.fixture
def fake_to_do_list2(db):
    owner = User.objects.get(username="fake_user")
    flist = To_Do_List.objects.create(
        list_name = "fake name10 to do",
        list_category = "Fake category10",
        list_owner = owner
    )
    return flist


@pytest.fixture
def fake_to_do_list_elements(db):
    flist = To_Do_List.objects.get(list_name = "fake name1 to do")
    To_Do_Element.objects.create(
        list_pk = flist,
        element_name = "nazwa1 to do",
        element_description = "desc1",
        completed = 0,
    )
    To_Do_Element.objects.create(
        list_pk = flist,
        element_name = "nazwa2 to do",
        element_description = "desc2",
        completed = 1,
    )
    To_Do_Element.objects.create(
        list_pk = flist,
        element_name = "nazwa3 to do",
        element_description = "desc3",
        completed = 0,
    )
