import pytest


# Boundary values: 1 and 5 stars are saved, 0 and 6 are refused and leave the rating unchanged.
@pytest.mark.parametrize("stars, status", [(0, 400), (1, 200), (5, 200), (6, 400)])
def test_update_stars_boundaries(api, auth, rating, stars, status):
    path = f"/api/ratings/{rating['id']}"
    res = api.put(path, json={"stars": stars}, headers=auth)
    assert res.status_code == status
    expected = stars if status == 200 else rating["stars"]
    res = api.get(path, headers=auth)
    assert res.status_code == 200
    assert res.json()["stars"] == expected
