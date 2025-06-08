# AWS Mini Web App – Marvel/DC Movie Manager

A web application that allows users to browse, add, and manage a collection of Marvel and DC superhero movies.

---

## 🗂 Overview

This project is a full-stack application built using a modern frontend and a Python Flask backend with PostgreSQL integration. It demonstrates how to combine multiple AWS services to deploy a fully functioning web app.

---

## 🔧 Features

* View a list of Marvel and DC superhero movies
* Sort movies by ID, title, year, genre, runtime, and IMDb score
* Add new movies to the database
* Delete existing movies
* Responsive UI for desktop and mobile devices

---

## 💻 Tech Stack

### Frontend

* HTML5
* CSS3
* Vanilla JavaScript

### Backend

* Python 3
* Flask web framework
* PostgreSQL
* Flask-CORS for handling cross-origin requests

---

## ☁ Deployment

### Frontend Hosting

* Hosted on **AWS S3** as a static website
* Public access enabled via S3 static site hosting
* Provides scalable and highly available delivery for the frontend

### Backend Services

* Flask app hosted on an **AWS EC2** instance, exposed on port `5000`
* PostgreSQL database hosted on **AWS RDS**

### Database

* PostgreSQL schema includes:

  * Title
  * Year
  * Genre
  * Runtime
  * IMDb score

---

## 🏗 Project Structure

```
AWS-Mini-Web-App/
├── static/
│   └── index.html           # Frontend (HTML/CSS/JS)
├── app.py                   # Flask backend API
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

---

## 🔌 Deployment Architecture

This app uses several AWS services to provide a production-like environment:

* **Amazon S3** – Hosts the frontend (HTML, CSS, JavaScript) as a static site
* **Amazon EC2** – Runs the Flask backend, handles HTTP requests and connects to the database
* **Amazon RDS** – Hosts a managed PostgreSQL database containing movie data

Security groups are configured to:

* Allow traffic between EC2 and RDS
* Expose EC2’s API port for client access
* Enable S3 frontend to call the EC2 API via CORS

---

## 🎬 Data Source

* Movie data inspired by **Marvel** and **DC Comics** superhero franchises
* IMDb scores and metadata referenced from public movie databases

---
