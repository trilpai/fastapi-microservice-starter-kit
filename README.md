# fastapi-microservice-starter-kit
Production-ready FastAPI microservice starter with JWT auth, 12-factor priniciples, Docker, CI/CD, and RESTful APIs.

## Initial Structure

```shell

fastapi-microservice-starter-kit/
├── app/
│   ├── api/
│   │   ├── config/              # ✅ settings, logging, constants
│   │   │   ├── settings.py
│   │   │   ├── logging.py
│   │   │   └── constants.py
│   │   ├── deps/                # ✅ Dependency injection (db, user, etc.)
│   │   ├── domains/             # ✅ Renamed from features — more standard
│   │   │   └── user/
│   │   │       ├── controllers/     # Endpoints
│   │   │       ├── services/
│   │   │       ├── models/         # SQLAlchemy models
│   │   │       ├── schemas/        # Pydantic validation
│   │   │       └── repositories/   # DB / RESTful interaction layer
│   │   └── router.py              # ✅ Single entrypoint to API router
│   │
│   ├── webui/
│   │   ├── templates/
│   │   │   └── features/          # Feature pages
│   │   │       └── user/
│   │   ├── static/
│   │   └── router.py              # ✅ Jinja routes go here
│   │
│   └── main.py                    # ✅ Entrypoint mounts both routers
│
├── scripts/                       # ✅ Cleanly isolated DB Migrations
│   ├── migrations/
│   │   ├── env.py                 # Customized to app context
│   │   ├── script.py.mako
│   │   └── versions/
│   │       ├── 2025_07_15_XXXX_create_users_table.py
│   │       └── 2025_07_16_YYYY_add_roles_table.py
│   ├── seeders/
│   │   ├── 2025_07_15__seed_initial_users.py
│   │   └── 2025_07_16__seed_roles.py
│   └── run_seeders.py
│
├── tests/                         # ✅ Only for API — clean!
│   ├── unit/
│   │    └── api/
│   │        └── domains/
│   │            └── user/
│   │                ├── test_services.py
│   │                └── test_schemas.py
│   └── integration/
│        └── api/
│            └── domains/
│                └── user/
│                    └── test_endpoints.py
│
├── postman/                       # ✅ for Postman collection/environment JSON
│   ├── fastapi-starter-collection.json
│   └── fastapi-starter-environment.json
│
├── requirements.txt
├── alembic.ini
├── Dockerfile
├── .env
└── README.md


```

## DB Tables

### Common Fields (to be included in every table)
| Column       | Type     | Constraints                            | Description                                |
| ------------ | -------- | -------------------------------------- | ------------------------------------------ |
| `created_at` | DateTime | Not Null, Default: current timestamp   | Timestamp when the record was created      |
| `updated_at` | DateTime | Not Null, Auto-updated on modification | Timestamp when the record was last updated |
| `created_by` | Integer  | Nullable, FK → `user.id` (optional)    | ID of user who created the record          |
| `updated_by` | Integer  | Nullable, FK → `user.id` (optional)    | ID of user who last modified it            |
| `deleted_at` | DateTime | Nullable                               | If set, record is soft-deleted             |


#### privilege
| Column                      | Type        | Constraints      | Description                   |
| --------------------------- | ----------- | ---------------- | ----------------------------- |
| `id`                        | Integer     | Primary Key      | Auto-incremented ID           |
| `name`                      | String(64)  | Unique, Required | Human-readable privilege name |
| `description`               | String(256) | Optional         | What this privilege allows    |
| + common fields (see above) |             |                  |                               |

#### role
| Column          | Type        | Constraints      | Description                          |
| --------------- | ----------- | ---------------- | ------------------------------------ |
| `id`            | Integer     | Primary Key      | Auto-incremented ID                  |
| `name`          | String(64)  | Unique, Required | Role name like `SuperAdmin`, `Staff` |
| `description`   | String(256) | Optional         | Role description                     |
| + common fields |             |                  |                                      |

#### role_privilege
| Column          | Type    | Constraints                       | Description         |
| --------------- | ------- | --------------------------------- | ------------------- |
| `id`            | Integer | Primary Key                       | Auto-incremented ID |
| `role_id`       | Integer | Foreign Key → `role.id`, Required | FK to role          |
| `privilege_id`  | Integer | Foreign Key → `privilege.id`, Req | FK to privilege     |
| + common fields |         |                                   |                     |

> Will require UniqueConstraint('role_id', 'privilege_id') to avoid duplicates.

#### user
| Column              | Type        | Constraints                                                        | Description                   |
| ------------------- | ----------- | ------------------------------------------------------------------ | ----------------------------- |
| `id`                | Integer     | Primary Key                                                        | Auto-incremented ID           |
| `first_name`        | String(64)  | Required                                                           | First name                    |
| `last_name`         | String(64)  | Optional                                                           | Last name                     |
| `job_title`         | String(128) | Optional                                                           | e.g., Software Developer      |
| `gender`            | Enum        | Optional (e.g., 'male', 'female', 'other', 'prefer\_not\_to\_say') | Gender identity               |
| `dob`               | Date        | Optional                                                           | Date of birth                 |
| `profile_image_url` | String(512) | Optional                                                           | S3 URL or local file path     |
| `is_active`         | Boolean     | Default: `True`                                                    | Soft disable without deleting |
| `role_id`           | Integer     | Foreign Key → `role.id`, Required                                  | FK to role                    |
| + common fields     |             |                                                                    |                               |

#### user_identity
| Column             | Type        | Constraints                                      | Description                                             |
| ------------------ | ----------- | ------------------------------------------------ | ------------------------------------------------------- |
| `id`               | Integer     | PK, Auto-increment                               | Primary key                                             |
| `user_id`          | Integer     | FK → `user.id`, Not Null, On Delete CASCADE      | Link to owning user                                     |
| `type`             | Enum        | Not Null (`email`, `mobile`, `oauth`)            | Identity type                                           |
| `value`            | String(191) | Not Null, Unique with (`type`, `oauth_provider`) | Email, mobile number, or OAuth UID                      |
| `is_verified`      | Boolean     | Default: `False`, Nullable                       | Email/mobile only                                       |
| `is_primary`       | Boolean     | Default: `False`, Nullable                       | Only for email/mobile — can be used as default identity |
| `oauth_provider`   | String(50)  | Nullable, Required if `type` = `oauth`           | e.g., `google`, `facebook`                              |
| `otp_code`         | String(10)  | Nullable                                         | Last generated OTP (email/mobile only)                  |
| `otp_generated_at` | DateTime    | Nullable                                         | When OTP was generated                                  |
| `wrong_otp_count`  | Integer     | Default: 0                                       | Resets after successful or expired OTP                  |
| `otp_locked_until` | DateTime    | Nullable                                         | Lock cooldown after 3 failed OTP attempts               |
| + common fields     |             |                                                                    |                               |

#### user_auth
| Column                 | Type        | Constraints                                 | Description                            |
| ---------------------- | ----------- | ------------------------------------------- | -------------------------------------- |
| `id`                   | Integer     | PK, Auto-increment                          | Primary Key                            |
| `user_id`              | Integer     | FK → `user.id`, Not Null, On Delete CASCADE | Link to owning user                    |
| `username`             | String(100) | Unique, Nullable                            | Optional username login                |
| `password_hash`        | String(256) | Not Null                                    | Hashed password using bcrypt/argon2    |
| `wrong_password_count` | Integer     | Default: 0                                  | Counts failed attempts                 |
| `account_locked_until` | DateTime    | Nullable                                    | Lock timeout after max failed attempts |
| `last_login_at`        | DateTime    | Nullable                                    | Timestamp of last successful login     |
| + common fields     |             |                                                                    |                               |
