# Green Book Bon Voyage
Welcome to the Green Book Bon Voyage project! This application aims to provide users with an interactive platform to explore, review, and mark places as safe or unsafe. It integrates mapping and location services for geocoding and routing, creating a seamless user experience.

Table of Contents
Project Overview
Features
Technology Stack

Usage
API Endpoints



Project Overview
Green Book Bon Voyage is a web application that allows users to:

Register and log in
View and search for places
Mark places as safe or unsafe
Leave reviews for places
View routes and locations on a map

Features
User Authentication (Register, Login, Logout)
Profile Management
Place Listing and Details
Mark Places Safe/Unsafe
Leave and View Reviews
Interactive Map with Geocoding and Routing

Technology Stack

Backend
Flask: Web framework
SQLAlchemy: ORM for database interactions
Flask-Migrate: Database migrations
Flask-SocketIO: Real-time communication
Flask-CORS: Cross-Origin Resource Sharing
Flask-Session: Server-side session management
Flask-RESTful: API creation
Flask-Bcrypt: Password hashing

Frontend
React: JavaScript library for building user interfaces
Axios: HTTP client for making requests

Database
PostgreSQL: Relational database management system

Mapping and Geocoding
Mapbox: Mapping and location services

Usage

Register and Login
Navigate to the registration or login page to create a new account or log in with existing credentials.

View Places
Browse through the list of places or use the search functionality to find specific places.

Mark Places Safe/Unsafe
Click on a place to view its details and use the safety mark feature to mark it as safe or unsafe.

Leave Reviews
Add your review to a place by navigating to its details page and submitting your feedback.

Map Interaction
Use the interactive map to view locations, routes, and get geocoding information.

API Endpoints

Register: /api/register
Login: /api/login
Profile: /api/profile
Places: /api/places
Place By ID: /api/places/<id>
Routes: /api/routes
Safety Marks: /api/safety-marks
Mark Place Safe: /api/safety-marks/<place_id>/mark
Safety Mark By ID: /api/safety-marks/<id>
Reviews: /api/reviews
Review By ID: /api/reviews/<id>

Welcome to Green Book Bon Voyage !


