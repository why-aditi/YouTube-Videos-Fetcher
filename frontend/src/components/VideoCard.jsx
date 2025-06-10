import React from 'react';
import { formatDistanceToNow } from 'date-fns';
import { Play, Eye, ThumbsUp, MessageCircle, Calendar, User } from 'lucide-react';

const VideoCard = ({ video }) => {
  const formatNumber = (num) => {
    if (num >= 1000000) {
      return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
      return (num / 1000).toFixed(1) + 'K';
    }
    return num?.toString() || '0';
  };

  const formatDuration = (duration) => {
    if (!duration) return '';
    // Parse ISO 8601 duration (PT4M13S -> 4:13)
    const match = duration.match(/PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?/);
    if (!match) return '';
    
    const hours = parseInt(match[1] || 0);
    const minutes = parseInt(match[2] || 0);
    const seconds = parseInt(match[3] || 0);
    
    if (hours > 0) {
      return `${hours}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    }
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  };

  const openVideo = () => {
    window.open(`https://www.youtube.com/watch?v=${video.video_id}`, '_blank');
  };

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300">
      {/* Thumbnail */}
      <div className="relative cursor-pointer" onClick={openVideo}>
        <img
          src={video.thumbnails?.high?.url || video.thumbnails?.medium?.url || video.thumbnails?.default?.url}
          alt={video.title}
          className="w-full h-48 object-cover"
        />
        <div className="absolute inset-0 bg-black bg-opacity-0 hover:bg-opacity-20 transition-all duration-300 flex items-center justify-center">
          <Play className="text-white opacity-0 hover:opacity-100 transition-opacity duration-300" size={48} />
        </div>
        {video.duration && (
          <div className="absolute bottom-2 right-2 bg-black bg-opacity-80 text-white text-xs px-2 py-1 rounded">
            {formatDuration(video.duration)}
          </div>
        )}
      </div>

      {/* Content */}
      <div className="p-4">
        {/* Title */}
        <h3 
          className="font-semibold text-gray-900 mb-2 line-clamp-2 cursor-pointer hover:text-blue-600 transition-colors"
          onClick={openVideo}
          title={video.title}
        >
          {video.title}
        </h3>

        {/* Channel */}
        <div className="flex items-center text-sm text-gray-600 mb-2">
          <User size={14} className="mr-1" />
          <span className="truncate">{video.channel_title}</span>
        </div>

        {/* Stats */}
        <div className="flex items-center justify-between text-sm text-gray-500 mb-3">
          <div className="flex items-center space-x-4">
            {video.view_count > 0 && (
              <div className="flex items-center">
                <Eye size={14} className="mr-1" />
                <span>{formatNumber(video.view_count)}</span>
              </div>
            )}
            {video.like_count > 0 && (
              <div className="flex items-center">
                <ThumbsUp size={14} className="mr-1" />
                <span>{formatNumber(video.like_count)}</span>
              </div>
            )}
            {video.comment_count > 0 && (
              <div className="flex items-center">
                <MessageCircle size={14} className="mr-1" />
                <span>{formatNumber(video.comment_count)}</span>
              </div>
            )}
          </div>
        </div>

        {/* Published Date */}
        <div className="flex items-center text-xs text-gray-400">
          <Calendar size={12} className="mr-1" />
          <span>
            {formatDistanceToNow(new Date(video.published_at), { addSuffix: true })}
          </span>
        </div>

        {/* Description Preview */}
        {video.description && (
          <p className="text-sm text-gray-600 mt-2 line-clamp-2" title={video.description}>
            {video.description}
          </p>
        )}

        {/* Tags */}
        {video.tags && video.tags.length > 0 && (
          <div className="mt-3 flex flex-wrap gap-1">
            {video.tags.slice(0, 3).map((tag, index) => (
              <span
                key={index}
                className="inline-block bg-gray-100 text-gray-700 text-xs px-2 py-1 rounded-full"
              >
                #{tag}
              </span>
            ))}
            {video.tags.length > 3 && (
              <span className="text-xs text-gray-500">+{video.tags.length - 3} more</span>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default VideoCard;

