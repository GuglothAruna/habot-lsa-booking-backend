import pytest
from rest_framework.test import APIClient

from lsas.models import LSAProfile, Skill


@pytest.mark.django_db
def test_lsa_search_returns_matching_skill():
    autism = Skill.objects.create(name="Autism")

    lsa = LSAProfile.objects.create(
        name="Priya Sharma",
        email="priya.test@example.com",
        is_active=True,
    )
    lsa.skills.add(autism)

    client = APIClient()

    response = client.get(
        "/api/v1/lsas/search/",
        {"skill": "Autism"},
    )

    assert response.status_code == 200
    assert response.data["count"] == 1
    assert response.data["results"][0]["name"] == "Priya Sharma"


@pytest.mark.django_db
def test_lsa_search_does_not_return_wrong_skill():
    autism = Skill.objects.create(name="Autism")
    dyslexia = Skill.objects.create(name="Dyslexia")

    lsa = LSAProfile.objects.create(
        name="Anita Rao",
        email="anita.test@example.com",
        is_active=True,
    )
    lsa.skills.add(dyslexia)

    client = APIClient()

    response = client.get(
        "/api/v1/lsas/search/",
        {"skill": "Autism"},
    )

    assert response.status_code == 200
    assert response.data["count"] == 0
    import pytest
from django.test.utils import CaptureQueriesContext
from django.db import connection
from rest_framework.test import APIClient

from lsas.models import LSAProfile, Skill


@pytest.mark.django_db
def test_lsa_search_does_not_have_n_plus_one():
    skill = Skill.objects.create(name="Autism")

    for index in range(10):
        lsa = LSAProfile.objects.create(
            name=f"LSA {index}",
            email=f"lsa{index}@example.com",
            is_active=True,
        )
        lsa.skills.add(skill)

    client = APIClient()

    with CaptureQueriesContext(connection) as queries:
        response = client.get(
            "/api/v1/lsas/search/",
            {"skill": "Autism"},
        )

    assert response.status_code == 200
    assert response.data["count"] == 10

    # The number of queries should stay small and should not
    # increase once per LSA.
    assert len(queries) <= 4