# YouTube Video Fetcher API

A comprehensive FastAPI application that continuously fetches YouTube videos for specified search queries, stores them in MongoDB, and provides a modern React dashboard for viewing and managing the collected videos.

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Dashboard](#dashboard)
- [Deployment](#deployment)
- [Development](#development)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

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

**Development & Deployment:**

- Python 3.11+ - Modern Python runtime
- Node.js 20+ - JavaScript runtime for frontend
- Docker - Containerization (optional)
- MongoDB Atlas - Cloud database option

## Prerequisites

Before installing the YouTube Video Fetcher API, ensure you have the following prerequisites installed and configured:

### System Requirements

- Python 3.11 or higher
- Node.js 20.0 or higher
- MongoDB 6.0 or higher (local installation or MongoDB Atlas)
- Git for version control

### YouTube API Setup

1. Create a Google Cloud Project at [Google Cloud Console](https://console.cloud.google.com/)
2. Enable the YouTube Data API v3 for your project
3. Create API credentials (API Key) with YouTube Data API v3 access
4. Note the quota limits: 10,000 units per day per API key by default
5. (Optional) Create multiple API keys for higher quota limits

### MongoDB Setup

Choose one of the following options:

**Option 1: Local MongoDB Installation**

- Install MongoDB Community Edition from [MongoDB Download Center](https://www.mongodb.com/try/download/community)
- Start MongoDB service: `sudo systemctl start mongod`
- Verify installation: `mongo --version`

**Option 2: MongoDB Atlas (Cloud)**

- Create a free account at [MongoDB Atlas](https://www.mongodb.com/atlas)
- Create a new cluster
- Configure network access and database user
- Get the connection string

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
cd ..
```

### 4. Database Setup

If using local MongoDB, ensure it's running:

```bash
# Start MongoDB (Ubuntu/Debian)
sudo systemctl start mongod

# Verify MongoDB is running
sudo systemctl status mongod
```

### 5. Verify Installation

Run the test suite to verify everything is working:

```bash
python3 tests/test_api.py
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

### Basic Operations

#### Fetching Videos

The application automatically starts fetching videos when launched. You can also trigger manual fetches:

```bash
# Using curl
curl -X POST http://localhost:8000/api/admin/background/force-fetch

# Using the dashboard
# Navigate to the admin panel and click "Force Fetch"
```

#### Viewing Videos

Access the React dashboard at http://localhost:5173 to:

- Browse fetched videos with pagination
- Search videos by title, description, or channel
- Filter videos by date, channel, or other criteria
- View video statistics and metadata
- Click videos to open them on YouTube

#### Managing the System

Use the admin panel in the dashboard or API endpoints to:

- Start/stop background fetching
- Monitor API quota status
- View system statistics
- Force manual video fetches

## API Documentation

The YouTube Video Fetcher API provides comprehensive RESTful endpoints for managing videos and system operations.

### Base URL

```
http://localhost:8000/api
```

### Authentication

Currently, the API does not require authentication for read operations. Admin operations are available without authentication in development mode.

### Video Endpoints

#### GET /api/videos/

Retrieve paginated videos with optional filtering and sorting.

**Parameters:**

- `page` (int, optional): Page number (default: 1)
- `per_page` (int, optional): Items per page (default: 20, max: 100)
- `search` (string, optional): Search term for title, description, or channel
- `channel_id` (string, optional): Filter by specific channel ID
- `published_after` (datetime, optional): Filter videos published after this date
- `published_before` (datetime, optional): Filter videos published before this date

**Response:**

```json
{
  "videos": [
    {
      "video_id": "dQw4w9WgXcQ",
      "title": "Rick Astley - Never Gonna Give You Up",
      "description": "The official video for Rick Astley's 'Never Gonna Give You Up'",
      "published_at": "2009-10-25T06:57:33Z",
      "channel_id": "UCuAXFkgsw1L7xaCfnd5JJOw",
      "channel_title": "Rick Astley",
      "thumbnails": {
        "high": {
          "url": "https://i.ytimg.com/vi/dQw4w9WgXcQ/hqdefault.jpg",
          "width": 480,
          "height": 360
        }
      },
      "view_count": 1000000,
      "like_count": 50000,
      "comment_count": 10000,
      "tags": ["music", "pop", "80s"],
      "duration": "PT3M33S"
    }
  ],
  "total": 150,
  "page": 1,
  "per_page": 20,
  "total_pages": 8
}
```

#### GET /api/videos/latest

Get the most recently published videos.

**Parameters:**

- `limit` (int, optional): Number of videos to return (default: 10, max: 50)

#### GET /api/videos/stats

Get basic statistics about stored videos.

**Response:**

```json
{
  "total_videos": 1500,
  "latest_video": {
    "video_id": "abc123",
    "title": "Latest Video Title",
    "published_at": "2024-01-15T10:30:00Z"
  }
}
```

#### GET /api/videos/{video_id}

Get detailed information about a specific video.

### Admin Endpoints

#### GET /api/admin/status

Get comprehensive system status including background service and API quota information.

**Response:**

```json
{
  "background_service": {
    "is_running": true,
    "last_fetch_time": "2024-01-15T10:30:00Z",
    "fetch_count": 145,
    "error_count": 2,
    "fetch_interval": 10,
    "search_query": "python programming"
  },
  "youtube_api": {
    "total_keys": 3,
    "available_keys": 2,
    "exhausted_keys": 1,
    "current_key_index": 1
  },
  "system": {
    "status": "healthy"
  }
}
```

#### POST /api/admin/background/start

Start the background video fetching service.

#### POST /api/admin/background/stop

Stop the background video fetching service.

#### POST /api/admin/background/force-fetch

Trigger an immediate video fetch operation.

#### GET /api/admin/youtube/quota

Get detailed YouTube API quota status for all configured keys.

### Error Responses

The API uses standard HTTP status codes and returns detailed error information:

```json
{
  "detail": "Error description",
  "status_code": 400
}
```

Common status codes:

- `200`: Success
- `400`: Bad Request
- `404`: Not Found
- `422`: Validation Error
- `500`: Internal Server Error

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

## Deployment

The YouTube Video Fetcher API can be deployed in various environments, from development to production.

### Development Deployment

For development and testing purposes:

```bash
# Start MongoDB (if using local installation)
sudo systemctl start mongod

# Start the FastAPI backend
python3 main.py

# Start the React frontend (in a separate terminal)
cd dashboard
npm run dev
```

### Production Deployment

#### Option 1: Traditional Server Deployment

**1. Prepare the Server**

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install Python 3.11+
sudo apt install python3.11 python3.11-pip python3.11-venv

# Install Node.js 20+
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install MongoDB
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org
```

**2. Deploy the Application**

```bash
# Clone the repository
git clone <repository-url> /opt/youtube-video-fetcher
cd /opt/youtube-video-fetcher

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Build the frontend
cd dashboard
npm install
npm run build
cd ..

# Configure environment
cp .env.example .env
# Edit .env with production settings
```

**3. Configure Services**
Create systemd service files for automatic startup:

```bash
# Create backend service
sudo nano /etc/systemd/system/youtube-fetcher-api.service
```

```ini
[Unit]
Description=YouTube Video Fetcher API
After=network.target mongodb.service

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/youtube-video-fetcher
Environment=PATH=/opt/youtube-video-fetcher/venv/bin
ExecStart=/opt/youtube-video-fetcher/venv/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start services
sudo systemctl daemon-reload
sudo systemctl enable youtube-fetcher-api
sudo systemctl start youtube-fetcher-api
```

#### Option 2: Docker Deployment

**1. Create Dockerfile for Backend**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "main.py"]
```

**2. Create Dockerfile for Frontend**

```dockerfile
FROM node:20-alpine as build

WORKDIR /app
COPY dashboard/package*.json ./
RUN npm install

COPY dashboard/ .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
```

**3. Docker Compose Configuration**

```yaml
version: "3.8"

services:
  mongodb:
    image: mongo:6.0
    restart: always
    volumes:
      - mongodb_data:/data/db
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: password

  api:
    build: .
    restart: always
    ports:
      - "8000:8000"
    environment:
      - MONGODB_URL=mongodb://admin:password@mongodb:27017/youtube_videos?authSource=admin
    depends_on:
      - mongodb

  dashboard:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    restart: always
    ports:
      - "80:80"
    depends_on:
      - api

volumes:
  mongodb_data:
```

#### Option 3: Cloud Deployment

**MongoDB Atlas Setup**

1. Create a MongoDB Atlas account
2. Create a new cluster
3. Configure network access (add your server's IP)
4. Create a database user
5. Get the connection string and update `MONGODB_URL` in `.env`

**Heroku Deployment**

```bash
# Install Heroku CLI
# Create Heroku app
heroku create youtube-video-fetcher

# Set environment variables
heroku config:set YOUTUBE_API_KEYS=your_api_keys
heroku config:set MONGODB_URL=your_mongodb_atlas_url

# Deploy
git push heroku main
```

**AWS/GCP/Azure Deployment**

- Use container services (ECS, Cloud Run, Container Instances)
- Set up managed MongoDB (DocumentDB, MongoDB Atlas)
- Configure load balancers and auto-scaling
- Set up monitoring and logging

### Environment-Specific Configuration

#### Development

```env
DEBUG=True
APP_HOST=127.0.0.1
MONGODB_URL=mongodb://localhost:27017
```

#### Production

```env
DEBUG=False
APP_HOST=0.0.0.0
MONGODB_URL=mongodb://username:password@host:port/database
SECRET_KEY=your-production-secret-key
```

### Security Considerations

For production deployments:

1. **Environment Variables**: Never commit API keys or secrets to version control
2. **Database Security**: Use authentication and encryption for MongoDB
3. **HTTPS**: Configure SSL/TLS certificates for secure communication
4. **Firewall**: Restrict access to necessary ports only
5. **Updates**: Keep all dependencies and system packages updated
6. **Monitoring**: Set up logging and monitoring for security events
7. **Backup**: Implement regular database backups

### Performance Optimization

For high-traffic deployments:

1. **Database Indexing**: Ensure proper MongoDB indexes are created
2. **Connection Pooling**: Configure appropriate connection pool sizes
3. **Caching**: Implement Redis caching for frequently accessed data
4. **Load Balancing**: Use multiple API instances behind a load balancer
5. **CDN**: Serve static assets through a Content Delivery Network
6. **Monitoring**: Set up performance monitoring and alerting

## Development

This section provides information for developers who want to contribute to or extend the YouTube Video Fetcher API.

### Development Setup

#### Prerequisites

- Python 3.11+
- Node.js 20+
- MongoDB 6.0+
- Git

#### Local Development Environment

```bash
# Clone the repository
git clone <repository-url>
cd youtube-video-fetcher

# Set up Python virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-asyncio black flake8 mypy

# Set up frontend
cd dashboard
npm install
npm install --save-dev @types/react @types/react-dom
cd ..

# Copy environment configuration
cp .env.example .env
# Edit .env with your development settings
```

### Code Structure

#### Backend Architecture

The backend follows a layered architecture pattern:

- **API Layer** (`app/api/`): FastAPI route handlers and request/response models
- **Service Layer** (`app/services/`): Business logic and external API integration
- **Data Layer** (`app/models/`): Data models and database schemas
- **Core Layer** (`app/core/`): Configuration, database connections, and utilities

#### Frontend Architecture

The frontend uses a component-based architecture:

- **Components** (`dashboard/src/components/`): Reusable React components
- **Services** (`dashboard/src/services/`): API integration and data fetching
- **Hooks** (`dashboard/src/hooks/`): Custom React hooks for state management
- **Utils** (`dashboard/src/utils/`): Utility functions and helpers

### Development Workflow

#### Backend Development

```bash
# Run the development server with auto-reload
python3 main.py

# Run tests
python3 -m pytest tests/

# Format code
black app/ tests/

# Lint code
flake8 app/ tests/

# Type checking
mypy app/
```

#### Frontend Development

```bash
cd dashboard

# Start development server
npm run dev

# Run tests
npm test

# Build for production
npm run build

# Lint code
npm run lint

# Format code
npm run format
```

### Testing

#### Backend Testing

The project includes comprehensive test suites:

```bash
# Run all tests
python3 -m pytest

# Run with coverage
python3 -m pytest --cov=app

# Run specific test file
python3 -m pytest tests/test_api.py

# Run tests with verbose output
python3 -m pytest -v
```

#### Frontend Testing

```bash
cd dashboard

# Run unit tests
npm test

# Run tests with coverage
npm run test:coverage

# Run end-to-end tests
npm run test:e2e
```

### Adding New Features

#### Adding a New API Endpoint

1. Define the endpoint in the appropriate router file (`app/api/`)
2. Create or update the service layer logic (`app/services/`)
3. Add or modify data models if needed (`app/models/`)
4. Write tests for the new functionality
5. Update API documentation

Example:

```python
# app/api/videos.py
@router.get("/trending")
async def get_trending_videos(limit: int = 10):
    """Get trending videos"""
    try:
        videos = await video_service.get_trending_videos(limit)
        return {"videos": videos}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

#### Adding a New React Component

1. Create the component file in `dashboard/src/components/`
2. Add necessary props and TypeScript interfaces
3. Implement the component logic and styling
4. Add the component to the main application
5. Write tests for the component

Example:

```jsx
// dashboard/src/components/TrendingVideos.jsx
import React, { useState, useEffect } from "react";
import { videoAPI } from "../services/api";

const TrendingVideos = ({ limit = 10 }) => {
  const [videos, setVideos] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchTrendingVideos = async () => {
      try {
        const response = await videoAPI.getTrendingVideos(limit);
        setVideos(response.videos);
      } catch (error) {
        console.error("Error fetching trending videos:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchTrendingVideos();
  }, [limit]);

  if (loading) return <div>Loading...</div>;

  return (
    <div className="trending-videos">
      {videos.map((video) => (
        <VideoCard key={video.video_id} video={video} />
      ))}
    </div>
  );
};

export default TrendingVideos;
```

### Code Style and Standards

#### Python Code Style

- Follow PEP 8 guidelines
- Use Black for code formatting
- Use type hints for all function parameters and return values
- Write docstrings for all public functions and classes
- Use meaningful variable and function names

#### JavaScript/React Code Style

- Use ESLint and Prettier for code formatting
- Follow React best practices and hooks patterns
- Use TypeScript for type safety
- Write JSDoc comments for complex functions
- Use semantic HTML and accessible design patterns

#### Git Workflow

1. Create feature branches from `main`
2. Make small, focused commits with clear messages
3. Write tests for new features
4. Ensure all tests pass before submitting PR
5. Update documentation as needed

### Debugging

#### Backend Debugging

```bash
# Enable debug logging
export DEBUG=True

# Run with Python debugger
python3 -m pdb main.py

# Use logging for debugging
import logging
logging.basicConfig(level=logging.DEBUG)
```

#### Frontend Debugging

```bash
# Use React Developer Tools browser extension
# Enable source maps in development
# Use console.log() and browser debugger
# Use React Strict Mode for catching issues
```

### Performance Considerations

#### Backend Performance

- Use async/await for all database operations
- Implement proper database indexing
- Use connection pooling for database connections
- Cache frequently accessed data
- Monitor API response times

#### Frontend Performance

- Use React.memo() for expensive components
- Implement virtual scrolling for large lists
- Optimize images and assets
- Use code splitting for large applications
- Monitor bundle size and loading times

## Troubleshooting

This section covers common issues and their solutions when working with the YouTube Video Fetcher API.

### Common Issues

#### MongoDB Connection Issues

**Problem**: `Connection refused` error when connecting to MongoDB

```
pymongo.errors.ServerSelectionTimeoutError: localhost:27017: [Errno 111] Connection refused
```

**Solutions**:

1. **Check MongoDB Service Status**

   ```bash
   sudo systemctl status mongod
   sudo systemctl start mongod  # If not running
   ```

2. **Verify MongoDB Installation**

   ```bash
   mongo --version
   mongod --version
   ```

3. **Check MongoDB Configuration**

   ```bash
   sudo nano /etc/mongod.conf
   # Ensure bindIp is set to 0.0.0.0 or includes your IP
   ```

4. **Use MongoDB Atlas**
   - Update `MONGODB_URL` in `.env` to use Atlas connection string
   - Ensure network access is configured correctly

#### YouTube API Issues

**Problem**: `Quota exceeded` errors

```
googleapiclient.errors.HttpError: <HttpError 403 when requesting ... returned "Quota exceeded">
```

**Solutions**:

1. **Check API Key Configuration**

   ```bash
   # Verify API keys are properly set
   echo $YOUTUBE_API_KEYS
   ```

2. **Monitor Quota Usage**

   - Use the admin dashboard to check quota status
   - Add more API keys to increase quota limit

3. **Optimize Fetch Frequency**
   ```env
   # Increase fetch interval to reduce API calls
   FETCH_INTERVAL=30  # Fetch every 30 seconds instead of 10
   ```

**Problem**: `Invalid API key` errors

```
googleapiclient.errors.HttpError: <HttpError 400 when requesting ... returned "API key not valid">
```

**Solutions**:

1. **Verify API Key Format**

   - Ensure API keys are properly formatted
   - Check for extra spaces or characters

2. **Enable YouTube Data API v3**

   - Go to Google Cloud Console
   - Enable YouTube Data API v3 for your project

3. **Check API Key Restrictions**
   - Ensure API key has proper permissions
   - Remove unnecessary restrictions

#### React Dashboard Issues

**Problem**: Dashboard not loading or showing blank page

**Solutions**:

1. **Check Console Errors**

   ```bash
   # Open browser developer tools and check console
   # Look for JavaScript errors or network issues
   ```

2. **Verify API Connection**

   ```bash
   # Test API endpoint directly
   curl http://localhost:8000/api/videos/stats
   ```

3. **Check CORS Configuration**

   ```python
   # Ensure CORS is properly configured in main.py
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["*"],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

4. **Rebuild Frontend**
   ```bash
   cd dashboard
   rm -rf node_modules package-lock.json
   npm install
   npm run dev
   ```

#### Performance Issues

**Problem**: Slow API responses or high memory usage

**Solutions**:

1. **Database Optimization**

   ```python
   # Ensure proper indexing
   await videos_collection.create_index([("published_at", -1)])
   await videos_collection.create_index("video_id", unique=True)
   ```

2. **Pagination Optimization**

   ```python
   # Use smaller page sizes for better performance
   per_page = min(per_page, 50)  # Limit to 50 items per page
   ```

3. **Memory Management**
   ```bash
   # Monitor memory usage
   htop
   # Restart services if memory usage is high
   sudo systemctl restart youtube-fetcher-api
   ```

#### Environment Configuration Issues

**Problem**: Environment variables not loading

**Solutions**:

1. **Check .env File Location**

   ```bash
   # Ensure .env file is in the project root
   ls -la .env
   ```

2. **Verify Environment Variable Format**

   ```env
   # Ensure no spaces around equals sign
   YOUTUBE_API_KEYS=key1,key2,key3
   # Not: YOUTUBE_API_KEYS = key1, key2, key3
   ```

3. **Check File Permissions**
   ```bash
   chmod 600 .env  # Secure permissions
   ```

### Debugging Steps

#### Step 1: Check System Status

```bash
# Check all services
sudo systemctl status mongod
sudo systemctl status youtube-fetcher-api

# Check ports
netstat -tlnp | grep :8000
netstat -tlnp | grep :27017
```

#### Step 2: Review Logs

```bash
# Application logs
tail -f /var/log/youtube-fetcher/app.log

# System logs
journalctl -u youtube-fetcher-api -f

# MongoDB logs
tail -f /var/log/mongodb/mongod.log
```

#### Step 3: Test Components Individually

```bash
# Test database connection
python3 -c "
from app.core.database import connect_to_mongo
import asyncio
asyncio.run(connect_to_mongo())
print('Database connection successful')
"

# Test YouTube API
python3 -c "
from app.services.youtube_service import youtube_client
print(f'API keys configured: {len(youtube_client.api_keys)}')
"

# Test API endpoints
curl -X GET http://localhost:8000/health
curl -X GET http://localhost:8000/api/videos/stats
```

#### Step 4: Validate Configuration

```bash
# Check environment variables
python3 -c "
from app.core.config import settings
print(f'MongoDB URL: {settings.mongodb_url}')
print(f'API Keys: {len(settings.get_api_keys())}')
print(f'Search Query: {settings.search_query}')
"
```

### Getting Help

If you encounter issues not covered in this troubleshooting guide:

1. **Check the GitHub Issues**: Look for similar problems and solutions
2. **Enable Debug Logging**: Set `DEBUG=True` in your `.env` file
3. **Collect System Information**: Include OS, Python version, and error logs
4. **Create a Minimal Reproduction**: Isolate the problem to its simplest form
5. **Submit an Issue**: Provide detailed information about the problem

### Monitoring and Maintenance

#### Health Checks

```bash
# API health check
curl http://localhost:8000/health

# Database health check
mongo --eval "db.adminCommand('ping')"

# System resource monitoring
htop
df -h
```

#### Regular Maintenance

1. **Update Dependencies**: Regularly update Python and Node.js packages
2. **Monitor Disk Space**: Ensure adequate space for database growth
3. **Backup Database**: Implement regular MongoDB backups
4. **Review Logs**: Check for errors or performance issues
5. **Update API Keys**: Rotate YouTube API keys periodically

## Contributing

We welcome contributions to the YouTube Video Fetcher API! This section outlines how to contribute effectively to the project.

### Getting Started

#### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:

   ```bash
   git clone https://github.com/your-username/youtube-video-fetcher.git
   cd youtube-video-fetcher
   ```

3. Add the upstream repository:
   ```bash
   git remote add upstream https://github.com/original-repo/youtube-video-fetcher.git
   ```

#### Development Environment

Follow the [Development Setup](#development-setup) instructions to set up your local development environment.

### Contribution Guidelines

#### Code of Conduct

- Be respectful and inclusive in all interactions
- Focus on constructive feedback and collaboration
- Help maintain a welcoming environment for all contributors

#### Types of Contributions

We welcome various types of contributions:

1. **Bug Reports**: Help us identify and fix issues
2. **Feature Requests**: Suggest new functionality or improvements
3. **Code Contributions**: Submit bug fixes or new features
4. **Documentation**: Improve or expand documentation
5. **Testing**: Add or improve test coverage
6. **Performance**: Optimize existing code

#### Before Contributing

1. **Check Existing Issues**: Look for existing issues or discussions
2. **Create an Issue**: For significant changes, create an issue first
3. **Discuss Approach**: Get feedback on your proposed solution
4. **Follow Standards**: Adhere to coding standards and best practices

### Submitting Changes

#### Pull Request Process

1. **Create a Branch**:

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes**:

   - Write clean, well-documented code
   - Follow existing code style and patterns
   - Add tests for new functionality
   - Update documentation as needed

3. **Test Your Changes**:

   ```bash
   # Run backend tests
   python3 -m pytest

   # Run frontend tests
   cd dashboard && npm test

   # Test the application manually
   ```

4. **Commit Changes**:

   ```bash
   git add .
   git commit -m "feat: add video trending analysis feature"
   ```

5. **Push to Your Fork**:

   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create Pull Request**:
   - Go to GitHub and create a pull request
   - Provide a clear description of changes
   - Reference any related issues
   - Include screenshots for UI changes

#### Commit Message Format

Use conventional commit messages:

- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `test:` for adding tests
- `refactor:` for code refactoring
- `style:` for formatting changes
- `chore:` for maintenance tasks

Examples:

```
feat: add video analytics dashboard
fix: resolve MongoDB connection timeout issue
docs: update API documentation for new endpoints
test: add unit tests for video service
```

### Development Standards

#### Code Quality

- **Python**: Follow PEP 8, use type hints, write docstrings
- **JavaScript/React**: Use ESLint, Prettier, and TypeScript
- **Testing**: Maintain high test coverage (>80%)
- **Documentation**: Update docs for all public APIs

#### Review Process

1. **Automated Checks**: Ensure all CI checks pass
2. **Code Review**: Address feedback from maintainers
3. **Testing**: Verify functionality works as expected
4. **Documentation**: Confirm docs are updated appropriately

### Feature Development

#### Adding New API Endpoints

1. **Design the API**: Consider REST principles and consistency
2. **Implement Service Logic**: Add business logic to service layer
3. **Create Data Models**: Define Pydantic models for request/response
4. **Write Tests**: Add comprehensive test coverage
5. **Update Documentation**: Document the new endpoint

#### Adding Frontend Features

1. **Design the UI**: Consider user experience and accessibility
2. **Create Components**: Build reusable React components
3. **Integrate with API**: Connect to backend services
4. **Add Tests**: Write unit and integration tests
5. **Update Documentation**: Document new features

### Testing Guidelines

#### Backend Testing

```python
# Example test structure
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_videos():
    response = client.get("/api/videos/")
    assert response.status_code == 200
    assert "videos" in response.json()

@pytest.mark.asyncio
async def test_video_service():
    # Test service layer functionality
    pass
```

#### Frontend Testing

```javascript
// Example React component test
import { render, screen } from "@testing-library/react";
import VideoCard from "../VideoCard";

test("renders video card with title", () => {
  const mockVideo = {
    video_id: "test123",
    title: "Test Video",
    // ... other properties
  };

  render(<VideoCard video={mockVideo} />);
  expect(screen.getByText("Test Video")).toBeInTheDocument();
});
```

### Documentation

#### API Documentation

- Use clear, descriptive endpoint names
- Provide comprehensive parameter descriptions
- Include example requests and responses
- Document error conditions and status codes

#### Code Documentation

- Write clear docstrings for all functions and classes
- Include type hints for Python code
- Add inline comments for complex logic
- Keep documentation up-to-date with code changes

### Release Process

#### Version Management

- Follow semantic versioning (MAJOR.MINOR.PATCH)
- Update version numbers in appropriate files
- Create release notes for significant changes
- Tag releases in Git

#### Deployment

- Test changes in staging environment
- Ensure backward compatibility
- Update deployment documentation
- Monitor post-deployment metrics

### Community

#### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and ideas
- **Pull Requests**: Code review and collaboration

#### Recognition

Contributors will be recognized in:

- README.md contributors section
- Release notes for significant contributions
- GitHub contributor statistics

Thank you for contributing to the YouTube Video Fetcher API! Your contributions help make this project better for everyone.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

### MIT License Summary

The MIT License is a permissive open-source license that allows you to:

- **Use** the software for any purpose
- **Copy** and distribute the software
- **Modify** the software and create derivative works
- **Distribute** modified versions
- **Use** the software in commercial applications

#### Requirements

- Include the original license and copyright notice in any copy of the software
- Include the license notice in any substantial portions of the software

#### Limitations

- The software is provided "as is" without warranty
- Authors are not liable for any damages or issues arising from use

### Third-Party Licenses

This project uses several third-party libraries and frameworks, each with their own licenses:

#### Backend Dependencies

- **FastAPI**: MIT License
- **MongoDB Motor**: Apache License 2.0
- **Pydantic**: MIT License
- **Google API Client**: Apache License 2.0
- **Uvicorn**: BSD License

#### Frontend Dependencies

- **React**: MIT License
- **Vite**: MIT License
- **Tailwind CSS**: MIT License
- **Lucide React**: ISC License
- **Axios**: MIT License

### Contributing License Agreement

By contributing to this project, you agree that your contributions will be licensed under the same MIT License that covers the project. This ensures that the project remains open and accessible to all users.

---

**YouTube Video Fetcher API** - A comprehensive solution for fetching, storing, and managing YouTube videos with a modern web interface.

For more information, visit the [project repository](https://github.com/your-username/youtube-video-fetcher) or check the [API documentation](http://localhost:8000/docs).

_Built with ❤️ by the open-source community_
