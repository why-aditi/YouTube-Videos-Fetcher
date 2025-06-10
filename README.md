# YouTube Video Fetcher API

A comprehensive FastAPI application that continuously fetches YouTube videos for specified search queries, stores them in MongoDB, and provides a modern React dashboard for viewing and managing the collected videos.

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Dashboard](#dashboard)

## Features

### Core Features

- **Continuous Video Fetching**: Automatically fetches latest YouTube videos based on configurable search queries
- **Multiple API Key Support**: Implements intelligent quota management with automatic failover between multiple YouTube API keys
- **Scalable Database Design**: Optimized MongoDB schema with proper indexing for fast queries
- **RESTful API**: Comprehensive API endpoints with pagination, filtering, and sorting capabilities
- **Modern React Dashboard**: Responsive web interface built with Vite, Tailwind CSS, and modern UI components
- **Real-time Status Monitoring**: Live system status updates and API quota monitoring

### Advanced Features

- **Smart Quota Management**: Automatically switches between API keys when quota limits are reached
- **Background Task Processing**: Asynchronous video fetching with configurable intervals
- **Comprehensive Filtering**: Search by title, description, channel, date ranges, and more
- **Responsive Design**: Mobile-friendly dashboard that works on all devices
- **Error Handling**: Robust error handling and logging throughout the application
- **CORS Support**: Properly configured for frontend-backend communication

## Architecture

The application follows a modern microservices-inspired architecture with clear separation of concerns:

```
├── Youtube_Video_Fetcher_API/
│   ├── api/                 # API route handlers
│   │   ├── videos.py       # Video-related endpoints
│   │   └── admin.py        # Admin and system endpoints
│   ├── core/               # Core application components
│   │   ├── config.py       # Configuration management
│   │   └── database.py     # Database connection and setup
│   ├── models/             # Data models and schemas
│   │   └── video.py        # Video data models
│   └── services/           # Business logic services
│       ├── youtube_service.py    # YouTube API integration
│       ├── video_service.py      # Video data operations
│       └── background_service.py # Background task management
├── dashboard/              # React frontend application
│   ├── src/
│   │   ├── components/     # React components
│   │   └── services/       # API integration
│   └── public/             # Static assets
├── tests/                  # Test suites
└── docs/                   # Documentation
```

### Technology Stack

**Backend:**

- FastAPI - Modern, fast web framework for building APIs
- MongoDB - NoSQL database for flexible video data storage
- Motor - Asynchronous MongoDB driver for Python
- Pydantic - Data validation and settings management
- Google API Client - YouTube Data API v3 integration

**Frontend:**

- React 18 - Modern JavaScript library for building user interfaces
- Vite - Fast build tool and development server
- Tailwind CSS - Utility-first CSS framework
- Lucide React - Beautiful icon library
- Axios - HTTP client for API communication

## Installation

Follow these steps to install and set up the YouTube Video Fetcher API:

### 1. Clone the Repository

```bash
git clone <repository-url>
cd youtube-video-fetcher
```

### 2. Backend Setup

```bash
# Install Python dependencies
pip3 install -r requirements.txt

# Copy environment configuration
cp .env.example .env

# Edit the .env file with your configuration
nano .env
```

### 3. Frontend Setup

```bash
# Navigate to dashboard directory
cd dashboard

# Install Node.js dependencies
npm install

# Return to project root
npm run dev
```

## Configuration

The application uses environment variables for configuration. All settings are defined in the `.env` file:

### Environment Variables

| Variable                  | Description                                 | Default                     | Required |
| ------------------------- | ------------------------------------------- | --------------------------- | -------- |
| `YOUTUBE_API_KEYS`        | Comma-separated list of YouTube API keys    | -                           | Yes      |
| `SEARCH_QUERY`            | Default search query for fetching videos    | "python programming"        | No       |
| `FETCH_INTERVAL`          | Interval between fetch operations (seconds) | 10                          | No       |
| `MAX_RESULTS_PER_REQUEST` | Maximum videos per API request              | 50                          | No       |
| `MONGODB_URL`             | MongoDB connection string                   | "mongodb://localhost:27017" | No       |
| `DATABASE_NAME`           | MongoDB database name                       | "youtube_videos"            | No       |
| `APP_HOST`                | FastAPI server host                         | "0.0.0.0"                   | No       |
| `APP_PORT`                | FastAPI server port                         | 8000                        | No       |
| `DEBUG`                   | Enable debug mode                           | True                        | No       |
| `SECRET_KEY`              | Application secret key                      | -                           | Yes      |

### Sample Configuration

```env
# YouTube API Configuration
YOUTUBE_API_KEYS=AIzaSyC4K8_your_api_key_1,AIzaSyC4K8_your_api_key_2
SEARCH_QUERY=python programming tutorials
FETCH_INTERVAL=10
MAX_RESULTS_PER_REQUEST=50

# MongoDB Configuration
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=youtube_videos

# Application Configuration
APP_HOST=0.0.0.0
APP_PORT=8000
DEBUG=True

# Security
SECRET_KEY=your-super-secret-key-change-this-in-production
```

### YouTube API Quota Management

The application implements intelligent quota management for YouTube API keys:

- **Daily Quota**: Each API key has 10,000 units per day by default
- **Search Cost**: Each search request costs 100 units
- **Automatic Failover**: When one key exhausts its quota, the system automatically switches to the next available key
- **Quota Reset**: Quotas reset automatically after 24 hours
- **Status Monitoring**: Real-time quota status available through admin endpoints

## Usage

### Starting the Application

#### Development Mode

```bash
# Start the FastAPI backend
python3 main.py

# In a separate terminal, start the React frontend
cd dashboard
npm run dev
```

#### Using the Startup Script

```bash
# Make the script executable (first time only)
chmod +x start.sh

# Start the backend
./start.sh
```

### Accessing the Application

- **API Server**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **React Dashboard**: http://localhost:5173
- **Health Check**: http://localhost:8000/health

## Dashboard

The React dashboard provides a modern, responsive interface for interacting with the YouTube Video Fetcher API.

### Features

#### Video Browsing

- **Grid Layout**: Videos displayed in a responsive card grid
- **Pagination**: Navigate through large collections of videos
- **Thumbnail Preview**: High-quality video thumbnails with duration overlay
- **Video Information**: Title, channel, view count, publish date, and description
- **Direct Links**: Click videos to open them on YouTube

#### Search and Filtering

- **Global Search**: Search across video titles, descriptions, and channel names
- **Advanced Filters**: Filter by channel ID, publish date, and other criteria
- **Real-time Results**: Instant search results as you type
- **Filter Persistence**: Filters remain active during navigation

#### Admin Controls

- **System Status**: Real-time monitoring of background service status
- **API Quota Monitoring**: Track YouTube API usage across multiple keys
- **Manual Operations**: Force video fetches and control background service
- **Statistics Dashboard**: View total videos, latest fetches, and system health

#### Responsive Design

- **Mobile Friendly**: Optimized for smartphones and tablets
- **Touch Support**: Touch-friendly interface elements
- **Adaptive Layout**: Automatically adjusts to screen size
- **Modern UI**: Clean, professional design with smooth animations

### Navigation

The dashboard is organized into several main sections:

1. **Header**: System status indicator and admin controls toggle
2. **Search Bar**: Global search with filter options
3. **Video Grid**: Main content area displaying video cards
4. **Pagination**: Navigation controls for browsing multiple pages
5. **Admin Panel**: System management and monitoring tools

### Customization

The dashboard can be customized by modifying the React components:

- **Styling**: Edit Tailwind CSS classes in component files
- **Layout**: Modify component structure in `src/components/`
- **API Integration**: Update API calls in `src/services/api.js`
- **Configuration**: Adjust settings in `src/config/`
