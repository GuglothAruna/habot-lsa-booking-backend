# LSA Booking Backend

Production-oriented Python backend prototype for an LSA service booking platform.

## Overview

This backend connects parents with Learning Support Assistants (LSAs) and provides APIs for LSA search, booking, payment processing, and payment webhook handling.

## Technology Stack

- Python 3.13
- Django 5.2
- Django REST Framework
- PostgreSQL 18
- Django ORM
- pytest
- requests
- OpenAPI / Swagger
- GitHub Actions

## Architecture

Parent
↓
Django REST API
↓
LSA Search / Booking / Payment Webhook
↓
PostgreSQL

## Main APIs

### LSA Search

`GET /api/v1/lsas/search/?skill=Autism`

### Create Booking

`POST /api/v1/bookings/`

### Payment Webhook

`POST /api/v1/payments/webhook/`

### API Documentation

`GET /api/docs/`

## Database Design

Main entities:

- Parent
- LSAProfile
- Skill
- BookingRequest
- Payment

Relationships:

- Parent → BookingRequest
- LSAProfile → BookingRequest
- LSAProfile ↔ Skill
- BookingRequest → Payment

## Booking Protection

The booking API validates:

- Parent
- Active LSA
- Future start time
- End time after start time
- Overlapping sessions

Overlapping sessions return HTTP 409 Conflict.

Booking creation uses a database transaction and row locking to improve concurrency safety.

## N+1 Query Optimization

LSA search uses Django ORM `prefetch_related()` for related skills.

This prevents a separate database query from being executed for every returned LSA.

Automated tests verify that the query count remains bounded.

## Payment Flow

New bookings start as:

`PENDING`

Payment success:

`PENDING → CONFIRMED`

Payment failure:

`PENDING → PAYMENT_FAILED`

The webhook uses transactional processing and duplicate-success protection.

## Testing

The project contains automated pytest coverage for:

- LSA search
- Skill filtering
- N+1 query behavior
- Successful booking
- Invalid booking
- Double-booking prevention
- Payment success
- Invalid webhook
- Duplicate webhook

## CI/CD

GitHub Actions automatically:

1. Starts PostgreSQL
2. Installs dependencies
3. Runs Django checks
4. Runs database migrations
5. Runs pytest

## Local Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver