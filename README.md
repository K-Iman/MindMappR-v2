# MindMappR

MindMappR is a web-based mental wellness application built with Django. It provides users with simple mental health self-assessment tools, progress tracking, and helpful resources to improve self-awareness over time.

---

## Features

### 1. User Authentication
- Sign up, login, and logout functionality
- Username-based accounts
- Secure session handling

### 2. Depression Assessment System
Two levels of assessment:
- **Quick Test**: Short screening based on 2 core questions (PHQ-2 style)
- **Deep Test**: Detailed assessment based on 9 core symptom questions (PHQ-9 style)

Each test provides:
- A score
- A risk level (low, moderate, high or severity scale)
- Instant feedback based on responses

### 3. Progress Tracking
- Stores past assessment results per user
- Displays progress over time
- Visual graph representation of mood/risk trends

### 4. Mental Health Resources
- Educational content and support guidance
- Simple, accessible explanations

### 5. Modern UI
- Responsive design for desktop and mobile
- Light mode (white + green theme)
- Dark mode (black + green theme)
- Smooth animations and modern layout system

---

## Tech Stack

- Backend: Django
- Frontend: HTML, CSS, JavaScript
- Database: SQLite (development), PostgreSQL (production)
- Deployment: Render
- Visualization: Chart.js (for progress graphs)
- ML (legacy/optional): Scikit-learn (if enabled)

---

## Project Structure
