def assert_unchanged(api, auth, rating):
    """The owner can still read the rating, and its fields are as they were."""
    res = api.get(f"/api/ratings/{rating['id']}", headers=auth)
    assert res.status_code == 200
    assert res.json() == rating


# Another user cannot read the rating of the owner.
def test_other_user_cannot_read(api, auth, other_auth, rating):
    res = api.get(f"/api/ratings/{rating['id']}", headers=other_auth)
    assert 400 <= res.status_code <= 499
    assert_unchanged(api, auth, rating)


# Another user cannot change the stars of the owner's rating.
def test_other_user_cannot_update(api, auth, other_auth, rating):
    res = api.put(f"/api/ratings/{rating['id']}", json={"stars": 1}, headers=other_auth)
    assert 400 <= res.status_code <= 499
    assert_unchanged(api, auth, rating)


# Another user cannot delete the owner's rating.
def test_other_user_cannot_delete(api, auth, other_auth, rating):
    res = api.delete(f"/api/ratings/{rating['id']}", headers=other_auth)
    assert 400 <= res.status_code <= 499
    assert_unchanged(api, auth, rating)
