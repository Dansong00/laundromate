// apps/web/next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  // Enable server-side rendering for Railway
  // output: 'export', // Removed - causes issues with Railway

  // Enable image optimization
  images: {
    unoptimized: false,
  },

  // Enable compression for production
  compress: true,
};

module.exports = nextConfig;