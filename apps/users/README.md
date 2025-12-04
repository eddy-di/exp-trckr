# Users App — Documentation

The **Users** app provides authentication, registration, and identity management for the entire project.  
It includes a fully custom user model with multi-identifier login support (email, username, or phone), JWT authentication, and secure registration workflows.

---

# 🚀 Main Responsibilities

- Custom **User** model (email/username/phone login)
- Multi-field JWT authentication (`email OR username OR phone`)
- Registration endpoint with immediate token issuance
- Token refresh & verification
- Password validation & hashing
- Soft-delete and restore functionality
- Custom authentication backend support
- Serializer-based user creation & login handling

---

# 📂 App Structure

```
apps/users/
    ├── models.py
    ├── views.py
    ├── serializers.py
    ├── urls.py
    ├── managers.py
    ├── backends.py   (if implemented)
    ├── tests/
    └── README.md
```

---

# 👤 Custom User Model

The `User` model extends Django's:

- `AbstractBaseUser`
- `PermissionsMixin`
- `BaseModel` (project common model)

### Supported identifiers:

- `email`
- `username`
- `phone`

Only **one** is required to create a user.

### Additional fields:

- `first_name`
- `last_name`
- `currency` (default `"USD"`)

### Authentication field:

```
USERNAME_FIELD = "email"
```

Passwords are hashed automatically via:

```
user.set_password()
```

---

# ⚙️ User Manager

The custom `UserManager` supports:

### `create_user()`
- At least one identifier must be provided (email/username/phone)
- Normalizes email
- Hashes password

### `create_superuser()`
- Requires email
- Sets: `is_staff = True`, `is_superuser = True`, `is_active = True`

---

# 🧩 Soft Delete & Restore

The user model supports safe account removal:

### Soft Delete:
- sets `is_active = False`
- sets `is_deleted = True`
- timestamps `deleted_at`

### Restore:
- re-enables user account
- removes delete flags

These operations avoid data loss while disabling login.

---

# 🔐 Authentication Logic

The app uses **SimpleJWT** for token-based authentication:

- Access token
- Refresh token

Custom serializer enables **multi-field authentication**:

### Login Payload:
```json
{
  "identifier": "email_or_username_or_phone",
  "password": "your-password"
}
```

---

# 🧩 Serializers Overview

## 1. `RegisterSerializer`
- Validates passwords match
- Ensures **at least one identifier** exists
- Validates password strength
- Creates user securely in atomic transaction
- Returns user + JWT tokens in response

## 2. `MultiFieldTokenObtainPairSerializer`
- Extends `TokenObtainPairSerializer`
- Allows login by: email, username, or phone
- Raises proper `AuthenticationFailed` exceptions
- Returns:
  - access token
  - refresh token
  - user details

## 3. `RegisterResponseSerializer`
Used in OpenAPI schema for registration responses.

---

# 📡 API Endpoints

Base path:

```
/api/v1/auth/
```

### **Register**
```
POST /api/v1/auth/register/
```

Returns access + refresh tokens immediately.

### **Login**
```
POST /api/v1/auth/token/
```

Accepts:
```json
{
    "identifier": "email/username/phone",
    "password": "password"
}
```

### **Token Refresh**
```
POST /api/v1/auth/token/refresh/
```

### **Token Verify**
```
POST /api/v1/auth/token/verify/
```

---

# 🧪 Tests

The `tests` module includes:

- Registration tests
- Login tests for email/username/phone
- Token refresh tests
- Token verify tests
- Inactive user login handling
- Serializer validation tests
- User model and manager tests

Run tests:

```bash
pytest apps/users --cov=apps/users --cov-report=term-missing
```

---

# 🛠 Requirements

Make sure authentication backend is configured:

```python
AUTHENTICATION_BACKENDS = [
    "apps.users.backends.MultiIdentifierBackend",
    "django.contrib.auth.backends.ModelBackend",
]
```

---

# 🏁 Summary

The Users app provides the authentication backbone of the system:

✔ Custom user model  
✔ Email/username/phone login  
✔ Secure registration  
✔ JWT authentication  
✔ Token refresh & verify  
✔ Soft delete + restore  
✔ Full test coverage  
✔ API-first design with drf-spectacular  

It ensures a flexible and secure identity system suitable for modern web and mobile applications.