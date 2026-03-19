staff service initiated

# Staff Service - School ERP

Production-ready Non-Teaching Staff Management microservice built with FastAPI and PostgreSQL.

This service handles:

- Non-teaching staff profile lifecycle
- Staff role-linked user provisioning
- Designation and department associations
- Bulk onboarding via Excel
- Staff self-profile and timetable visibility
- Admin-level auditing of create/update/deactivate actions

---

## Overview

Service base URL (local): http://127.0.0.1:8008

API prefix: /staff

Health endpoint: /health

---

## Tech Stack

- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic v2
- SlowAPI (rate limiting)
- TrustedHost + CORS middleware

---

## Security Model

- JWT bearer authentication
- Role-based access control by endpoint
- Roles used by routes: ADMIN, NON_TEACHING_STAFF
- Strict DTO validation with extra field rejection
- Audit log writes for administrative data changes

Role behavior:

- ADMIN: full staff management (create/list/update/deactivate/get-by-id/bulk)
- NON_TEACHING_STAFF: self profile, designation list, timetable read access

---

## Core Features

### 1) Staff Lifecycle Management

- Create non-teaching staff profile
- Auto-create linked auth user
- Auto-assign NON_TEACHING_STAFF role
- List staff with filters and pagination
- Update profile details and status
- Soft deactivate staff account
- Get staff by ID (admin)

### 2) Bulk Staff Onboarding

- Upload .xlsx file for bulk creation
- Max file size: 5 MB
- Max rows: 500
- Required columns validation
- Nested-transaction style row handling for partial success
- Row-level error collection in response

### 3) Designations and Departments

- Uses staff_designations reference table
- Uses departments reference table
- Validates designation and department existence during create/update
- Active designation lookup endpoint

### 4) Staff Self-Service

- Self profile endpoint for logged-in non-teaching staff
- Timetable read endpoint for class-section and term

### 5) Audit Trail

- Best-effort writes to shared audit_logs table
- Logs create/update/deactivate actions with actor and payload snapshot

---

## Main API Endpoints

All routes are under /staff.

### Admin endpoints

- POST /
- POST /bulk
- GET /
- GET /{staff_id}
- PUT /{staff_id}
- DELETE /{staff_id}

### Staff/Admin shared utility endpoints

- GET /designations/list

### Self-service endpoints

- GET /me
- GET /me/timetable

---

## Data Model Highlights

Primary entities:

- non_teaching_staff
- staff_designations

Auth/reference entities:

- users
- roles
- user_roles
- departments
- timetable_entries (read reference)
- academic_terms (read reference)

Important constraints:

- employment_type in: FULL_TIME, PART_TIME, CONTRACT, DAILY_WAGE
- status in: ACTIVE, INACTIVE, TERMINATED, ON_LEAVE
- user linkage uniqueness and FK integrity

---

## API Behavior Notes

- Default list behavior returns ACTIVE staff unless status filter is provided.
- Updating staff status also synchronizes linked auth user is_active state.
- Deactivation is soft-delete style (status -> INACTIVE, deleted_at set).
- Timetable endpoint returns active timetable entries ordered by weekday and period.

---

## Environment Variables

Use .env in this service folder.

- DATABASE_URL
- SECRET_KEY
- ACCESS_TOKEN_EXPIRE_MINUTES
- ALLOWED_ORIGINS
- ALLOWED_HOSTS
- SERVICE_NAME
- INTERNAL_SERVICE_TOKEN
- INTERNAL_SERVICE_NAME
- INTERNAL_ALLOWED_SERVICES

---

## Local Run

Install dependencies:

python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt

Run:

uvicorn main:app --host 0.0.0.0 --port 8000

Typical local mapping for this service is port 8008.

---

## Health Check

GET /health

Response:

{
	"status": "ok",
	"service": "staff_service"
}

---

## Production Checklist

- Set strong secrets and restrict hosts/origins
- Ensure NON_TEACHING_STAFF role exists in roles table
- Ensure designation and department masters are seeded
- Ensure shared audit_logs table is present
- Validate timetable reference tables are available for /me/timetable
- Run integration tests before release