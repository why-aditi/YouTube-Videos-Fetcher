import axios from "axios";

const API_BASE_URL = "http://localhost:8000/api";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export const videoAPI = {
  // Get paginated videos
  getVideos: async (params = {}) => {
    const response = await api.get("/videos/", { params });
    return response.data;
  },

  // Get latest videos
  getLatestVideos: async (limit = 10) => {
    const response = await api.get("/videos/latest", { params: { limit } });
    return response.data;
  },

  // Get video statistics
  getVideoStats: async () => {
    const response = await api.get("/videos/stats");
    return response.data;
  },

  // Get specific video by ID
  getVideoById: async (videoId) => {
    const response = await api.get(`/videos/${videoId}`);
    return response.data;
  },
};

export const adminAPI = {
  // Get system status
  getSystemStatus: async () => {
    const response = await api.get("/admin/status");
    return response.data;
  },

  // Start background fetching
  startBackgroundFetching: async () => {
    const response = await api.post("/admin/background/start");
    return response.data;
  },

  // Stop background fetching
  stopBackgroundFetching: async () => {
    const response = await api.post("/admin/background/stop");
    return response.data;
  },

  // Force fetch videos
  forceFetchVideos: async () => {
    const response = await api.post("/admin/background/force-fetch");
    return response.data;
  },

  // Get background status
  getBackgroundStatus: async () => {
    const response = await api.get("/admin/background/status");
    return response.data;
  },

  // Get YouTube quota status
  getYouTubeQuotaStatus: async () => {
    const response = await api.get("/admin/youtube/quota");
    return response.data;
  },
};

export default api;
