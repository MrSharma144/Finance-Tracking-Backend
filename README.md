# Finance Tracking Backend
A robust, enterprise-grade financial data management API built with **Django 5.0** and **Django REST Framework (DRF)**. The system features a strictly enforced three-tier Role-Based Access Control (RBAC) system—Admin, Analyst, and Viewer—designed to protect sensitive financial data while providing powerful analytical insights.

Built with a focus on **security-first architecture**, this project demonstrates modern backend engineering patterns including stateless JWT authentication, granular permission layers, automated API documentation, and SQL-optimized financial aggregation.

---

## 💎 Why This Project?
Financial systems are high-stakes environments where data leaks are unacceptable. This backend solves the core challenges of fintech platforms:

1.  **Multi-User Isolation**: Every request is scoped. Viewers see only their data, while the database-level filtering ensures that a "Viewer" cannot access an "Analyst's" records even with a direct ID.
2.  **Granular RBAC**: Permissions are not global toggles; they are applied at the route, object, and field levels. 
3.  **Aggregation Performance**: Advanced summaries and breakdowns (e.g., month-over-month trends, category splits) are calculated directly in the database layer using Django's powerful aggregation engine, ensuring scalability as transaction counts grow.

---

## 🔥 Features
### 🔐 Authentication & User Management
*   **JWT Integration**: Stateless authentication using `SimpleJWT` (Bearer tokens).
*   **Self-Registration**: Open registration for new users with default `Viewer` role.
*   **Profile Access**: Dedicated `/api/users/me/` endpoint for current user context.
*   **Admin Control**: Only Admins can list all users or modify user roles and account statuses.

### 💰 Financial Record Management (CRUD)
*   **Transaction Lifecycle**: Full support for Income and Expense records with categorization.
*   **Advanced Filtering**: Filter by date range, transaction type, and category using `django-filter`.
*   **Role-Specific Logic**: 
    *   **Viewers**: Can Create/Read their own transactions.
    *   **Analysts**: Can Create/Read/Update/Delete their own, and View all others.
    *   **Admins**: Full CRUD access system-wide.

### 📊 Dashboard & Analytics
*   **Dual-Mode Summary**: One endpoint (`/api/summary/`) that intelligently toggles between **Personal** and **Global** modes based on permissions and query flags (`?global=true`).
*   **Category Breakdown**: Real-time aggregation of spending/income per category (Salary, Groceries, Rent, etc.).
*   **Financial Health**: Instant calculation of total income, total expense, and net balance.

---

## 🛠️ Tech Stack
| Layer | Technology | Rationale |
| :--- | :--- | :--- |
| **Framework** | Django 5.0.6 + DRF | "Batteries-included" security, robust ORM, and enterprise-grade scalability. |
| **Authentication** | JWT (SimpleJWT) | Stateless, scalable, and cross-platform compatible (Web/Mobile). |
| **Database** | SQLite / PostgreSQL | SQLite for zero-config local dev; PostgreSQL ready for high-concurrency production. |
| **Documentation** | drf-spectacular | Industry-standard OpenAPI 3.0 specs with Swagger UI integration. |
| **Security** | Python-Dotenv | Secure management of secrets and environment variables. |

---

## 🏗️ Architecture & Design
### Project Structure
```text
Finance Tracking Backend/
├── finance_project/          # Project Settings & Routing
│   ├── settings.py           # JWT, Security, and App Config
│   └── urls.py               # Main URL entrance (Schema, Swagger, API)
├── finance_tracker_api/      # Core Business Logic
│   ├── models.py             # CustomUser (RBAC) & Transaction Schemas
│   ├── views.py              # API logic & Query Sets
│   ├── serializers.py        # Input Validation & JSON conversion
│   ├── permissions.py        # Granular RBAC Permission Classes
│   ├── filters.py            # Transaction Search & Filtering logic
│   └── tests_*.py            # Extensive Automated Test Suite
├── .env.example              # Environment Configuration Template
├── requirements.txt          # Python Dependencies
└── schema.yml                # Generated OpenAPI Specification
```

### Request Lifecycle
1.  **Request Entrance**: Hits Django Middleware (CORS, Security, Auth).
2.  **JWT Authentication**: `JWTAuthentication` extracts the Bearer token and injects the `request.user`.
3.  **RBAC Gatekeeping**: Custom permission classes (`IsAdmin`, `IsOwnerOrAdmin`) check the user's role against the endpoint requirements.
4.  **Query Filtering**: `get_queryset()` ensures users can only access records they are authorized to see (Horizontal Privilege Escalation prevention).
5.  **Validation**: Serializers sanitize and validate inputs before they reach the database.
6.  **JSON Response**: Results returned with appropriate HTTP codes (201 Created, 403 Forbidden, etc.).

---

## 🕹️ API Endpoints & Access Control
### Permission Matrix
| Endpoint | Viewer | Analyst | Admin |
| :--- | :---: | :---: | :---: |
| **GET /api/users/** | ❌ | ❌ | ✅ |
| **GET /api/users/me/** | ✅ | ✅ | ✅ |
| **POST /api/transactions/** | ✅ | ✅ | ✅ |
| **GET /api/transactions/** | Own Only | All | All |
| **DELETE /api/transactions/{id}/** | ❌ | Own Only | ✅ |
| **GET /api/summary/?global=true** | ❌ | ✅ | ✅ |

### Key Endpoints Reference
*   **Authentication**:
    *   `POST /api/token/`: Obtain Access/Refresh tokens.
    *   `POST /api/token/refresh/`: Renew expired tokens.
*   **Dashboard**:
    *   `GET /api/summary/`: Personal financial summary.
    *   `GET /api/summary/?global=true`: System-wide analytics (Admin/Analyst).
*   **Interactive Docs**:
    *   `GET /api/docs/`: Swagger UI for interactive testing.

---

## 🚀 Setup & Testing
### Prerequisites
*   Python 3.10+
*   Virtual Environment (venv)

### Installation
1.  **Clone & Enter**:
    ```bash
    git clone <repo-url>
    cd finance-tracking-backend
    ```
2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Environment Setup**:
    Copy `.env.example` to `.env` and configure your `SECRET_KEY`.
4.  **Initialize Database**:
    ```bash
    python manage.py migrate
    ```
5.  **Run Server**:
    ```bash
    python manage.py runserver
    ```

### 🧪 Quick Test (Demo Credentials)
You can use the pre-configured admin account to test all features:
*   **Username**: `admin`
*   **Password**: `admin` (Use `createsuperuser` if not seeded).

**How to authenticate in Swagger UI**:
1.  Call `POST /api/token/` with the admin credentials.
2.  Copy the `access` token.
3.  Click the **"Authorize"** button at the top right of the Swagger UI (`/api/docs/`).
4.  Enter `Bearer <your_token>` and click Authorize.

---

## 🛡️ Security & Scalability
### Security Measures
*   **SQL Injection Prevention**: All records are accessed via Django ORM using parameterized queries.
*   **Password Hashing**: Uses Django's PBKDF2 hashing algorithm (industry standard).
*   **Environment Isolation**: Secrets are kept out of source control via `.env`.
*   **Soft Logic**: Critical endpoints use `queryset` scoping to ensure a user can never "guess" a transaction ID of another user.

### Scalability Roadmap
*   **PostgreSQL**: Built-in support for PG for handling high-throughput production workloads.
*   **Caching**: Ready for Redis integration to cache heavy global analytics summaries.
*   **Background Tasks**: Architecture allows for Easy integration of Celery for monthly PDF report generation.

---
*Created as a demonstration of high-quality backend engineering with Django.*
