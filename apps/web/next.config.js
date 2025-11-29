// apps/web/next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  // Enable server-side rendering for Railway
  // Enable standalone output for Docker builds
  output: 'standalone',

  transpilePackages: ['@laundromate/ui'],

  // Enable image optimization
  images: {
    unoptimized: false,
  },

  // Enable compression for production
  compress: true,
};

module.exports = nextConfig;