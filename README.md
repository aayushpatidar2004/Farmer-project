# Smart Farmer Assistance & Crop Management System

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2-green.svg)](https://www.djangoproject.org/)
[![Django REST Framework](https://img.shields.io/badge/DRF-3.14-red.svg)](https://www.django-rest-framework.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)](https://getbootstrap.com/)
[![MySQL](https://img.shields.io/badge/MySQL-PyMySQL-orange.svg)](https://www.mysql.com/)

A full-stack, production-ready web application built for modern agricultural management. Features crop cycle tracking, soil analysis, data-driven crop recommendations via Pandas/NumPy, live weather forecasts via Open-Meteo, crop disease remedies with safety protocols, and market price tracking.

**Live demo:** [Smart Farmer on Vercel](https://farmer-project-1dl6.vercel.app/)

---

## Architecture & Technology Stack

| Layer | Technology |
|---|---|
| **Backend Framework** | Python 3, Django 4.2 |
| **REST API** | Django REST Framework (DRF) |
| **Database** | MySQL (connected via pure-Python `PyMySQL` driver) |
| **Data Processing & Analytics** | Pandas, NumPy |
| **External Weather API** | Open-Meteo API (100% Free, No API Key Required) |
| **Frontend UI** | HTML5, CSS3, Bootstrap 5, Vanilla JavaScript, Bootstrap Icons |
| **Authentication** | Django Auth System (PBKDF2 Password Hashing, Role-Based Access) |

---

## Key Modules & Features

1. **Farmer Authentication & Profiles**:
   - Secure registration, login, logout, and profile management.
   - Dual roles: **Farmer** and **Admin**.

2. **Crop Management (CRUD)**:
   - Record sown crops, crop category, variety, sowing date, expected harvest date, land area, soil type, and irrigation method.
   - Upload and attach crop health images.
   - Filter and search crops by status (Planned, Growing, Ready for Harvest, Harvested).

3. **Open-Meteo Weather Dashboard**:
   - Live location weather lookup (Temperature, Humidity, Wind Speed, Rainfall/Precipitation, Pressure).
   - Completely free with graceful error handling for timeouts or invalid locations.

4. **Soil Information & Health Analysis**:
   - Enter soil sample data: pH, Nitrogen (N), Phosphorus (P), Potassium (K), Moisture, Organic Matter.
   - NumPy-based nutrient adequacy index calculation.

5. **Crop Recommendation Engine**:
   - Weighted multi-parameter matching algorithm built with Pandas & NumPy.
   - Ranks top 5 suitable crops based on soil chemistry (NPK, pH) and environmental inputs.

6. **Crop Disease & Remedy Database**:
   - Comprehensive searchable database of crop diseases, symptoms, causes, preventive practices, and chemical/organic pesticide treatments.

7. **Agricultural Market Prices**:
   - Search and filter crop commodity prices across mandis and locations.

8. **Django REST Framework API**:
   - Full REST endpoints for Crops, Profile, Diseases, Market Prices, Weather, and Recommendations.

---

## Installation & Local Setup

### 1. Prerequisites
- Python 3.10+ installed
- MySQL Server running locally or accessible remotely

### 2. Clone / Navigate to Directory
```bash
cd smart_farmer
```

### 3. Create & Activate Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Environment Configuration
Copy `.env.example` to `.env` and fill in your MySQL credentials:
```env
SECRET_KEY=django-insecure-smart-farmer-dev-key-2026
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=smart_farmer_db
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
```

### 6. Create MySQL Database
Run in your MySQL terminal / workbench:
```sql
CREATE DATABASE smart_farmer_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 7. Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 8. Load Sample / Demo Data
Load pre-populated crop diseases, pesticides, and market prices:
```bash
python manage.py load_sample_data
```

### 9. Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

### 10. Run Development Server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your browser.

---

## REST API Endpoint Reference

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `GET` | `/api/profile/` | Fetch authenticated user's profile | Yes |
| `GET` / `POST` | `/api/crops/` | List or create farmer crops | Yes |
| `GET` / `PUT` / `DELETE` | `/api/crops/<id>/` | Retrieve, update or delete a crop | Yes (Owner) |
| `GET` | `/api/diseases/` | Search disease database (`?search=rice&crop=rice`) | Yes |
| `GET` | `/api/market-prices/` | Filter market prices (`?crop_name=wheat`) | Yes |
| `POST` | `/api/recommendation/` | Generate crop recommendations from JSON input | Yes |
| `GET` | `/api/weather/?city=Delhi` | Get live Open-Meteo weather JSON | Yes |

---

## Running Automated Tests

```bash
python manage.py test
```

---

## Deploy on Render (Free Tier)

1. Push this repository to GitHub and create a free PostgreSQL database with a provider such as Neon. Render's free web service does not include a persistent disk, so SQLite is not suitable for production data.
2. In Render, choose **New > Blueprint** and connect the repository. The included `render.yaml` creates the free web service.
3. In the web service environment settings, set `DATABASE_URL` to the database provider's pooled or direct PostgreSQL connection URL. Render will generate `SECRET_KEY` and set `DEBUG=False`.
4. In the Render environment settings, set `CLOUDINARY_URL` to the Cloudinary URL from your Cloudinary dashboard (`cloudinary://API_KEY:API_SECRET@CLOUD_NAME`). Keep this value secret.
5. Deploy. Static files are collected during build and database migrations run when the service starts. Upload plant photos again after Cloudinary is configured; files previously stored on Render's temporary disk are not copied automatically.

The free web service may sleep when idle. Cloudinary stores uploaded plant photos independently of Render's temporary filesystem.

## Deploy on Vercel

1. Import this GitHub repository in Vercel. Keep the **Root Directory** as `./` and choose the **Django** preset. Vercel detects `manage.py` automatically; leave the Build Command and Output Directory at their defaults.
2. Add these project environment variables for **Production** and **Preview**:
   - `SECRET_KEY`: a new long, random Django secret.
   - `DEBUG`: `False`.
   - `DATABASE_URL`: a persistent PostgreSQL connection URL (the same external database used by Render can be reused if it accepts Vercel connections).
   - `CLOUDINARY_URL`: optional, but required for uploaded plant photos to persist between function invocations.
3. Deploy. Vercel provides a separate `*.vercel.app` URL; it does not reuse the Render URL. The app accepts Vercel deployment hosts and trusts their HTTPS origins automatically.

Vercel runs Django as a serverless function, so do not use the local SQLite database for production. Run `python manage.py migrate` against the configured production database once before first use. Vercel serves collected static files from its CDN automatically.

---

## Disclaimer

*Recommendations and disease treatment data provided in this application are for informational and demonstration purposes only. Farmers should consult qualified local agricultural extension officers before making critical farming decisions.*
