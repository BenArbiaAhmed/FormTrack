<img width="1836" height="874" alt="Screenshot from 2026-03-30 23-26-52" src="https://github.com/user-attachments/assets/e667dd46-d9fb-47dc-9bfd-d334f167e858" /># 💪 FormTrack

A modern, intelligent fitness tracking application that uses pose estimation technology to monitor and analyze workout performance in real-time. This application leverages computer vision to detect user movements, count repetitions, and provide detailed workout analytics.

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square)
![React](https://img.shields.io/badge/React-19.2-61DAFB?style=flat-square&logo=react)
![FastAPI](https://img.shields.io/badge/FastAPI-0.120-009688?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
<img width="1836" height="874" alt="Screenshot from 2026-03-30 23-26-36" src="https://github.com/user-attachments/assets/cdc255b5-a620-49d4-b4fb-a32ca87f467a" />
<img width="1836" height="874" alt="Screenshot from 2026-03-30 23-26-52" src="https://github.com/user-attachments/assets/306e00b5-2d7f-4cce-adc9-be08273e094b" />



## 📋 Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Project Architecture](#project-architecture)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

- **Real-Time Pose Detection**: Uses MediaPipe to detect and track body poses in real-time
- **Exercise Tracking**: Supports multiple exercise types:
  - Push-ups
  - Squats
  - Tricep dips
- **Automatic Rep Counting**: Intelligent algorithms automatically count exercise repetitions
- **Performance Analytics**: Track workout history, statistics, and progress over time
- **User Authentication**: Secure user accounts with password hashing
- **Audio Feedback**: Real-time audio cues for form corrections
- **Responsive Dashboard**: Beautiful, responsive web interface with workout analytics
- **RESTful API**: Well-documented API endpoints for all functionality
- **Docker Support**: Containerized setup for easy deployment

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI 0.120+
- **Database**: SQLAlchemy with SQLite
- **Pose Detection**: MediaPipe & JAX
- **Authentication**: Argon2 password hashing
- **Server**: Uvicorn with auto-reload
- **Language**: Python 3.11+

### Frontend
- **Framework**: React 19.2
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **UI Components**: Radix UI, shadcn/ui
- **HTTP Client**: Axios
- **Routing**: React Router v7
- **State Management**: React Context API
- **Tables**: TanStack React Table
- **Charts**: Recharts
- **Icons**: Tabler Icons, Lucide React

### DevOps
- **Containerization**: Docker & Docker Compose
- **Development**: Hot-reload with Vite and Uvicorn

## 📁 Project Structure

```
pose-estimation-fitness-tracker/
├── backend/                          # Python FastAPI backend
│   ├── app/
│   │   ├── api/v1/                  # API v1 endpoints
│   │   ├── services/                # Business logic
│   │   │   ├── pose_detector.py     # MediaPipe pose detection
│   │   │   ├── pushup_logic.py      # Push-up counting algorithm
│   │   │   ├── squat_logic.py       # Squat counting algorithm
│   │   │   └── tricep_dips_logic.py # Tricep dips counting algorithm
│   │   ├── models/                  # SQLAlchemy ORM models
│   │   ├── schemas/                 # Pydantic request/response schemas
│   │   ├── db/                      # Database initialization
│   │   ├── exercises/               # Exercise base classes
│   │   ├── utils/                   # Utility functions
│   │   └── middleware/              # CORS and other middleware
│   ├── models/                      # Pre-trained pose landmarker
│   ├── requirements.txt             # Python dependencies
│   └── Dockerfile                   # Docker configuration
│
├── frontend/                         # React Vite frontend
│   ├── src/
│   │   ├── components/              # Reusable React components
│   │   ├── pages/                   # Application pages
│   │   ├── context/                 # React Context providers
│   │   ├── hooks/                   # Custom React hooks
│   │   ├── axios/                   # Axios instance configuration
│   │   └── lib/                     # Utility libraries
│   ├── public/                      # Static assets
│   ├── package.json                 # NPM dependencies
│   └── vite.config.ts              # Vite configuration
│
├── docker-compose.yml              # Docker Compose orchestration
└── README.md                        # This file
```

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.11 or higher**
- **Node.js 16 or higher** (for frontend development)
- **npm or yarn** (package manager)
- **Docker and Docker Compose** (optional, for containerized setup)
- **Git** (for version control)

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/pose-estimation-fitness-tracker.git
cd pose-estimation-fitness-tracker
```

### 2. Backend Setup

```bash
cd backend

# Create and activate a virtual environment (recommended)
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize the database
python -m app.db.init_db

# Generate a secret key for JWT (and add it to .env)
openssl rand -hex 32
# Store this in a .env file as SECRET_KEY=<generated_key>
```

### 3. Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install

# Build TypeScript (optional, for type checking)
npm run build
```

## ⚡ Quick Start

### Running Locally (Development)

**Terminal 1 - Backend Server:**
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn app.main:app --reload
```
The backend API will be available at `http://localhost:8000`

**Terminal 2 - Frontend Development Server:**
```bash
cd frontend
npm run dev
```
The frontend will be available at `http://localhost:5173`

### Running with Docker

```bash
# Build and start all services
docker-compose up --build

# Services will be available at:
# - Frontend: http://localhost:5173
# - Backend API: http://localhost:8000
```

## 🔧 Configuration

### Backend Environment Variables

Create a `.env` file in the `backend` directory:

```env
# Secret key for JWT tokens (generate with: openssl rand -hex 32)
SECRET_KEY=your_generated_secret_key_here

# Database configuration (optional, defaults to SQLite)
DATABASE_URL=sqlite:///./data/db/fitness.db

# API settings
API_VERSION=v1
```

### Frontend Environment Variables

Create a `.env` file in the `frontend` directory:

```env
# Backend API endpoint
VITE_API_URL=http://localhost:8000/api/v1
```

## 📖 Usage

### 1. Create a User Account

Navigate to the Sign Up page and create a new account with your email and password.

### 2. Start a Workout

1. Log in to your dashboard
2. Click "New Workout"
3. Select your exercise type (Push-ups, Squats, or Tricep Dips)
4. Allow camera access
5. Position yourself in front of the camera
6. Begin exercising - the app will automatically count your reps

### 3. View Your Progress

- Dashboard displays recent workout summaries
- View detailed statistics for each exercise type
- Track improvements over time with visual charts

## 📚 API Documentation

### Interactive API Docs

Once the backend is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Key Endpoints

#### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - User login

#### Workouts
- `GET /api/v1/workouts` - Get user's workout history
- `POST /api/v1/workouts` - Create new workout
- `GET /api/v1/workouts/{id}` - Get workout details

#### Exercises
- `GET /api/v1/exercises` - Get available exercise types
- `POST /api/v1/exercises/{type}/analyze` - Analyze exercise from video frame

## 🏗️ Project Architecture

### Backend Architecture

```
Request Flow:
Client → FastAPI Router → Schema Validation → Service Layer → Database

Pose Detection Flow:
Video Frame → MediaPipe PoseLandmarker → Exercise Logic → Rep Count → Response
```

### Key Components

- **PoseDetector**: Handles pose estimation using MediaPipe
- **Exercise Logic**: Exercise-specific algorithms (pushup_logic, squat_logic, etc.)
- **Session Manager**: Manages workout sessions and state
- **Database Layer**: SQLAlchemy models and initialization

### Frontend Architecture

```
User Interface (React Components)
    ↓
Pages (Dashboard, Workouts, etc.)
    ↓
Context API (Authentication, State)
    ↓
Axios HTTP Client
    ↓
FastAPI Backend
```

## 🐛 Troubleshooting

### Camera Not Detected
- Ensure browser has camera permissions
- Check camera is not in use by another application
- Try refreshing the page

### Backend Connection Issues
- Verify backend is running on `http://localhost:8000`
- Check `VITE_API_URL` in frontend `.env` file
- Ensure CORS middleware is enabled

### Database Errors
- Delete existing database: `rm data/db/fitness.db`
- Reinitialize: `python -m app.db.init_db`

## 📦 Dependencies

### Major Backend Dependencies
- FastAPI: Web framework
- MediaPipe: Pose detection
- JAX/JAXLib: Machine learning
- SQLAlchemy: ORM
- Pydantic: Data validation

### Major Frontend Dependencies
- React: UI library
- Vite: Build tool
- Tailwind CSS: Styling
- Radix UI: Component library
- Axios: HTTP client

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

Ahmed

## 🙏 Acknowledgments

- [MediaPipe](https://mediapipe.dev/) for pose detection technology
- [FastAPI](https://fastapi.tiangolo.com/) for the backend framework
- [React](https://react.dev/) for the frontend framework
- Community contributors and testers

## 📞 Support

For support, open an issue on GitHub.

---

**Happy Tracking! 💪**
