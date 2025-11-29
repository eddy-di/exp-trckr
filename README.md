# Backend Project Conventions & Best Practices

This document defines the **mandatory conventions and best practices** for working on this Django backend project. All contributors must follow these rules to ensure consistency, maintainability, and scalability.

---

## 1. General Principles

* Follow **PEP8** for Python code styling.
* Prefer **clarity over cleverness**.
* Write **small, single-responsibility functions**.
* Never commit secrets (`.env`, API keys, credentials).
* All new code must be covered with **basic tests**.

---

## 2. Project Structure

```txt
project_root/
├── apps/                  # All Django apps live here
├── common/                # Shared models, utils, permissions
├── config/                # Django settings, urls, wsgi, asgi
├── templates/             # App templates (if any)
├── manage.py
├── .env
├── requirements.txt
```

### Rules

* ❌ Do NOT create apps in the root directory
* ✅ Always create apps inside `apps/`
* ✅ Always use absolute imports (`apps.users.models`)

#### Short memo on apps creation

If you already have an app that has to be created in apps folder create the folder with the apps name.
Lets give an example with `accounts` app.

1. go to apps folder and create accounts empty folder
2. then type in this command to make apps registered in an empty folder

```
python manage.py startapp accounts apps/accounts
```

3. In settings part make sure to register an app like this `apps.accounts`

4. In created folder there will we `apps.py` inside it the variable `name` has to also include the apps folder beofre the name of the app. `apps.accounts`

---

## 3. App Naming Conventions

### Django Apps

* Must be **plural nouns**
* Must be **lowercase**

✅ Good:

```txt
users
accounts
transactions
categories
```

❌ Bad:

```txt
UserApp
accountApp
Transaction
```

### Python Files

* Must be **snake_case**

✅ `serializers.py`, `services.py`
❌ `serializersFile.py`

---

## 4. Model Naming Conventions

### Model Class Names

* Must be **singular**
* Must be **PascalCase**

✅ `User`, `Account`, `Transaction`, `Category`
❌ `Users`, `user`, `account_model`

---

## 5. Database Table Naming

### Custom Table Names

Table names have to be always provided in plural.

```python
class Meta:
    db_table = "accounts"
```

---

## 6. Base Model Convention (MANDATORY)

All models MUST inherit from the global base model:

```python
class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
```

✅ Enforces:

* UUID primary keys
* Auditing
* Soft delete

❌ Creating raw `models.Model` directly is forbidden

---

## 7. Foreign Key & Relationship Rules

* Always use **explicit `related_name`**

✅ Good:

```python
user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="accounts")
```

❌ Bad:

```python
user = models.ForeignKey(User, on_delete=models.CASCADE)
```

### Many-to-Many Fields

* Can use explicit `through` table for business logic M2M or implicit

---

## 8. Field Naming Conventions

* Use **descriptive snake_case**

✅ `created_at`, `total_amount`, `is_active`
❌ `createdAt`, `TotalAmount`, `flag`

### Boolean Fields

* Must start with:

✅ `is_`, `has_`, `can_`

✅ `is_deleted`, `has_access`
❌ `deleted`, `access`

---

## 9. API & Serializer Rules

### Serializer Naming

✅ `UserSerializer`, `AccountCreateSerializer`
❌ `user_serializer`, `AccountSerializer2`

### View Naming

✅ `AccountListAPIView`, `TransactionViewSet`
❌ `AccountView1`

### API Versioning

```txt
/api/v1/users/
/api/v1/accounts/
```

---

## 10. Migrations & Database Rules

* ✅ Run `makemigrations` for every model change
* ✅ Review migrations before committing
* ❌ Never manually modify applied migrations in production

---

## 11. Environment Variables

* `.env` is required locally
* `.env` is NOT committed

```env
DEBUG=True
SECRET_KEY=xxx
DATABASE_URL=xxx
```

---

## 12. Git Workflow Rules

* `main` → production
* `dev` → staging
* Feature branches:

```txt
feat/expense-category
fix/account-balance
```

### Commit Messages

✅

```txt
feat: add transaction model
fix: correct account balance calculation
refactor: optimize transaction queries
```

---

## 13. Code Review Rules

* No direct push to `main`
* At least **1 reviewer required**
* Must pass:

  * Tests
  * Linting
  * Migrations check

---

## 14. Security Rules (CRITICAL)

* ❌ Never log passwords or tokens
* ✅ Always hash passwords
* ✅ Use HTTPS in production
* ✅ Rotate secrets regularly

---

## 15. Logging & Monitoring

* Use structured logging
* No `print()` in production code
* All exceptions must be logged

---

## 16. Documentation Rules

* Every app MUST have:

  * `README.md`
  * Model docstrings
  * Service docstrings

* Swagger / OpenAPI must be updated after API changes

---

## 17. Breaking Change Policy

A change is considered **breaking** if it:

* Modifies DB schema
* Changes API response format
* Affects authentication logic

✅ Must be announced to the team before merging

---

## 18. Django REST Framework (DRF) Specific Conventions

### 18.1 API Design Principles

* APIs must be **stateless** and **resource-oriented**.
* Use **nouns**, not verbs, in endpoints.

✅ Good:

```txt
/api/v1/accounts/
/api/v1/transactions/
```

❌ Bad:

```txt
/api/v1/getAccounts/
/api/v1/createTransaction/
```

* Always version APIs using `/api/v1/`.

---

### 18.2 View Layer Rules

* Prefer **ViewSets + Routers** over individual APIViews for CRUD.
* Use:

  * `ModelViewSet` for full CRUD
  * `ReadOnlyModelViewSet` for read-only resources

✅ Naming:

```python
class TransactionViewSet(ModelViewSet):
    ...
```

❌ Avoid:

```python
class TransactionView1(APIView):
```

* Business logic MUST live in `services.py`, not inside views.

---

### 18.3 Serializer Rules

* Separate serializers by purpose:

✅

```txt
serializers.py
  - TransactionListSerializer
  - TransactionCreateSerializer
  - TransactionDetailSerializer
```

* Do NOT use `depth` in serializers.
* All writable nested logic must be implemented manually.
* Validation logic must live in `validate()` or field-level validators.

---

### 18.4 Permissions & Authentication

* Do NOT use `AllowAny` on production endpoints unless explicitly required.
* All protected endpoints must declare:

```python
permission_classes = [IsAuthenticated]
```

* Custom permissions must live in `common/permissions.py`.

---

### 18.5 Pagination, Filtering & Ordering

* All list endpoints MUST support pagination.
* Use `django-filter` for filtering.
* Ordering must be explicitly allowed using `ordering_fields`.

---

### 18.6 Response Format Rules

✅ Success:

```json
{
  "status": "success",
  "data": {}
}
```

✅ Error:

```json
{
  "status": "error",
  "message": "Validation failed",
  "errors": {}
}
```

---

### 18.7 OpenAPI / Swagger Rules

* All endpoints MUST be documented.
* Schema updates are mandatory for:

  * New endpoints
  * Modified serializers
  * Modified request/response structures

---

## 19. Testing Rules & Standards

### 19.1 Testing Framework

* Use **pytest + pytest-django** for all tests.
* Django `TestCase` is allowed only for legacy code.

---

### 19.2 Test Types (Mandatory Coverage)

Each feature MUST include:

* ✅ Model tests
* ✅ Service tests
* ✅ API endpoint tests

---

### 19.3 Test File Naming

```txt
test_models.py
test_services.py
test_api.py
```

---

### 19.4 Test Data Rules

* Use **factory_boy** for test data generation.
* Do NOT hardcode IDs.
* UUIDs must be dynamically generated.

---

### 19.5 API Test Rules

* Every endpoint must test:

  * ✅ Success case
  * ✅ Unauthorized access
  * ✅ Invalid payload
  * ✅ Permission denial

---

### 19.6 Database Rules in Tests

* Each test must be isolated.
* No test may depend on another.
* Rollbacks must be automatic.

---

### 19.7 Coverage Requirements

* Minimum required coverage: **80%**
* Critical logic (auth, payments, balances): **95%+**

---

### 19.8 CI Testing Rules

* All tests MUST pass in CI before merge.
* Migrations must be applied successfully in CI.

---

## 20. Module and import rules

Importing other modules in the project through `\` sign are not welcome.

Use brackets and import all the necessary modules, classes and other things as in the follofing example:

```python
from models import (
    User,
    Account,
    Category,
)
```

---

## 21. Celery & Background Jobs Conventions
### 21.1 Queue & Task Design Rules

All background jobs must be implemented as Celery tasks.

Tasks must be:

Idempotent (safe to retry)

Stateless

Short-running (no long blocking logic)

Heavy business logic must live in services.py, not inside the task itself.

✅ Good:

@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=5)
def recalc_account_balance_task(self, account_id):
    recalc_account_balance(account_id)


❌ Bad:

@shared_task
def big_task():
    # 200 lines of business logic here ❌

### 21.2 Task Naming Conventions

Task names must be descriptive and action-based:

✅ Good:

send_transaction_notification
recalculate_account_balance
generate_monthly_report


❌ Bad:

task1
handle_data
process

### 21.3 Retry & Failure Rules

All critical tasks must define retry behavior.

Use:

Exponential backoff

Max retry limit

All task failures must be logged.

✅ Required:

autoretry_for=(Exception,)
retry_backoff=5
retry_kwargs={"max_retries": 3}

## 22. Celery Testing Rules
### 22.1 Test Execution Mode

All Celery tests must run with:

CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True


This forces tasks to run synchronously during tests.

### 22.2 Task Test Coverage Requirements

Every Celery task must have:

✅ Success test

✅ Retry test

✅ Failure handling test (if critical)

✅ Side-effect validation (DB, cache, emails)

✅ Example Task Test
def test_recalculate_balance_task(db, account):
    recalc_account_balance_task.delay(account.id)
    account.refresh_from_db()
    assert account.balance == expected_balance

Prohibited in Tests

❌ No real Redis

❌ No real SMTP

❌ No external API calls

❌ No sleeping or time-based waiting

✅ Dedicated Queues (If Used)

Use separate queues for:

`default`

`emails`

`reports`

Do NOT mix long-running jobs with critical API-response tasks.


## 23. Final Rule

> ❗ If it is not documented here — **ask before implementing**.

---

✅ This document is **mandatory for all contributors**.
