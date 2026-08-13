# LSA Booking Backend

**Author:** Gugloth Aruna  
**Email:** arunagugloth7@gmail.com  
**Contact:** 7036807574  
**GitHub:** https://github.com/GuglothAruna/habot-lsa-booking-backend

## Project Overview

A production-oriented Django REST backend prototype for an LSA service booking platform.

The platform connects parents with Learning Support Assistants (LSAs) for children with learning difficulties.

## Technology Stack

- Python 3.13
- Django 5.2
- Django REST Framework
- PostgreSQL 18
- Django ORM
- pytest
- requests
- drf-spectacular
- GitHub Actions

## Architecture

```text
Parent
  |
  v
Django REST API
  |
  +-------------------+
  |                   |
  v                   v
LSA Search         Booking API
                      |
                      v
                  PostgreSQL
                      |
                      v
                   Payment
                      |
                      v
              Payment Webhook
