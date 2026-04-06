# Finance Tracking API

A robust, enterprise-grade backend developed with **Django** and **Django REST Framework (DRF)** for personal and professional finance management. This project features high-security authentication, granular Role-Based Access Control (RBAC), and advanced financial analytics.

## 🚀 Key Features

*   **Secure Authentication**: Integrated with **JWT (JSON Web Tokens)** via `SimpleJWT` for stateless authentication.
*   **Role-Based Access Control (RBAC)**:
    *   **Admin**: Full system access, including user management and global financial analytics.
    *   **Analyst**: Access to global financial trends and summaries without record modification.
    *   **Viewer**: Personal finance tracking (CRUD) and individual summaries.
*   **Comprehensive Transaction Management**: Seamlessly track Income and Expenses across multiple categories (Salary, Groceries, Rent, etc.).
*   **Dual-Mode Analytics**:
    *   **Personal Mode**: View your own financial health.
    *   **Global Mode**: (Admins/Analysts only) View aggregated system-wide financial data.
*   **Automated Documentation**: Interactive API documentation powered by **Swagger/OpenAPI** (`drf-spectacular`).
*   **Filtering & Pagination**: Advanced filtering by date range, category, and transaction type.

---

## 🛠️ Tech Stack

*   **Backend**: Python, Django 5.0.6, Django REST Framework
*   **Database**: SQLite (Local), PostgreSQL (Production)
*   **Security**: JWT Authentication, CORS Headers
*   **Documentation**: OpenAPI (drf-spectacular)
*   **Environment**: `python-dotenv` for configuration management
*   **Deployment**: Ready for Gunicorn & Whitenoise

---

## 📁 Folder Structure

```text
.
├── finance_project/           # Central Project Configuration
│   ├── settings.py           # Application settings (JWT, DB, Security)
│   ├── urls.py               # Main URL routing (Admin, API, Swagger)
│   └── ...
├── finance_tracker_api/       # Main API Application
│   ├── models.py             # Database Schemas (User, Transaction)
│   ├── views.py              # API Business Logic
│   ├── serializers.py        # Data Validation & Transformation
│   ├── permissions.py        # RBAC Implementation
│   ├── filters.py            # Transaction Filtering Logic
│   ├── tests_*.py            # Extensive Automated Test Suite
│   └── ...
├── .env.example              # Environment Variables Template
├── manage.py                 # Django CLI Utility
├── requirements.txt           # Project Dependencies
├── schema.yml                # Generated OpenAPI Schema
└── build.sh                  # Deployment/Build Script
```

---

## ⚙️ Setup & Installation

### 1. Prerequisites
*   Python 3.10+
*   pip (Python Package Manager)

### 2. Clone & Install
```bash
# Clone the repository
git clone <repository-url>
cd finance-tracking-backend

# Create and activate virtual environment
python -m venv venv
source venv/Scripts/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Configuration
Copy `.env.example` to `.env` and update the values:
```bash
cp .env.example .env
```

### 4. Database Setup
```bash
# Run migrations
python manage.py migrate

# Create a Superuser (Admin)
python manage.py createsuperuser
```

### 5. Run the Server
```bash
python manage.py runserver
```
The API will be available at `http://127.0.0.1:8000/`.

---

## 📖 API Reference

### Authentication
*   **POST** `/api/token/`: Obtain Access & Refresh tokens (Login).
*   **POST** `/api/token/refresh/`: Refresh an expired access token.

### User Management
*   **POST** `/api/users/`: Register a new user.
*   **GET** `/api/users/me/`: Retrieve current user profile.

### Transactions (CRUD)
*   **GET** `/api/transactions/`: List user transactions (supports filtering).
*   **POST** `/api/transactions/`: Create a new transaction.
*   **GET/PUT/PATCH/DELETE** `/api/transactions/{id}/`: Manage specific transaction.

### Analytics & Summaries
*   **GET** `/api/transactions/summary/`: Personal financial breakdown (Total Income/Expense/Balance).
*   **GET** `/api/summary/`: 
    *   **Personal Mode** (Default): Personal analytics.
    *   **Global Mode** (Admin/Analyst): Use `?global=true` for system-wide insights.

### Interactive Documentation
*   **Swagger UI**: `/api/schema/swagger-ui/`
*   **Redoc**: `/api/schema/redoc/`

---

## 🧪 Testing

The project includes as extensive test suite covering RBAC, Analytics, and User Management.
```bash
# Run all tests
python manage.py test finance_tracker_api
```

---

## 📄 License
This project is for educational/internal use.

---
