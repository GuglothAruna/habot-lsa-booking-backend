# LSA Booking Backend

**Author:** Gugloth Aruna  
**Email:** arunagugloth7@gmail.com  
**Contact:** 7036807574  
**GitHub:** https://github.com/GuglothAruna/habot-lsa-booking-backend

## Project Overview

A production-oriented Django REST backend prototype for an LSA (Learning Support Assistant) service-booking platform.

The backend connects parents with Learning Support Assistants (LSAs) and provides APIs for:

- LSA search by skill
- Booking creation and validation
- Double-booking prevention
- Payment state management
- Payment webhook processing
- Mock external payment integration
- Automated testing
- OpenAPI/Swagger documentation
- GitHub Actions CI

## Technology Stack

- Python 3.13
- Django 5.2
- Django REST Framework
- PostgreSQL 18
- Django ORM
- pytest
- pytest-django
- requests
- drf-spectacular
- GitHub Actions

## Architecture

```text
                    Client
                      |
                      v
               Django REST API
                      |
        +-------------+-------------+
        |             |             |
        v             v             v
    LSA Search     Booking       Payment
                     API          Webhook
                       |             |
                       +------v------+
                              |
                              v
                         PostgreSQL
