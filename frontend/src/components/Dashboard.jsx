import React, { useState, useEffect } from 'react';
import { 
  Search, 
  Filter, 
  RefreshCw, 
  Play, 
  Pause, 
  Settings, 
  BarChart3,
  Calendar,
  User,
  Database,
  Activity
} from 'lucide-react';
import VideoCard from './VideoCard';
import Pagination from './Pagination';
import { videoAPI, adminAPI } from '../services/api';

const Dashboard = () => {
  const [videos, setVideos] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  // Pagination
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalVideos, setTotalVideos] = useState(0);
  const [perPage, setPerPage] = useState(20);
  
  // Filters
  const [searchTerm, setSearchTerm] = useState('');
  const [channelFilter, setChannelFilter] = useState('');
  const [dateFilter, setDateFilter] = useState('');
  
  // System status
  const [systemStatus, setSystemStatus] = useState(null);
  const [stats, setStats] = useState(null);
  
  // UI state
  const [showFilters, setShowFilters] = useState(false);
  const [showAdmin, setShowAdmin] = useState(false);

  // Load videos
  const loadVideos = async (page = currentPage) => {
    setLoading(true);
    setError(null);
    
    try {
      const params = {
        page,
        per_page: perPage,
      };
      
      if (searchTerm) params.search = searchTerm;
      if (channelFilter) params.channel_id = channelFilter;
      if (dateFilter) {
        const date = new Date();
        switch (dateFilter) {
          case 'today':
            date.setHours(0, 0, 0, 0);
            params.published_after = date.toISOString();
            break;
          case 'week':
            date.setDate(date.getDate() - 7);
            params.published_after = date.toISOString();
            break;
          case 'month':
            date.setMonth(date.getMonth() - 1);
            params.published_after = date.toISOString();
            break;
        }
      }
      
      const response = await videoAPI.getVideos(params);
      setVideos(response.videos);
      setCurrentPage(response.page);
      setTotalPages(response.total_pages);
      setTotalVideos(response.total);
    } catch (err) {
      setError('Failed to load videos: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  // Load system status
  const loadSystemStatus = async () => {
    try {
      const [statusResponse, statsResponse] = await Promise.all([
        adminAPI.getSystemStatus(),
        videoAPI.getVideoStats()
      ]);
      setSystemStatus(statusResponse);
      setStats(statsResponse);
    } catch (err) {
      console.error('Failed to load system status:', err);
    }
  };

  // Handle search
  const handleSearch = (e) => {
    e.preventDefault();
    setCurrentPage(1);
    loadVideos(1);
  };

  // Handle filter changes
  const handleFilterChange = () => {
    setCurrentPage(1);
    loadVideos(1);
  };

  // Admin actions
  const handleStartFetching = async () => {
    try {
      await adminAPI.startBackgroundFetching();
      loadSystemStatus();
    } catch (err) {
      setError('Failed to start background fetching: ' + err.message);
    }
  };

  const handleStopFetching = async () => {
    try {
      await adminAPI.stopBackgroundFetching();
      loadSystemStatus();
    } catch (err) {
      setError('Failed to stop background fetching: ' + err.message);
    }
  };

  const handleForceFetch = async () => {
    try {
      setLoading(true);
      await adminAPI.forceFetchVideos();
      await loadVideos();
      await loadSystemStatus();
    } catch (err) {
      setError('Failed to force fetch: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  // Initial load
  useEffect(() => {
    loadVideos();
    loadSystemStatus();
  }, []);

  // Auto-refresh system status
  useEffect(() => {
    const interval = setInterval(loadSystemStatus, 30000); // Every 30 seconds
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center">
              <Database className="h-8 w-8 text-blue-600 mr-3" />
              <h1 className="text-2xl font-bold text-gray-900">YouTube Video Fetcher</h1>
            </div>
            
            <div className="flex items-center space-x-4">
              {/* System Status Indicator */}
              {systemStatus && (
                <div className="flex items-center space-x-2">
                  <Activity 
                    className={`h-5 w-5 ${
                      systemStatus.background_service.is_running ? 'text-green-500' : 'text-red-500'
                    }`} 
                  />
                  <span className="text-sm text-gray-600">
                    {systemStatus.background_service.is_running ? 'Active' : 'Stopped'}
                  </span>
                </div>
              )}
              
              <button
                onClick={() => setShowAdmin(!showAdmin)}
                className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-md"
                title="Admin Controls"
              >
                <Settings className="h-5 w-5" />
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Admin Panel */}
      {showAdmin && (
        <div className="bg-blue-50 border-b">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4">
                <h3 className="text-lg font-medium text-gray-900">Admin Controls</h3>
                {systemStatus && (
                  <div className="flex items-center space-x-4 text-sm">
                    <span>
                      Fetches: {systemStatus.background_service.fetch_count}
                    </span>
                    <span>
                      API Keys: {systemStatus.youtube_api.available_keys}/{systemStatus.youtube_api.total_keys}
                    </span>
                  </div>
                )}
              </div>
              
              <div className="flex items-center space-x-2">
                <button
                  onClick={handleForceFetch}
                  disabled={loading}
                  className="px-3 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 flex items-center space-x-1"
                >
                  <RefreshCw className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
                  <span>Force Fetch</span>
                </button>
                
                {systemStatus?.background_service.is_running ? (
                  <button
                    onClick={handleStopFetching}
                    className="px-3 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 flex items-center space-x-1"
                  >
                    <Pause className="h-4 w-4" />
                    <span>Stop</span>
                  </button>
                ) : (
                  <button
                    onClick={handleStartFetching}
                    className="px-3 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 flex items-center space-x-1"
                  >
                    <Play className="h-4 w-4" />
                    <span>Start</span>
                  </button>
                )}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Stats Bar */}
      {stats && (
        <div className="bg-white border-b">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3">
            <div className="flex items-center justify-between text-sm text-gray-600">
              <div className="flex items-center space-x-6">
                <div className="flex items-center space-x-1">
                  <BarChart3 className="h-4 w-4" />
                  <span>Total Videos: {stats.total_videos.toLocaleString()}</span>
                </div>
                {stats.latest_video && (
                  <div className="flex items-center space-x-1">
                    <Calendar className="h-4 w-4" />
                    <span>
                      Latest: {new Date(stats.latest_video.published_at).toLocaleDateString()}
                    </span>
                  </div>
                )}
              </div>
              
              <div className="text-right">
                Showing {totalVideos.toLocaleString()} videos
              </div>
            </div>
          </div>
        </div>
      )}

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {/* Search and Filters */}
        <div className="mb-6">
          <div className="flex flex-col sm:flex-row gap-4">
            {/* Search */}
            <form onSubmit={handleSearch} className="flex-1">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
                <input
                  type="text"
                  placeholder="Search videos, channels, or descriptions..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
            </form>
            
            {/* Filter Toggle */}
            <button
              onClick={() => setShowFilters(!showFilters)}
              className="px-4 py-2 border border-gray-300 rounded-md hover:bg-gray-50 flex items-center space-x-2"
            >
              <Filter className="h-4 w-4" />
              <span>Filters</span>
            </button>
          </div>

          {/* Filters Panel */}
          {showFilters && (
            <div className="mt-4 p-4 bg-white rounded-lg border border-gray-200">
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Channel ID
                  </label>
                  <input
                    type="text"
                    placeholder="Filter by channel ID"
                    value={channelFilter}
                    onChange={(e) => setChannelFilter(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Published Date
                  </label>
                  <select
                    value={dateFilter}
                    onChange={(e) => setDateFilter(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    <option value="">All time</option>
                    <option value="today">Today</option>
                    <option value="week">Past week</option>
                    <option value="month">Past month</option>
                  </select>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Per Page
                  </label>
                  <select
                    value={perPage}
                    onChange={(e) => setPerPage(Number(e.target.value))}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    <option value={10}>10</option>
                    <option value={20}>20</option>
                    <option value={50}>50</option>
                    <option value={100}>100</option>
                  </select>
                </div>
              </div>
              
              <div className="mt-4 flex justify-end">
                <button
                  onClick={handleFilterChange}
                  className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
                >
                  Apply Filters
                </button>
              </div>
            </div>
          )}
        </div>

        {/* Error Message */}
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-md">
            <p className="text-red-800">{error}</p>
          </div>
        )}

        {/* Loading State */}
        {loading && (
          <div className="flex justify-center items-center py-12">
            <RefreshCw className="h-8 w-8 animate-spin text-blue-600" />
            <span className="ml-2 text-gray-600">Loading videos...</span>
          </div>
        )}

        {/* Videos Grid */}
        {!loading && videos.length > 0 && (
          <>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 mb-8">
              {videos.map((video) => (
                <VideoCard key={video.video_id} video={video} />
              ))}
            </div>

            {/* Pagination */}
            <Pagination
              currentPage={currentPage}
              totalPages={totalPages}
              onPageChange={(page) => {
                setCurrentPage(page);
                loadVideos(page);
              }}
              className="mt-8"
            />
          </>
        )}

        {/* Empty State */}
        {!loading && videos.length === 0 && (
          <div className="text-center py-12">
            <Database className="h-16 w-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No videos found</h3>
            <p className="text-gray-600 mb-4">
              {searchTerm || channelFilter || dateFilter
                ? 'Try adjusting your search criteria or filters.'
                : 'No videos have been fetched yet. Check the admin panel to start fetching.'}
            </p>
            {!searchTerm && !channelFilter && !dateFilter && (
              <button
                onClick={handleForceFetch}
                disabled={loading}
                className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
              >
                Fetch Videos Now
              </button>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;

