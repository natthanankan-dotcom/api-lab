import pytest

STARS_ERROR = "number of stars must be between 1 and 5 (inclusive)"
AUTH_ERROR = "authentication failed"


def type_error(kind):
    """The message that QuickPizza gives when stars has the wrong JSON type."""
    return f"json: cannot unmarshal {kind} into Go struct field Rating.stars of type int"


# Base choice: 3 stars as a whole number, a real pizza, the user's token.
def test_base_choice_is_saved(api, auth, pizza_id):
    new = {"pizza_id": pizza_id, "stars": 3}
    res = api.post("/api/ratings", json=new, headers=auth)
    assert res.status_code == 201
    assert res.json()["stars"] == 3
    assert res.json()["pizza_id"] == pizza_id
    api.delete(f"/api/ratings/{res.json()['id']}", headers=auth)


# C1: a number of stars below 1 or above 5 is refused with a message.
@pytest.mark.parametrize("stars", [0, 6])
def test_stars_out_of_range(api, auth, pizza_id, stars):
    new = {"pizza_id": pizza_id, "stars": stars}
    res = api.post("/api/ratings", json=new, headers=auth)
    assert res.status_code == 400
    assert res.json() == {"error": STARS_ERROR}


# C2 decimal: 3.5 stars is refused, because stars must be a whole number.
def test_stars_decimal_is_refused(api, auth, pizza_id):
    new = {"pizza_id": pizza_id, "stars": 3.5}
    res = api.post("/api/ratings", json=new, headers=auth)
    assert res.status_code == 400
    assert res.json() == {"error": type_error("number 3.5")}


# C2 text: stars written as the text "3" is refused.
def test_stars_text_is_refused(api, auth, pizza_id):
    new = {"pizza_id": pizza_id, "stars": "3"}
    res = api.post("/api/ratings", json=new, headers=auth)
    assert res.status_code == 400
    assert res.json() == {"error": type_error("string")}


# C2 missing: a rating without the stars field is refused.
def test_stars_missing_is_refused(api, auth, pizza_id):
    new = {"pizza_id": pizza_id}
    res = api.post("/api/ratings", json=new, headers=auth)
    assert res.status_code == 400
    assert res.json() == {"error": STARS_ERROR}


# C3 does not exist: a rating for a pizza that does not exist is refused.
def test_pizza_does_not_exist_is_refused(api, auth):
    new = {"pizza_id": 999999999, "stars": 3}
    res = api.post("/api/ratings", json=new, headers=auth)
    assert res.status_code == 400
    assert res.json() == {"error": "pizza ID 999999999 not found"}


# C4 none: a rating without the Authorization header is refused with 401.
def test_no_token_is_refused(api, auth, pizza_id):
    new = {"pizza_id": pizza_id, "stars": 3}
    res = api.post("/api/ratings", json=new)
    assert res.status_code == 401
    assert res.json() == {"error": AUTH_ERROR}


# C4 wrong length: a token that is too short is refused with 401.
def test_short_token_is_refused(api, auth, pizza_id):
    new = {"pizza_id": pizza_id, "stars": 3}
    res = api.post("/api/ratings", json=new, headers={"Authorization": "token short"})
    assert res.status_code == 401
    assert res.json() == {"error": AUTH_ERROR}
