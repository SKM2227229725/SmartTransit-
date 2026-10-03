SmartTransit is a web-based intelligent public transport platform 
designed for small cities. It provides:

- Real-time bus tracking
- Stop-based arrival information
- ETA prediction using machine learning
- Route optimization
- Demand forecasting
- Anomaly detection
- Fare calculation
- Authority-side analytics

The project must be a FULLY WORKING web application — not 
documentation, not a UI prototype. Implement frontend, backend, 
database, auth, real-time communication, GPS simulation, ML models, 
analytics, notifications, and deployment configuration.

==================================================
TECH STACK
==================================================

Frontend:   React + Vite + Tailwind CSS + Leaflet + Recharts
Backend:    Python 3.12+ + Django 5.x + Django REST Framework
Database:   PostgreSQL 16
Real-time:  Django Channels + WebSocket + Redis 7
AI/ML:      XGBoost + Prophet + Isolation Forest + Dijkstra/A*
Background: Celery + Celery Beat + Redis
Auth:       SimpleJWT (access + refresh tokens)
Testing:    Pytest + Django TestCase + Postman
Deployment: Docker + Docker Compose + Nginx + Gunicorn
Version:    Git + GitHub

==================================================
MAIN MODULES
==================================================
👤 Passenger
🚌 Driver + GPS Simulator
🏛️ Authority / Admin
📍 Real-time Bus Tracking
🤖 AI ETA Prediction
📊 Demand Forecasting
🚨 Anomaly Detection
🗺️ Route Optimization
💰 Fare Calculation
📈 Analytics & Reports

==================================================
IMPORTANT PROJECT RULE
==================================================
This is an academic prototype for small cities. 
Do NOT claim physical GPS hardware is deployed.
The Driver App SIMULATES GPS by sending vehicle location 
every 5 seconds. The system must be designed so a real GPS 
device can be plugged in later without redesign.

Use realistic demo data (Solapur city area: 17.66°N, 75.90°E).
The entire system must be demonstrable without real buses.

==================================================
USER ROLES
==================================================
1. Passenger
2. Driver
3. Authority / Admin
