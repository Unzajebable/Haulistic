import pytest
from haulistic.models import Shopping_List, List_Element


@pytest.fixture
def fake_shopping_list():
    return Shopping_List.objects.create(
        list_name = "fake name1",
        list_category = "Fake category1",
        list_owner = 3,
    )


@pytest.fixture
def fake_list_elements():
    List_Element.objects.create(
        list_pk = 1,
        element_name = "nazwa1",
        element_description= "desc1",
        amount= 2,
    )
    List_Element.objects.create(
        list_pk = 1,
        element_name = "nazwa2",
        element_description= "desc2",
        amount= 4,
    )
    List_Element.objects.create(
        list_pk = 1,
        element_name = "nazwa3",
        element_description= "desc3",
        amount= 3,
    )

