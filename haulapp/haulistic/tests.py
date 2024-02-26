import pytest
from .models import Shopping_List, List_Element


# @pytest.mark.django_db            # to do testowania detailed view
# def test_add_list_view(client, fake_shopping_list): 
#     response = client.get(f"/list/{fake_shopping_list.pk}/")
#     assert response.status_code == 200
#     assert response.context["list_name"] == "fake name"
#     assert response.context["list_category"] == "Fake category"
#     assert response.context["list_owner"] == 3


@pytest.mark.django_db
def test_add_list_view(client):
    response = client.post(
        "/list/add/",
        {
            "list_name": "fake name",
            "list_category": "Fake category",
            "list_owner": 3,
        }
    )
    assert response.status_code == 302
    assert Shopping_List.objects.get(list_name="fake name")


@pytest.mark.django_db
def test_add_list_element_view(client, fake_shopping_list):
    response = client.post(
        f"list/{fake_shopping_list.pk}/add-item/",
        {
            "element_name": "fake elem name",
            "element_description": "Fake elem desc",
            "amount": 2,
            "list_pk": fake_shopping_list.pk,
        }
    )
    assert response.status_code == 302
    assert Shopping_List.objects.get(list_name="fake elem name")
    assert Shopping_List.objects.get(amount=2)


# @pytest.mark.django_db
# def test_products_list(client, fake_list_elements):
#     response = client.get("/")
#     assert response.status_code == 200
#     # assert response.context['fake_list_elements'] == nazwa1 > nazwa2 > nazwa3