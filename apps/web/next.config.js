// apps/web/next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  // Disable static generation
  output: 'export',

  // Disable image optimization
  images: {
    unoptimized: true,
  },

  // Disable all experimental features
  experimental: {},

  // Disable compression
  compress: false,
};

module.exports = nextConfig;