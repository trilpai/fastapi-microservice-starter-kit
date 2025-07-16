# 📘 User Domain Data Models Summary

This document provides a comprehensive overview of the six data models used in the **User Domain** of the Trilp AI FastAPI microservice. Each model is documented in detail, including field types, relationships, constraints, and index usage. This is intended as a reliable reference for both new and experienced backend engineers.

---

## 🧩 1. `user`

### 🗂️ Description
The `user` table stores core profile information for individuals who interact with the system. It links to roles, login credentials, and multiple contact identities.

### 🔢 Fields
| Column              | Type           | Constraints                  | Description                                               |
|---------------------|----------------|-------------------------------|-----------------------------------------------------------|
| `id`               | Integer        | PK, Auto-increment            | Unique identifier for the user                            |
| `first_name`       | String(64)     | NOT NULL                      | User's first name                                         |
| `last_name`        | String(64)     | NULLABLE                      | Optional last name                                        |
| `job_title`        | String(128)    | NULLABLE                      | Optional job title or designation                         |
| `gender`           | Enum            | NULLABLE                      | One of: `male`, `female`, `other`, `prefer_not_to_say`    |
| `dob`              | Date           | NULLABLE                      | Date of birth                                             |
| `profile_image_url`| String(512)    | NULLABLE                      | Profile picture URL or path                               |
| `is_active`        | Boolean        | NOT NULL, Default: `True`     | User's active/inactive status                             |
| `role_id`          | Integer        | FK → `role.id`, NOT NULL      | Assigned role                                             |
| `created_at`       | DateTime       | Auto-managed                  | Record creation timestamp                                 |
| `updated_at`       | DateTime       | Auto-managed                  | Record last update timestamp                              |
| `created_by`       | Integer        | NULLABLE                      | User who created the record                               |
| `updated_by`       | Integer        | NULLABLE                      | User who last updated the record                          |
| `deleted_at`       | DateTime       | NULLABLE                      | Timestamp of soft deletion                                |

### 🔗 Relationships
- `role` → many-to-one with `Role`
- `auth` → one-to-one with `UserAuth`
- `identities` → one-to-many with `UserIdentity`

### 🧷 Indexes
- `ix_user_deleted_at`
- `ix_user_role_id`
- `ix_user_is_active`

---

## 🔐 2. `user_auth`

### 🗂️ Description
Stores login credentials and metadata such as account lockouts and last login times.

### 🔢 Fields
| Column               | Type           | Constraints                    | Description                                               |
|----------------------|----------------|---------------------------------|-----------------------------------------------------------|
| `id`                | Integer        | PK, Auto-increment              | Unique ID                                                 |
| `user_id`           | Integer        | FK → `user.id`, NOT NULL        | Owner of this auth record                                 |
| `username`          | String(100)    | UNIQUE, NULLABLE                | Optional login username                                   |
| `password_hash`     | String(256)    | NOT NULL                        | Hashed password                                           |
| `wrong_password_count`| Integer      | NOT NULL, Default: `0`          | Failed login attempts                                     |
| `account_locked_until`| DateTime     | NULLABLE                        | Lockout expiry timestamp                                  |
| `last_login_at`     | DateTime       | NULLABLE                        | Last successful login                                     |
| `created_at`, `updated_at`, `deleted_at` etc. | See `TimestampMixin` |

### 🔗 Relationships
- `user` → one-to-one with `User`

### 🧷 Indexes
- `ix_user_auth_deleted_at`
- `ix_user_auth_user_id`

---

## 🆔 3. `user_identity`

### 🗂️ Description
Represents contact or login identities like email, mobile, or OAuth UID. Supports verification, OTP, and primary designation.

### 🔢 Fields
| Column               | Type             | Constraints                                  | Description                                |
|----------------------|------------------|----------------------------------------------|--------------------------------------------|
| `id`                | Integer          | PK, Auto-increment                            | Unique ID                                   |
| `user_id`           | Integer          | FK → `user.id`, NOT NULL                      | Owner of this identity                      |
| `type`              | Enum             | NOT NULL (email, mobile, oauth)               | Identity type                               |
| `value`             | String(191)      | NOT NULL                                      | Email, phone number, or OAuth UID          |
| `is_verified`       | Boolean          | Default: `False`                              | Identity verified?                          |
| `is_primary`        | Boolean          | Default: `False`                              | Preferred contact method                    |
| `oauth_provider`    | String(50)       | NULLABLE                                      | OAuth provider (if type = oauth)           |
| `otp_code`          | String(10)       | NULLABLE                                      | Last OTP sent                               |
| `otp_generated_at`  | DateTime         | NULLABLE                                      | OTP generation time                         |
| `wrong_otp_count`   | Integer          | Default: `0`                                  | Wrong OTP attempts                          |
| `otp_locked_until`  | DateTime         | NULLABLE                                      | OTP retry locked until                      |
| `created_at`, `updated_at`, `deleted_at` etc. | See `TimestampMixin` |

### 🔗 Relationships
- `user` → many-to-one with `User`

### 🧷 Indexes & Constraints
- `uq_identity_value` (type, value, oauth_provider)
- `ix_user_identity_deleted_at`
- `ix_user_identity_is_verified`
- `ix_user_identity_is_primary`
- `ix_user_identity_user_id`

---

## 🛡️ 4. `role`

### 🗂️ Description
Represents named access groups such as Admin, Manager, etc., with assigned privileges.

### 🔢 Fields
| Column         | Type         | Constraints              | Description                            |
|----------------|--------------|---------------------------|----------------------------------------|
| `id`          | Integer      | PK, Auto-increment        | Unique role ID                         |
| `name`        | String(64)   | UNIQUE, NOT NULL          | Name of the role                       |
| `description` | String(256)  | NULLABLE                  | Optional description                   |
| `created_at`, `updated_at`, `deleted_at` etc. | See `TimestampMixin` |

### 🔗 Relationships
- `privileges` → many-to-many with `Privilege` via `role_privilege`
- `users` → one-to-many with `User`

### 🧷 Indexes
- `ix_role_deleted_at`

---

## 🔐 5. `privilege`

### 🗂️ Description
Defines individual access rights (e.g., `view_dashboard`, `edit_user`) that can be assigned to roles.

### 🔢 Fields
| Column         | Type         | Constraints              | Description                          |
|----------------|--------------|---------------------------|--------------------------------------|
| `id`          | Integer      | PK, Auto-increment        | Unique privilege ID                  |
| `name`        | String(64)   | UNIQUE, NOT NULL          | Privilege code name                  |
| `description` | String(256)  | NULLABLE                  | Optional text explanation            |
| `created_at`, `updated_at`, `deleted_at` etc. | See `TimestampMixin` |

### 🔗 Relationships
- `roles` → many-to-many with `Role` via `role_privilege`

### 🧷 Indexes
- `ix_privilege_deleted_at`

---

## 🔗 6. `role_privilege`

### 🗂️ Description
Join table that maps roles to their privileges, enabling many-to-many relationships.

### 🔢 Fields
| Column         | Type       | Constraints                              | Description                    |
|----------------|------------|-------------------------------------------|--------------------------------|
| `id`          | Integer    | PK, Auto-increment                        | Unique record ID               |
| `role_id`     | Integer    | FK → `role.id`, NOT NULL, CASCADE DELETE  | Associated role                |
| `privilege_id`| Integer    | FK → `privilege.id`, NOT NULL, CASCADE DELETE | Associated privilege      |
| `created_at`, `updated_at`, `deleted_at` etc. | See `TimestampMixin` |

### 🧷 Indexes & Constraints
- `uq_role_privilege` (role_id, privilege_id) → Enforce uniqueness
- `ix_role_privilege_deleted_at`

---

## 📌 Shared Conventions

### Timestamps
All models inherit from `TimestampMixin` which provides:
- `created_at`
- `updated_at`
- `created_by`
- `updated_by`
- `deleted_at` (used for soft-deletion)

### Indexing Strategy
- Soft deletes use `ix_<table>_deleted_at`
- Foreign keys are indexed for join efficiency
- Boolean filters (`is_verified`, `is_active`, etc.) are indexed where frequent filters are expected

### Lazy Loading
- `lazy="joined"` used for most one-to-one and many-to-one relationships for eager loading
- `lazy="selectin"` used for one-to-many and many-to-many to optimize for batch loads

---

## ✅ Summary
This schema enables scalable user management with extensible authentication and role-based access control (RBAC).
Every relationship is well-indexed and documented, ensuring both performance and clarity for future contributors.

Feel free to reach out to the Trilp AI backend team for any clarifications or contributions to the model design.

