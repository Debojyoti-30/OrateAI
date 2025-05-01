import React from 'react';

const VideoPlayer = ({ videoSrc }) => {
  return (
    <video controls width="100%">
      <source src={videoSrc} type="video/mp4" />
      Your browser does not support the video tag.
    </video>
  );
};

export default VideoPlayer;
