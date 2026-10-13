import re

import pytest
from jsonschema import validate

USER_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "username": {"type": "string"},
        "email": {"type": "string"},
        "address": {
            "type": "object",
            "properties": {
                "street": {"type": "string"},
                "city": {"type": "string"},
                "zipcode": {"type": "string"},
                "geo": {
                    "type": "object",
                    "properties": {"lat": {"type": "string"}, "lng": {"type": "string"}},
                    "required": ["lat", "lng"],
                },
            },
            "required": ["street", "city", "zipcode", "geo"],
        },
        "company": {"type": "object", "required": ["name"]},
    },
    "required": ["id", "name", "username", "email", "address", "company"],
}

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@pytest.mark.api
@pytest.mark.smoke
def test_users_collection_size(api):
    response = api.get("/users")
    assert response.status_code == 200
    assert len(response.json()) == 10


@pytest.mark.api
@pytest.mark.regression
def test_every_user_matches_schema_and_has_valid_email(api):
    for user in api.get("/users").json():
        validate(instance=user, schema=USER_SCHEMA)
        assert EMAIL_RE.match(user["email"]), f"Malformed email for user {user['id']}: {user['email']}"


@pytest.mark.api
@pytest.mark.regression
def test_user_ids_are_unique(api):
    ids = [u["id"] for u in api.get("/users").json()]
    assert len(ids) == len(set(ids)), "Duplicate user IDs returned"


@pytest.mark.api
@pytest.mark.regression
def test_nested_posts_belong_to_requested_user(api):
    response = api.get("/users/2/posts")
    assert response.status_code == 200
    body = response.json()
    assert body, "Expected at least one post"
    assert all(p["userId"] == 2 for p in body)


@pytest.mark.api
@pytest.mark.negative
def test_unknown_user_returns_404(api):
    assert api.get("/users/9999").status_code == 404
