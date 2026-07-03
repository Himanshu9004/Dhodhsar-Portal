# Dhodhsar Gram Vikas Portal

A Flask + MongoDB multi-page portal for village services, grievance submission, admin content management, and local information.

## Project structure

```text
.
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── routes.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── storage.py
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── uploads/
│   └── templates/
│       ├── admin_dashboard.html
│       ├── admin_login.html
│       └── index.html
├── .env.example
├── README.md
├── requirements.txt
├── run.py
```

## Database schema

The app uses MongoDB collections with these document shapes:

- admins: `{ username, password, role, created_at }`
- notices: `{ title, body, created_at }`
- contacts: `{ name, phone, role, created_at }`
- grievances: `{ name, phone, subject, description, status, created_at }`
- mandi_rates: `{ crop, price, unit, updated_at }`
- businesses: `{ name, category, phone, address, approved, created_at }`
- works: `{ title, description, budget_status, image, created_at }`
- schemes: `{ name, description, link, created_at }`
- jobs: `{ title, description, link, created_at }`

## Architecture notes

- The Flask app is initialized from [app/__init__.py](app/__init__.py) and configured through [app/config.py](app/config.py).
- Mongo collections are defined in [app/models.py](app/models.py) and initialized in [app/database.py](app/database.py).
- File uploads are handled by [app/services/storage.py](app/services/storage.py).

## Setup

1. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. Start MongoDB locally.
3. Copy `.env.example` to `.env` and update the connection string.
4. Run the app:
   ```bash
   python run.py
   ```

## Next phase

- Expand the admin dashboard with CRUD forms for notices, mandi rates, schemes, jobs, businesses, and development works.
- Add richer public pages for Krishi Mitra, Digital Panchayat, Sarkari Seva, and Yuva Rojgar.
- Add multilingual content and weather integration in the next iteration.
