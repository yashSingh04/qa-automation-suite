# QA Automation Suite — Selenium + API + CI

Test automation framework in Python covering **UI (Selenium WebDriver)** and
**REST API (requests)** layers, with parallel execution, HTML reporting,
failure screenshots and a GitHub Actions pipeline.

**38 tests — 21 API, 17 UI — all green.**

---

## Why it's built this way

| Decision | Reason |
|---|---|
| **Page Object Model** | Locators live in one place per page. A UI change is a one-line fix, not a sweep through every test. |
| **Explicit waits only** | There is no `time.sleep()` in this repo. Every wait is a condition (`element_to_be_clickable`, `url_contains`), which is what kills flakiness. |
| **Function-scoped driver** | Fresh browser per test, so no state bleeds between cases and tests can run in any order. |
| **Chained page objects** | `login_page.login(...)` returns an `InventoryPage`. Tests read as user journeys, and a wrong-page bug surfaces as a type error rather than a confusing assertion. |
| **Markers** | `smoke` / `regression` / `e2e` / `negative` so CI can run a 30-second gate on PRs and the full suite nightly. |
| **Selenium Manager** | Driver binaries resolve automatically (Selenium 4.6+). No `webdriver-manager`, nothing to pin, no driver drift in CI. |
| **Schema validation** | API responses are checked against JSON Schema, so a contract change fails loudly instead of silently passing a shape check. |

## Layout

```
├── pages/              # Page Object Model
│   ├── base_page.py    # waits, interactions, non-throwing state queries
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   └── checkout_page.py
├── tests/
│   ├── ui/             # Selenium: login, inventory, sorting, E2E checkout
│   └── api/            # requests: CRUD, schema, filtering, perf budget
├── utils/
│   ├── config.py       # env-overridable configuration
│   └── api_client.py   # session wrapper with timeouts + request logging
├── conftest.py         # driver/api fixtures, screenshot-on-failure hook
├── pytest.ini          # markers, reporting, logging
└── .github/workflows/ci.yml
```

## Coverage

**UI** — valid login; five parametrised invalid-login paths; locked-out user;
inventory listing; cart badge add/remove; four sort orders verified against a
sorted reference; full purchase journey with arithmetic reconciliation of
subtotal + tax = total; three incomplete-checkout negative cases.

**API** — collection and single-resource GETs; JSON Schema validation; POST/PUT/
PATCH/DELETE; PATCH verified not to clear untouched fields; query filtering;
nested resources; unique-ID check; email format validation across all records;
404 handling; response-time budget; content-type assertion.

## Running it

```bash
pip install -r requirements.txt

pytest                      # everything
pytest -m api               # API only (no browser needed, ~5s)
pytest -m ui                # UI only
pytest -m smoke             # fast critical path
pytest -m "ui and negative" # combine markers
pytest -n 4                 # 4 workers in parallel
```

Configuration is environment-driven:

```bash
BROWSER=firefox HEADLESS=false pytest -m ui
BASE_URL=https://staging.example.com pytest
```

## CI

`.github/workflows/ci.yml` runs on every push and PR, plus nightly at 02:00 UTC:

- **API job** — installs and runs the API suite
- **UI job** — matrix across **Chrome and Firefox**, headless, 2 workers
- HTML reports and failure screenshots uploaded as artifacts on every run,
  including failures (`if: always()`)

## Targets under test

- UI: [saucedemo.com](https://www.saucedemo.com) — Sauce Labs' public practice application
- API: [jsonplaceholder.typicode.com](https://jsonplaceholder.typicode.com) — public REST fixture service

Both are public sandboxes intended for automation practice, so this suite is
safe to run against them at any time.
