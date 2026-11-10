# api-lab

API tests for [QuickPizza](https://quickpizza.grafana.com), written with pytest and requests
(ITDS362, Lab: API Testing with pytest and requests).

## Install and run

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows PowerShell
# source .venv/bin/activate     # macOS / Linux
pip install -r requirements.txt
pytest -v
```

Save a full run as an HTML report:

```bash
pytest -v --html=report.html --self-contained-html
```

Expected result: `32 passed, 1 xfailed`. The xfail is Defect 1 (see `RESULTS.md`).

Every test that changes data creates its own user with a new name (`lab-` + 12 hex digits)
through the `auth` fixture in `conftest.py`, and every request goes through one
`requests.Session`, so the AWSALB cookie keeps the run on one server.

## Input domain model for `POST /api/ratings` (Step A1)

| Characteristic | Block | Value in the test | Covered by |
|---|---|---|---|
| C1 Value of stars | below 1 | 0 | `test_stars_out_of_range[0]` |
| | 1 to 5 (base) | 3 | `test_base_choice_is_saved` |
| | above 5 | 6 | `test_stars_out_of_range[6]` |
| C2 Type of stars | whole number (base) | 3 | `test_base_choice_is_saved` |
| | decimal | 3.5 | `test_stars_decimal_is_refused` |
| | text | "3" | `test_stars_text_is_refused` |
| | missing | no field | `test_stars_missing_is_refused` |
| C3 Pizza | exists (base) | a new pizza | `test_base_choice_is_saved` |
| | does not exist | 999999999 | `test_pizza_does_not_exist_is_refused` |
| C4 Token | the user's own (base) | from `auth` | `test_base_choice_is_saved` |
| | none | no header | `test_no_token_is_refused` |
| | wrong length | `token short` | `test_short_token_is_refused` |

Base choice coverage: 1 base test + (3−1) + (4−1) + (2−1) + (3−1) = 1 + 2 + 3 + 1 + 2 = **9 tests**,
all in `test_create_rating.py`. Each non-base test changes one characteristic and keeps the others at
the base block.

Boundary values for `PUT /api/ratings/{id}` (Step A3) are 0, 1, 5 and 6, in `test_update_rating.py`.
