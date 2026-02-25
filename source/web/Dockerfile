# Use an official Node.js runtime as a parent image
FROM node:20-slim AS base

# Set environment variables
ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"

# Enable corepack
RUN corepack enable
# WORKAROUND HERE:
RUN corepack prepare pnpm@10.28.1 --activate

RUN pnpm install -g serve

# Copy application code
COPY . /app
WORKDIR /app

# Stage for installing production dependencies
FROM base AS prod-deps
RUN --mount=type=secret,id=npm,target=/root/.npmrc --mount=type=cache,id=pnpm,target=/pnpm/store pnpm install --prod --frozen-lockfile --registry https://pkgs.dev.azure.com/EclipseInsightsHC/Commercialization/_packaging/eclipse-insights-nuget/npm/registry/

# Stage for building the application
FROM base AS build
RUN --mount=type=secret,id=npm,target=/root/.npmrc --mount=type=cache,id=pnpm,target=/pnpm/store pnpm install --frozen-lockfile --registry https://pkgs.dev.azure.com/EclipseInsightsHC/Commercialization/_packaging/eclipse-insights-nuget/npm/registry/
RUN pnpm run build

# Final stage
FROM base
COPY --from=prod-deps /app/node_modules /app/node_modules
COPY --from=build /app/dist /app/dist
EXPOSE 8086
CMD ["pnpm", "build:start"]
