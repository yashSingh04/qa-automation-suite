import pytest
from jsonschema import validate

POST_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "userId": {"type": "integer"},
        "title": {"type": "string"},
        "body": {"type": "string"},
    },
    "required": ["id", "userId", "title", "body"],
}


@pytest.mark.api
@pytest.mark.smoke
def test_list_posts_returns_200_and_full_collection(api):
    response = api.get("/posts")
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert len(body) == 100


@pytest.mark.api
@pytest.mark.smoke
def test_single_post_matches_schema(api):
    response = api.get("/posts/1")
    assert response.status_code == 200
    validate(instance=response.json(), schema=POST_SCHEMA)


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.parametrize("post_id", [1, 25, 50, 100], ids=lambda i: f"post-{i}")
def test_known_posts_are_retrievable(api, post_id):
    response = api.get(f"/posts/{post_id}")
    assert response.status_code == 200
    assert response.json()["id"] == post_id


@pytest.mark.api
@pytest.mark.negative
@pytest.mark.parametrize("post_id", [0, 101, 999999], ids=["zero", "just-past-end", "far-out-of-range"])
def test_nonexistent_post_returns_404(api, post_id):
    assert api.get(f"/posts/{post_id}").status_code == 404


@pytest.mark.api
@pytest.mark.regression
def test_create_post_returns_201_and_echoes_payload(api):
    payload = {"title": "QA automation suite", "body": "created by test", "userId": 7}
    response = api.post("/posts", json=payload)
    assert response.status_code == 201
    created = response.json()
    assert created["title"] == payload["title"]
    assert created["userId"] == payload["userId"]
    assert "id" in created


@pytest.mark.api
@pytest.mark.regression
def test_update_post_persists_changes(api):
    payload = {"id": 1, "title": "updated title", "body": "updated body", "userId": 1}
    response = api.put("/posts/1", json=payload)
    assert response.status_code == 200
    assert response.json()["title"] == "updated title"


@pytest.mark.api
@pytest.mark.regression
def test_patch_updates_only_supplied_field(api):
    response = api.patch("/posts/1", json={"title": "patched"})
    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "patched"
    assert body["userId"] == 1, "PATCH must not clear untouched fields"


@pytest.mark.api
@pytest.mark.regression
def test_delete_post_returns_200(api):
    assert api.delete("/posts/1").status_code == 200


@pytest.mark.api
@pytest.mark.regression
def test_filter_posts_by_user(api):
    response = api.get("/posts", params={"userId": 3})
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 10
    assert all(p["userId"] == 3 for p in body)


@pytest.mark.api
def test_response_time_within_budget(api):
    response = api.get("/posts/1")
    assert response.elapsed.total_seconds() < 3, "GET /posts/1 exceeded the 3s budget"


@pytest.mark.api
def test_content_type_is_json(api):
    response = api.get("/posts/1")
    assert "application/json" in response.headers["Content-Type"]
