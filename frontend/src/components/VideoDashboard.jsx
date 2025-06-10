import React, { useState, useEffect } from 'react';
import {
  Box,
  TextField,
  Card,
  CardContent,
  Typography,
  Grid,
  CircularProgress,
  Alert,
  Pagination,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from '@mui/material';
import { API_BASE_URL, VIDEOS_PER_PAGE } from '../config';

const VideoDashboard = () => {
  const [videos, setVideos] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(0);
  const [searchTerm, setSearchTerm] = useState('');
  const [channelTitle, setChannelTitle] = useState('');
  const [sortBy, setSortBy] = useState('published_at');

  const fetchVideos = async () => {
    setLoading(true);
    setError(null);
    try {
      const queryParams = new URLSearchParams({
        page,
        per_page: VIDEOS_PER_PAGE,
        sort: sortBy,
      });

      if (searchTerm) queryParams.append('search', searchTerm);
      if (channelTitle) queryParams.append('channel_title', channelTitle);

      const response = await fetch(`${API_BASE_URL}/videos?${queryParams}`);
      if (!response.ok) throw new Error('Failed to fetch videos');
      
      const data = await response.json();
      setVideos(data.videos);
      setTotalPages(data.total_pages);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchVideos();
  }, [page, sortBy]);

  const handleSearch = () => {
    setPage(1);
    fetchVideos();
  };

  const handlePageChange = (event, value) => {
    setPage(value);
  };

  return (
    <Box sx={{ p: 3 }}>
      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={4}>
          <TextField
            fullWidth
            label="Search Videos"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
          />
        </Grid>
        <Grid item xs={12} sm={4}>
          <TextField
            fullWidth
            label="Search by Channel Name"
            value={channelTitle}
            onChange={(e) => setChannelTitle(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
          />
        </Grid>
        <Grid item xs={12} sm={4}>
          <FormControl fullWidth>
            <InputLabel>Sort By</InputLabel>
            <Select
              value={sortBy}
              label="Sort By"
              onChange={(e) => setSortBy(e.target.value)}
            >
              <MenuItem value="published_at">Published Date</MenuItem>
              <MenuItem value="view_count">View Count</MenuItem>
              <MenuItem value="like_count">Like Count</MenuItem>
            </Select>
          </FormControl>
        </Grid>
      </Grid>

      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

      {loading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
          <CircularProgress />
        </Box>
      ) : (
        <>
          <Grid container spacing={2}>
            {videos.map((video) => (
              <Grid item xs={12} sm={6} md={4} key={video.video_id}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" noWrap>{video.title}</Typography>
                    <Typography variant="subtitle2" color="text.secondary">
                      {video.channel_title}
                    </Typography>
                    <Typography variant="body2" color="text.secondary" noWrap>
                      {video.description}
                    </Typography>
                    <Typography variant="caption" display="block">
                      Published: {new Date(video.published_at).toLocaleDateString()}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>

          <Box sx={{ display: 'flex', justifyContent: 'center', mt: 3 }}>
            <Pagination
              count={totalPages}
              page={page}
              onChange={handlePageChange}
              color="primary"
            />
          </Box>
        </>
      )}
    </Box>
  );
};

export default VideoDashboard;