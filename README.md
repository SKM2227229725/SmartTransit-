# 🚌 SmartTransit

<<<<<<< HEAD
**AI-Powered Real-Time Public Transport Tracking for Small Cities**
=======
- Real-time bus tracking
- Stop-based arrival information
- ETA prediction using machine learning
- Route optimization
- Demand forecasting
- Anomaly detection
- Fare calculation acc to distance 
- Authority-side analytics
>>>>>>> f08b04514580c07976a0ddf01bb7ef1dfe8c8eb2

[![Django](https://img.shields.io/badge/Django-5.0.6-092E20?style=flat-square&logo=django)](https://djangoproject.com)
[![DRF](https://img.shields.io/badge/DRF-3.15-ff1709?style=flat-square)](https://django-rest-framework.org)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=flat-square&logo=react)](https://react.dev)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=flat-square&logo=postgresql)](https://postgresql.org)
[![Redis](https://img.shields.io/badge/Redis-7-DC382D?style=flat-square&logo=redis)](https://redis.io)
[![Celery](https://img.shields.io/badge/Celery-5-37814A?style=flat-square&logo=celery)](https://celeryq.dev)

> Production-grade, fully working academic project — no prototypes, no placeholders.

---

## 🎯 Problem

Small Indian cities lack real-time bus tracking. Commercial GPS hardware costs ₹8–15 lakh/year. Google Maps ignores Tier-2 cities.

## 💡 Solution

**SmartTransit** turns any driver's smartphone into a GPS beacon — live tracking for passengers, dispatch for drivers, analytics for authorities. **Zero hardware cost.**

---

## ✨ Features

| Role | Capabilities |
|------|-------------|
| 👤 **Passenger** | Live map · ML ETA · Fare calculator · Notifications · Route browse |
| 🚌 **Driver** | Trip lifecycle · GPS simulator (5-sec pings) · Prevent dual trips |
| 🏛️ **Authority** | Fleet CRUD · Live ops map · Analytics · Anomaly resolve · CSV/PDF reports |

### AI/ML
- **ETA** — XGBoost regression
- **Demand** — Prophet (24h + 7d)
- **Anomaly** — Isolation Forest (speed, deviation, inactivity)
- **Route** — Dijkstra / A*

### Server-Side Business Rules
- One active trip per driver (transaction-safe)
- Fare computed on backend (`base + distance × rate`)
- Append-only audit log
- Role-scoped DRF permissions
- Real-GPS plug-in ready (`source: simulator | device`)

---

## 🏛️ Architecture
