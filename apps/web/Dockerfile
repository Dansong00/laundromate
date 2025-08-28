FROM node:18-alpine AS base

# Install dependencies only when needed
FROM base AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app

# Allow building from monorepo root or app dir
ARG APP_DIR=apps/web

# Install all dependencies (including dev) for build step
COPY ${APP_DIR}/package.json ${APP_DIR}/package-lock.json* ./
RUN npm ci

# Rebuild the source code only when needed
FROM base AS builder
WORKDIR /app
ARG APP_DIR=apps/web
COPY --from=deps /app/node_modules ./node_modules
COPY ${APP_DIR}/ .

# Next.js collects completely anonymous telemetry data about general usage.
# Learn more here: https://nextjs.org/telemetry
# Uncomment the following line in case you want to disable telemetry during the build.
ENV NEXT_TELEMETRY_DISABLED 1

RUN npm run build

# Production image, copy all the files and run next
FROM base AS runner
WORKDIR /app
ARG APP_DIR=apps/web

ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED 1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY ${APP_DIR}/public ./public
COPY ${APP_DIR}/package.json ./package.json

# Install only production deps in runner
COPY ${APP_DIR}/package-lock.json* ./
RUN npm ci --omit=dev && npm cache clean --force

# Set the correct permission for prerender cache
RUN mkdir .next
RUN chown nextjs:nodejs .next

# Copy the built Next.js app
COPY --from=builder --chown=nextjs:nodejs /app/.next ./.next

USER nextjs

ENV PORT 3000
ENV HOSTNAME "0.0.0.0"

CMD ["sh", "-c", "npm start -- -p $PORT"]