LSA Booking Backend

Author: Gugloth Aruna
Email: arunagugloth7@gmail.com
GitHub: https://github.com/GuglothAruna/habot-lsa-booking-backend

1. Project Overview

A production-oriented Django REST backend prototype for an LSA (Learning Support Assistant) service-booking platform.

The backend connects parents with Learning Support Assistants (LSAs) and provides APIs for LSA search, booking creation, payment processing, and payment webhook handling.

Key capabilities

LSA search by skill

Booking creation and validation

Double-booking prevention

Payment state management

Payment webhook processing

Mock external payment integration

Automated testing

OpenAPI/Swagger documentation

GitHub Actions CI

2. Technology Stack

Python 3.13

Django 5.2

Django REST Framework

PostgreSQL 18

Django ORM

pytest / pytest-django

requests

drf-spectacular (OpenAPI / Swagger)

GitHub Actions

3. Architecture

Client
   |
   v
Django REST API
   |
   +-----------------------+
   |                       |
   v                       v
LSA Search             Booking API
                           |
                           v
                       PostgreSQL
                           |
                           v
                        Payment
                           |
                           v
                    Payment Webhook

The backend is divided into focused Django applications:

accounts — parent data

lsas — LSA profiles and skills

bookings — booking validation and overlap protection

payments — payment records, mock gateway client, and webhook processing

config — Django configuration and URL routing

4. Project Structure

pythonbackend/
├── .github/
│   └── workflows/
│       └── tests.yml
├── accounts/
├── bookings/
├── config/
├── lsas/
├── payments/
├── conftest.py
├── manage.py
├── pytest.ini
├── requirements.txt
├── README.md
└── .env.example

The real .env file and .venv/ directory are intentionally excluded from Git.

5. Database Design

Main entities

Parent

LSAProfile

Skill

BookingRequest

Payment

Relationships

Parent 1 -------- N BookingRequest N -------- 1 LSAProfile
                                      |
                                      1
                                      |
                                      1
                                   Payment

LSAProfile N -------- N Skill

The schema uses foreign keys, a one-to-one payment relationship, timestamps, status fields, and indexes for common lookup and booking-validation patterns.

Database changes are managed with Django migrations.

6. API Endpoints

Search available LSAs

GET /api/v1/lsas/search/?skill=Autism

Returns active LSAs filtered by skill.

Create a booking

POST /api/v1/bookings/

Validates the requested booking and creates it in PENDING state.

Validation includes:

Parent exists

LSA exists and is active

Start time is in the future

End time is after start time

Requested time does not overlap an active booking for the same LSA

A conflicting booking returns:

409 Conflict

Payment webhook

POST /api/v1/payments/webhook/

Receives payment success/failure events and updates payment and booking states atomically.

API documentation

http://127.0.0.1:8000/api/docs/

Swagger/OpenAPI documentation is generated with drf-spectacular.

7. Double-Booking Protection

Booking creation runs inside a database transaction and locks the selected LSA row before checking for an overlapping booking.

The overlap condition is:

existing.start_time < requested.end_time
AND
existing.end_time > requested.start_time

This allows back-to-back sessions while rejecting overlapping sessions.

Example:

Existing: 10:00 -------- 11:00
New:             10:30 -------- 11:30
                     ❌ Conflict

Existing: 10:00 -------- 11:00
New:                          11:00 -------- 12:00
                                   ✅ Allowed

8. N+1 Query Optimization

The LSA search uses:

prefetch_related("skills")

to fetch related skill data efficiently instead of executing one additional database query for every returned LSA.

An automated test measures the query count and verifies that it remains bounded as the number of LSAs increases.

9. Payment and Webhook Flow

Booking created
      |
      v
Booking PENDING
      |
      v
Payment PENDING
      |
      +------ success ------> Payment SUCCESS
      |                           |
      |                           v
      |                     Booking CONFIRMED
      |
      +------ failure ------> Payment FAILED
                                  |
                                  v
                         Booking PAYMENT_FAILED

The payment integration uses Python requests, a timeout, exception handling, and logging.

The webhook updates payment and booking state inside a database transaction.

Duplicate successful webhook events are handled safely so an already-processed successful payment is not applied again.

10. Automated Testing

The project contains 9 pytest tests covering:

LSA search success

LSA skill filtering

N+1 query behavior

Successful booking

Invalid booking time

Double-booking prevention

Payment success and booking confirmation

Invalid webhook payload

Duplicate webhook handling

Run:

python -m pytest -v

Expected local result:

9 passed

11. Continuous Integration

GitHub Actions runs on pushes and pull requests.

The workflow:

Starts a temporary PostgreSQL service

Installs the Python dependencies

Runs Django system checks

Runs Django migrations

Runs the pytest suite

The workflow is stored at:

.github/workflows/tests.yml

12. Local Setup

Prerequisites

Python 3.13

PostgreSQL 18

Git

Create the virtual environment

py -3.13 -m venv .venv

Activate it:

.venv\Scripts\Activate.ps1

Install dependencies

python -m pip install -r requirements.txt

Create the PostgreSQL database

Create a PostgreSQL database named:

habot_lsa_db

Use the local PostgreSQL postgres user and your own PostgreSQL password.

Configure environment variables

Create .env from .env.example and provide your local secrets.

Example:

POSTGRES_DB=habot_lsa_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password_here
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

SECRET_KEY=change_me
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DEFAULT_SESSION_FEE=500.00

PAYMENT_GATEWAY_URL=http://127.0.0.1:8000/mock-payment/charge/

Never commit .env.

Run migrations

python manage.py migrate

Run the development server

python manage.py runserver

Open Swagger

http://127.0.0.1:8000/api/docs/

13. Security

Database credentials are loaded from environment variables.

.env is excluded from Git.

.venv/ is excluded from Git.

.env.example contains placeholders only.

CI uses a separate temporary PostgreSQL configuration.

Real credentials must never be committed to the public repository.

14. Final API Summary

Method

Endpoint

Purpose

GET

/api/v1/lsas/search/

Search active LSAs by skill

POST

/api/v1/bookings/

Create a validated booking

POST

/api/v1/payments/webhook/

Process payment events

GET

/api/docs/

OpenAPI/Swagger documentation

15. Repository

Public repository:

https://github.com/GuglothAruna/habot-lsa-booking-backend
