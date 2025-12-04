# Finance App — Documentation

The **Finance** app manages core financial functionality including accounts, categories, and transactions. It provides a fully authenticated, soft‑delete‑enabled financial subsystem with balance tracking, categorized spending, and income/expense management.

## 🚀 Main Responsibilities

- Manage **accounts** with balances
- Manage **nested categories** (global or user-specific)
- Process **transactions** and auto‑update account balances
- Enforce user-level **ownership and permissions**
- Provide fully documented **REST API endpoints**
- Handle **soft delete** instead of hard deletion

---

## 📂 Application Structure

```
apps/finance/
    ├── models/
    │   ├── account.py
    │   ├── category.py
    │   └── transaction.py
    ├── serializers/
    ├── views/
    ├── permissions/
    ├── tests/
    └── README.md
```

---

# 🧩 Models Overview

## 1. Account

Represents a user’s financial account.

- Linked to a **user**
- Supports types (`main`, `savings`, `cash`)
- Tracks **balance**
- All removals use **soft delete**
- Updated automatically when transactions are created or deleted

---

## 2. Category

Represents a category or subcategory for transactions.

- Belongs to a user or is **global** (`user=None`)
- Supports **parent-child** nesting
- Enforces unique `(user, name, parent)`
- Soft deleted instead of removed
- Used to classify transactions

---

## 3. Transaction

Represents an income or expense movement.

- Belongs to a user, account, category
- Supports `income` or `expense`
- Automatically updates the associated account balance
- Soft deleted with rollback of balance impact

### Balance Rules:

| Type     | On Create | On Delete |
|----------|-----------|-----------|
| Income   | + amount  | – amount  |
| Expense  | – amount  | + amount  |

---

# 🔐 Permissions

### **IsOwnerOrReadOnlyGlobal**

- Users may edit **only their own categories**
- Global categories are **read-only**
- Transactions require:
  - user-owned account
  - user-owned or global category

---

# 📡 API Endpoints

### Accounts

| Action | Method | Endpoint |
|--------|--------|----------|
| List | GET | `/accounts/` |
| Retrieve | GET | `/accounts/{id}/` |
| Create | POST | `/accounts/` |
| Update | PUT/PATCH | `/accounts/{id}/` |
| Delete (soft) | DELETE | `/accounts/{id}/` |

### Categories

| Action | Method | Endpoint |
|--------|--------|----------|
| List (global + own) | GET | `/categories/` |
| Retrieve | GET | `/categories/{id}/` |
| Create | POST | `/categories/` |
| Update | PUT/PATCH | `/categories/{id}/` |
| Delete (soft) | DELETE | `/categories/{id}/` |

### Transactions

| Action | Method | Endpoint |
|--------|--------|----------|
| List | GET | `/transactions/` |
| Retrieve | GET | `/transactions/{id}/` |
| Create | POST | `/transactions/` |
| Update | PUT/PATCH | `/transactions/{id}/` |
| Delete (soft, revert balance) | DELETE | `/transactions/{id}/` |

All endpoints support **drf-spectacular** OpenAPI documentation.

---

# 🧪 Testing

Coverage includes:

- CRUD operations for all models
- Soft deletion behavior
- Transaction balance logic
- Category parenting validation
- Ownership & permissions
- Serializer field validation

Run tests:

```bash
pytest --cov=apps/finance --cov-report=term-missing
```

---

# 🧱 Design Principles

- **Soft deletion only**
- **Automatic balance updates**
- **User‑isolated data with global overrides**
- **select_related for efficient DB access**
- **Clean API-first design**
- **Extensive pytest coverage**

---

# 🏁 Summary

The Finance app is the core financial system of the project:

✔ Account management  
✔ Categorized transactions  
✔ Income & expense operations  
✔ Balance tracking  
✔ Permissions enforcement  
✔ Full API documentation  

It is designed to be secure, maintainable, efficient, and fully testable.
